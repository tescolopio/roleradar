"""API usage tracking service for monitoring Tavily and Groq API calls."""

from datetime import datetime, date, timezone, timedelta
from typing import Dict, List, Any, Optional
from sqlalchemy import func, desc
from ..database import db_service
from ..models import APIUsageLog


class APITracker:
    """Track and analyze API usage across services."""

    @staticmethod
    def log_api_call(
        api_name: str,
        endpoint: str = None,
        query: str = None,
        result_count: int = None,
        error: str = None
    ) -> bool:
        """
        Log an API call to the tracking table.

        Args:
            api_name: Name of the API ('tavily', 'groq')
            endpoint: The specific endpoint called
            query: The query or prompt (will be truncated to 500 chars)
            result_count: Number of results returned
            error: Error message if the call failed

        Returns:
            True if logged successfully, False otherwise
        """
        try:
            now = datetime.now(timezone.utc)
            today = now.date()
            hour = now.hour

            # Truncate query to 500 chars
            if query and len(query) > 500:
                query = query[:500] + "..."

            with db_service.get_session() as session:
                # Check if log exists for this api/endpoint/date/hour combination
                log = session.query(APIUsageLog).filter_by(
                    api_name=api_name,
                    endpoint=endpoint,
                    date=today,
                    hour=hour
                ).first()

                if log:
                    # Increment existing log
                    log.request_count += 1
                    if result_count:
                        log.result_count = (log.result_count or 0) + result_count
                    if error:
                        log.error = error
                    log.updated_at = now
                else:
                    # Create new log entry
                    log = APIUsageLog(
                        api_name=api_name,
                        endpoint=endpoint,
                        date=today,
                        hour=hour,
                        query=query,
                        result_count=result_count,
                        error=error,
                        request_count=1
                    )
                    session.add(log)

                session.commit()
            return True

        except Exception as e:
            print(f"⚠️  Error logging API call: {e}")
            return False

    @staticmethod
    def get_usage_summary(days: int = 7) -> Dict[str, Any]:
        """
        Get API usage summary for the last N days.

        Args:
            days: Number of days to include in summary

        Returns:
            Dictionary with daily and total usage statistics
        """
        try:
            cutoff_date = date.today() - timedelta(days=days)

            with db_service.get_session() as session:
                # Daily totals by API
                daily = session.query(
                    APIUsageLog.api_name,
                    APIUsageLog.date,
                    func.sum(APIUsageLog.request_count).label('total_calls'),
                    func.sum(APIUsageLog.result_count).label('total_results'),
                    func.count(func.distinct(APIUsageLog.endpoint)).label('endpoints')
                ).filter(
                    APIUsageLog.date >= cutoff_date
                ).group_by(
                    APIUsageLog.api_name,
                    APIUsageLog.date
                ).order_by(
                    APIUsageLog.date.desc(),
                    APIUsageLog.api_name
                ).all()

                # Total by API
                totals = session.query(
                    APIUsageLog.api_name,
                    func.sum(APIUsageLog.request_count).label('total_calls'),
                    func.sum(APIUsageLog.result_count).label('total_results')
                ).filter(
                    APIUsageLog.date >= cutoff_date
                ).group_by(
                    APIUsageLog.api_name
                ).all()

                # Format results
                daily_data = [
                    {
                        'api': d[0],
                        'date': str(d[1]),
                        'calls': d[2] or 0,
                        'results': d[3] or 0,
                        'endpoints': d[4] or 0
                    }
                    for d in daily
                ]

                totals_data = {
                    t[0]: {
                        'calls': t[1] or 0,
                        'results': t[2] or 0
                    }
                    for t in totals
                }

                return {
                    'daily': daily_data,
                    'totals': totals_data,
                    'period_days': days
                }

        except Exception as e:
            print(f"⚠️  Error getting usage summary: {e}")
            return {'daily': [], 'totals': {}, 'error': str(e)}

    @staticmethod
    def get_hourly_breakdown(api_name: str = None, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get hourly API usage breakdown.

        Args:
            api_name: Filter by specific API ('tavily', 'groq'), or None for all
            days: Number of days to include

        Returns:
            List of hourly usage records
        """
        try:
            cutoff_date = date.today() - timedelta(days=days)

            with db_service.get_session() as session:
                query = session.query(
                    APIUsageLog.api_name,
                    APIUsageLog.date,
                    APIUsageLog.hour,
                    func.sum(APIUsageLog.request_count).label('total_calls'),
                    func.sum(APIUsageLog.result_count).label('total_results')
                ).filter(
                    APIUsageLog.date >= cutoff_date
                )

                if api_name:
                    query = query.filter(APIUsageLog.api_name == api_name)

                results = query.group_by(
                    APIUsageLog.api_name,
                    APIUsageLog.date,
                    APIUsageLog.hour
                ).order_by(
                    APIUsageLog.date.desc(),
                    APIUsageLog.hour.desc()
                ).all()

                return [
                    {
                        'api': r[0],
                        'date': str(r[1]),
                        'hour': f"{r[2]:02d}:00" if r[2] is not None else 'unknown',
                        'calls': r[3] or 0,
                        'results': r[4] or 0
                    }
                    for r in results
                ]

        except Exception as e:
            print(f"⚠️  Error getting hourly breakdown: {e}")
            return []

    @staticmethod
    def get_top_queries(api_name: str = None, days: int = 7, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get the most frequent queries/prompts.

        Args:
            api_name: Filter by specific API ('tavily', 'groq'), or None for all
            days: Number of days to include
            limit: Maximum number of queries to return

        Returns:
            List of top queries with call counts
        """
        try:
            cutoff_date = date.today() - timedelta(days=days)

            with db_service.get_session() as session:
                query = session.query(
                    APIUsageLog.api_name,
                    APIUsageLog.endpoint,
                    APIUsageLog.query,
                    func.sum(APIUsageLog.request_count).label('total_calls')
                ).filter(
                    APIUsageLog.date >= cutoff_date,
                    APIUsageLog.query.isnot(None)
                )

                if api_name:
                    query = query.filter(APIUsageLog.api_name == api_name)

                results = query.group_by(
                    APIUsageLog.api_name,
                    APIUsageLog.endpoint,
                    APIUsageLog.query
                ).order_by(
                    desc('total_calls')
                ).limit(limit).all()

                return [
                    {
                        'api': r[0],
                        'endpoint': r[1],
                        'query': r[2][:100] if r[2] else 'N/A',
                        'calls': r[3] or 0
                    }
                    for r in results
                ]

        except Exception as e:
            print(f"⚠️  Error getting top queries: {e}")
            return []

    @staticmethod
    def get_error_summary(api_name: str = None, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get summary of API errors.

        Args:
            api_name: Filter by specific API ('tavily', 'groq'), or None for all
            days: Number of days to include

        Returns:
            List of errors with counts
        """
        try:
            cutoff_date = date.today() - timedelta(days=days)

            with db_service.get_session() as session:
                query = session.query(
                    APIUsageLog.api_name,
                    APIUsageLog.error,
                    func.count(APIUsageLog.id).label('error_count')
                ).filter(
                    APIUsageLog.date >= cutoff_date,
                    APIUsageLog.error.isnot(None)
                )

                if api_name:
                    query = query.filter(APIUsageLog.api_name == api_name)

                results = query.group_by(
                    APIUsageLog.api_name,
                    APIUsageLog.error
                ).order_by(
                    desc('error_count')
                ).all()

                return [
                    {
                        'api': r[0],
                        'error': r[1][:200] if r[1] else 'Unknown',
                        'count': r[2] or 0
                    }
                    for r in results
                ]

        except Exception as e:
            print(f"⚠️  Error getting error summary: {e}")
            return []

    @staticmethod
    def get_daily_stats(date_str: str = None) -> Dict[str, Any]:
        """
        Get detailed stats for a specific day (today if not specified).

        Args:
            date_str: Date in YYYY-MM-DD format, or None for today

        Returns:
            Dictionary with daily statistics
        """
        try:
            if date_str:
                from datetime import datetime as dt
                target_date = dt.strptime(date_str, '%Y-%m-%d').date()
            else:
                target_date = date.today()

            with db_service.get_session() as session:
                # Overall daily stats
                overall = session.query(
                    APIUsageLog.api_name,
                    func.sum(APIUsageLog.request_count).label('calls'),
                    func.sum(APIUsageLog.result_count).label('results'),
                    func.count(func.distinct(APIUsageLog.endpoint)).label('endpoints'),
                    func.count(func.distinct(APIUsageLog.hour)).label('active_hours')
                ).filter(
                    APIUsageLog.date == target_date
                ).group_by(
                    APIUsageLog.api_name
                ).all()

                stats = {
                    'date': str(target_date),
                    'apis': {}
                }

                for api, calls, results, endpoints, active_hours in overall:
                    stats['apis'][api] = {
                        'calls': calls or 0,
                        'results': results or 0,
                        'endpoints': endpoints or 0,
                        'active_hours': active_hours or 0,
                        'avg_calls_per_hour': round((calls or 0) / (active_hours or 1), 1)
                    }

                return stats

        except Exception as e:
            print(f"⚠️  Error getting daily stats: {e}")
            return {'error': str(e)}
