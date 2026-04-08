"""Flask dashboard for RoleRadar."""

from flask import Flask, render_template, jsonify, request
from ..services import ProcessingService, TavilySearchService, BraveSearchService, GroqAnalysisService, get_search_service
from ..services.groq_service import get_prompt_templates
from ..database import db_service
from ..config import config
from ..models.database import HiringSignal, Company, Opportunity
from sqlalchemy import desc
from datetime import datetime, timedelta, timezone
import json


def create_app():
    """Create Flask application."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config.FLASK_SECRET_KEY

    # Initialize database tables
    db_service.create_tables()

    # Load configuration from database (overrides env vars)
    config.load_from_database()

    processing_service = ProcessingService()
    
    # ==================== Public Dashboard Routes ====================
    
    @app.route('/')
    def index():
        """Dashboard home page."""
        return render_template('index.html')
    
    @app.route('/admin')
    def admin():
        """Admin management dashboard."""
        return render_template('admin.html')

    @app.route('/companies')
    def companies_page():
        """Companies listing page."""
        return render_template('companies.html')

    @app.route('/opportunities')
    def opportunities_page():
        """Opportunities listing page."""
        return render_template('opportunities.html')

    @app.route('/relationships')
    def relationships_page():
        """Relationships graph visualization page."""
        return render_template('relationships.html')
    
    # ==================== Summary & Reporting API ====================
    
    @app.route('/api/summary')
    def get_summary():
        """Get dashboard summary data."""
        summary = processing_service.get_dashboard_summary()
        return jsonify(summary)
    
    @app.route('/api/companies')
    def get_companies():
        """Get top companies."""
        limit = int(request.args.get('limit', 20))
        companies = processing_service.get_top_companies(limit=limit)
        return jsonify(companies)

    @app.route('/api/companies/<int:company_id>/signals')
    def get_company_signals(company_id):
        """Get detailed signal information for tooltip display."""
        with db_service.get_session() as session:
            signals = session.query(HiringSignal).filter_by(
                company_id=company_id
            ).order_by(
                desc(HiringSignal.confidence)
            ).all()

            return jsonify([{
                'type': s.signal_type,
                'confidence': round(s.confidence * 100, 1),
                'description': s.description,
                'detected_date': s.detected_date.isoformat()
            } for s in signals])

    @app.route('/api/companies/<int:company_id>/score-breakdown')
    def get_score_breakdown(company_id):
        """Get detailed score breakdown for tooltip display."""
        with db_service.get_session() as session:
            company = session.query(Company).get(company_id)
            if not company:
                return jsonify({'error': 'Company not found'}), 404

            weights = config.SCORING_WEIGHTS

            # Calculate individual components
            active_opps = session.query(Opportunity).filter_by(
                company_id=company_id,
                is_active=True
            ).count()

            job_score = min(active_opps * 10, 40) * weights['explicit_job_posting']

            recent_signals = session.query(HiringSignal).filter_by(
                company_id=company_id
            ).filter(
                HiringSignal.detected_date > datetime.now(timezone.utc) - timedelta(days=90)
            ).all()

            if recent_signals:
                avg_confidence = sum(s.confidence for s in recent_signals) / len(recent_signals)
                signal_score = avg_confidence * 100 * weights['hiring_signals']
            else:
                signal_score = 0

            has_funding = any(s.signal_type == 'funding' for s in recent_signals)
            has_expansion = any(s.signal_type == 'expansion' for s in recent_signals)
            growth_score = (50 if (has_funding or has_expansion) else 0) * weights['company_growth']

            activity_score = (100 if recent_signals else 0) * weights['recent_activity']

            return jsonify({
                'total_score': company.score,
                'job_postings': job_score,
                'hiring_signals': signal_score,
                'company_growth': growth_score,
                'recent_activity': activity_score,
                'weights': weights
            })

    @app.route('/api/opportunities')
    def get_opportunities():
        """Get active opportunities."""
        limit = int(request.args.get('limit', 50))
        opportunities = processing_service.get_active_opportunities(limit=limit)
        return jsonify(opportunities)

    @app.route('/api/graph')
    def get_graph_data():
        """Get graph database data for visualization."""
        from ..models.graph import GraphDatabase
        graph_db = GraphDatabase()

        nodes = []
        edges = []

        # Build nodes and edges from graph
        for node_id in graph_db.graph.nodes():
            node_data = graph_db.graph.nodes[node_id]
            node_type = node_data.get('type', 'unknown')

            # Determine color and shape based on type
            if node_type == 'company':
                color = '#3b82f6'  # blue
                shape = 'box'
                label = node_data.get('name', node_id)
            elif node_type == 'opportunity':
                color = '#10b981'  # green
                shape = 'diamond'
                label = node_data.get('title', node_id)[:30]  # truncate long titles
            elif node_type == 'signal':
                color = '#f59e0b'  # orange
                shape = 'triangle'
                signal_type = node_data.get('signal_type', 'signal')
                label = signal_type
            else:
                color = '#64748b'  # gray
                shape = 'dot'
                label = node_id

            nodes.append({
                'id': node_id,
                'label': label,
                'color': color,
                'shape': shape,
                'type': node_type
            })

        # Build edges
        for source, target, edge_data in graph_db.graph.edges(data=True):
            relation = edge_data.get('relation', 'connected')
            edges.append({
                'from': source,
                'to': target,
                'label': relation,
                'arrows': 'to'
            })

        # Get statistics
        stats = {
            'total_nodes': graph_db.graph.number_of_nodes(),
            'total_edges': graph_db.graph.number_of_edges(),
            'companies': sum(1 for n in graph_db.graph.nodes() if n.startswith('company:')),
            'opportunities': sum(1 for n in graph_db.graph.nodes() if n.startswith('opportunity:')),
            'signals': sum(1 for n in graph_db.graph.nodes() if n.startswith('signal:'))
        }

        # Get multi-signal companies
        multi_signal = graph_db.find_companies_with_multiple_signals(min_signals=2)

        return jsonify({
            'nodes': nodes,
            'edges': edges,
            'stats': stats,
            'multi_signal_companies': multi_signal
        })
    
    # ==================== Credentials Management API ====================
    
    @app.route('/api/credentials/status', methods=['GET'])
    def get_credentials_status():
        """Get credential configuration status (not the values)."""
        return jsonify({
            'tavily_configured': bool(getattr(config, 'TAVILY_API_KEY', None)),
            'brave_configured': bool(getattr(config, 'BRAVE_API_KEY', None)),
            'groq_configured': bool(config.GROQ_API_KEY),
            'database_configured': config.DATABASE_URL != 'sqlite:///roleradar.db',
            'secure_mode': config.is_secure_mode()
        })
    
    @app.route('/api/credentials/update', methods=['PUT'])
    def update_credentials():
        """Update API keys and database credentials."""
        try:
            data = request.get_json()
            
            # Validate at least one credential provided
            tavily_key = data.get('tavily_api_key', '').strip()
            brave_key = data.get('brave_api_key', '').strip()
            groq_key = data.get('groq_api_key', '').strip()
            database_url = data.get('database_url', '').strip()
            
            if not any([tavily_key, brave_key, groq_key, database_url]):
                return jsonify({'error': 'At least one credential must be provided'}), 400
            
            updated_fields = []
            
            # Update Tavily API Key
            if tavily_key:
                config.TAVILY_API_KEY = tavily_key
                if hasattr(config, '_secure_store') and config._secure_store:
                    config._secure_store.set("TAVILY_API_KEY", tavily_key)
                updated_fields.append('Tavily API Key')
                
            # Update Brave API Key
            if brave_key:
                config.BRAVE_API_KEY = brave_key
                if hasattr(config, '_secure_store') and config._secure_store:
                    config._secure_store.set("BRAVE_API_KEY", brave_key)
                updated_fields.append('Brave API Key')
            
            # Update Groq API Key
            if groq_key:
                config.GROQ_API_KEY = groq_key
                if hasattr(config, '_secure_store') and config._secure_store:
                    config._secure_store.set("GROQ_API_KEY", groq_key)
                updated_fields.append('Groq API Key')
            
            # Update Database URL
            if database_url:
                # Validate database URL format
                if not any(database_url.startswith(prefix) for prefix in ['postgresql://', 'sqlite:///', 'mysql://']):
                    return jsonify({'error': 'Invalid database URL. Must start with postgresql://, sqlite:///, or mysql://'}), 400
                
                config.DATABASE_URL = database_url
                if hasattr(config, '_secure_store') and config._secure_store:
                    config._secure_store.set("DATABASE_URL", database_url)
                updated_fields.append('Database URL')
            
            # Save to secure storage if available
            if hasattr(config, '_secure_store') and config._secure_store:
                config._secure_store.save()
            
            return jsonify({
                'success': True,
                'message': f'Updated: {", ".join(updated_fields)}',
                'updated_fields': updated_fields,
                'status': get_credentials_status().get_json()
            })
        except Exception as e:
            return jsonify({'error': str(e), 'message': 'Failed to update credentials'}), 500
    
    @app.route('/api/credentials/test', methods=['POST'])
    def test_credentials():
        """Test if API keys and database connection work."""
        try:
            results = {}
            
            # Test Search API (Tavily or Brave)
            if getattr(config, 'TAVILY_API_KEY', None):
                try:
                    tavily = TavilySearchService()
                    results['tavily'] = {
                        'status': 'valid',
                        'message': 'Tavily API key is configured and valid'
                    }
                except Exception as e:
                    results['tavily'] = {
                        'status': 'invalid',
                        'message': f'Tavily API error: {str(e)}'
                    }
            elif getattr(config, 'BRAVE_API_KEY', None):
                try:
                    brave = BraveSearchService()
                    results['brave'] = {
                        'status': 'valid',
                        'message': 'Brave API key is configured and valid'
                    }
                except Exception as e:
                    results['brave'] = {
                        'status': 'invalid',
                        'message': f'Brave API error: {str(e)}'
                    }
            else:
                results['tavily'] = {
                    'status': 'not_configured',
                    'message': 'No Search API key (Tavily or Brave) configured'
                }
            
            # Test Groq API
            if config.GROQ_API_KEY:
                try:
                    groq = GroqAnalysisService()
                    if groq.client:
                        results['groq'] = {
                            'status': 'valid',
                            'message': 'Groq API key is configured and valid'
                        }
                    else:
                        results['groq'] = {
                            'status': 'invalid',
                            'message': 'Groq client initialization failed'
                        }
                except Exception as e:
                    results['groq'] = {
                        'status': 'invalid',
                        'message': f'Groq API error: {str(e)}'
                    }
            else:
                results['groq'] = {
                    'status': 'not_configured',
                    'message': 'Groq API key not configured'
                }
            
            # Test Database Connection
            try:
                db_status = db_service.get_status()
                results['database'] = {
                    'status': 'valid' if db_status.get('status') == 'ready' else 'invalid',
                    'message': f"{db_status.get('type')} database is {db_status.get('status')}"
                }
            except Exception as e:
                results['database'] = {
                    'status': 'invalid',
                    'message': f'Database connection error: {str(e)}'
                }
            
            return jsonify({
                'success': True,
                'results': results
            })
        except Exception as e:
            return jsonify({'error': str(e), 'message': 'Failed to test credentials'}), 500
    
    # ==================== Configuration Management API ====================
    
    @app.route('/api/config/search-roles', methods=['GET'])
    def get_search_roles():
        """Get current search roles."""
        return jsonify({
            'roles': config.SEARCH_ROLES,
            'count': len(config.SEARCH_ROLES)
        })
    
    @app.route('/api/config/search-roles', methods=['PUT'])
    def update_search_roles():
        """Update search roles."""
        try:
            data = request.get_json()
            roles = data.get('roles', [])

            if not isinstance(roles, list):
                return jsonify({'error': 'roles must be a list'}), 400

            if len(roles) == 0:
                return jsonify({'error': 'at least one role is required'}), 400

            # Update config (also saves to secure store if available)
            config.update_search_roles(roles)

            # Also save to database for persistence
            db_service.set_config_value("SEARCH_ROLES", roles, "User-configured search roles")

            return jsonify({
                'success': True,
                'message': f'Updated {len(roles)} search roles',
                'roles': config.SEARCH_ROLES
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/config/schedule', methods=['GET'])
    def get_schedule():
        """Get current schedule times."""
        return jsonify({
            'schedule_times': config.SCHEDULE_TIMES,
            'timezone': config.TIMEZONE
        })
    
    @app.route('/api/config/schedule', methods=['PUT'])
    def update_schedule():
        """Update schedule times."""
        try:
            data = request.get_json()
            times = data.get('schedule_times', [])

            if not isinstance(times, list):
                return jsonify({'error': 'schedule_times must be a list'}), 400

            if len(times) == 0:
                return jsonify({'error': 'at least one schedule time is required'}), 400

            # Validate time format (HH:MM)
            import re
            time_pattern = re.compile(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$')
            for time_str in times:
                if not time_pattern.match(time_str):
                    return jsonify({'error': f'Invalid time format: {time_str}. Use HH:MM'}), 400

            # Update config (also saves to secure store if available)
            config.update_schedule_times(times)

            # Also save to database for persistence
            db_service.set_config_value("SCHEDULE_TIMES", times, "User-configured schedule times")

            return jsonify({
                'success': True,
                'message': f'Updated schedule to {len(times)} times',
                'schedule_times': config.SCHEDULE_TIMES
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/config/weights', methods=['GET'])
    def get_weights():
        """Get current scoring weights."""
        return jsonify(config.SCORING_WEIGHTS)
    
    @app.route('/api/config/weights', methods=['PUT'])
    def update_weights():
        """Update scoring weights."""
        try:
            data = request.get_json()
            weights = data.get('weights', {})

            if not isinstance(weights, dict):
                return jsonify({'error': 'weights must be a dictionary'}), 400

            # Validate weights sum to 1.0
            total = sum(weights.values())
            if abs(total - 1.0) > 0.01:
                return jsonify({'error': f'Weights must sum to 1.0, got {total}'}), 400

            # Update config
            config.SCORING_WEIGHTS = weights
            if hasattr(config, '_secure_store') and config._secure_store:
                config._secure_store.set("SCORING_WEIGHTS", weights)
                config._secure_store.save()

            # Also save to database for persistence
            db_service.set_config_value("SCORING_WEIGHTS", weights, "User-configured scoring weights")

            return jsonify({
                'success': True,
                'message': 'Updated scoring weights',
                'weights': config.SCORING_WEIGHTS
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/config/extraction-prompts', methods=['GET'])
    def get_extraction_prompts():
        """Get current data extraction prompts."""
        return jsonify(get_prompt_templates())
    
    @app.route('/api/config/extraction-prompts', methods=['PUT'])
    def update_extraction_prompts():
        """Update data extraction prompts."""
        try:
            data = request.get_json()

            prompts = {
                'ENTITY_EXTRACTION_PROMPT': data.get('entity_extraction'),
                'HIRING_SIGNALS_PROMPT': data.get('hiring_signals'),
                'GROWTH_DETECTION_PROMPT': data.get('growth_detection')
            }

            for key, value in prompts.items():
                if value:
                    setattr(config, key, value)
                    if hasattr(config, '_secure_store') and config._secure_store:
                        config._secure_store.set(key, value)
                    # Also save to database for persistence
                    db_service.set_config_value(key, value, f"User-configured {key}")

            if hasattr(config, '_secure_store') and config._secure_store:
                config._secure_store.save()

            return jsonify({
                'success': True,
                'message': 'Updated extraction prompts',
                'prompts': get_prompt_templates()
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # ==================== Search Control API ====================
    
    @app.route('/api/search/manual', methods=['POST'])
    def trigger_manual_search():
        """Trigger a manual search immediately."""
        try:
            # Get optional query parameter
            query = request.args.get('query')
            
            search_service = get_search_service()
            if query:
                results = search_service.search(query)
                message = f'Searched for: {query}'
            else:
                results = search_service.daily_search()
                message = 'Ran full daily search'
            
            total_results = sum(len(r) for r in results.values()) if isinstance(results, dict) else len(results)
            
            return jsonify({
                'success': True,
                'message': message,
                'results_found': total_results,
                'search_data': results
            })
        except Exception as e:
            return jsonify({'error': str(e), 'message': 'Search failed'}), 500
    
    @app.route('/api/search/process', methods=['GET', 'POST'])
    def trigger_processing():
        """Trigger processing with streaming progress updates."""
        import json as json_module
        
        # Capture request context before entering generator
        limit = request.args.get('limit', 100, type=int)
        
        def generate():
            try:
                processor = ProcessingService()
                results = processor.tavily.get_unprocessed_results(limit=limit)
                
                total = len(results)
                yield f"data: {json_module.dumps({'type': 'start', 'total': total})}\n\n"
                
                processed = 0
                for result in results:
                    try:
                        processor._process_single_result(result)
                        processor.tavily.mark_as_processed(result.id)
                        processed += 1
                        
                        yield f"data: {json_module.dumps({'type': 'progress', 'processed': processed, 'total': total, 'current': {'id': result.id, 'title': result.title[:80] if result.title else 'Untitled'}})}\n\n"
                    except Exception as e:
                        yield f"data: {json_module.dumps({'type': 'error', 'processed': processed, 'total': total, 'error': str(e)[:200], 'result_id': result.id})}\n\n"
                
                yield f"data: {json_module.dumps({'type': 'complete', 'processed': processed, 'total': total})}\n\n"
            except Exception as e:
                yield f"data: {json_module.dumps({'type': 'fatal_error', 'error': str(e)})}\n\n"
        
        return app.response_class(
            generate(),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no'
            }
        )
    
    @app.route('/api/search/status', methods=['GET'])
    def get_search_status():
        """Get status of current searches."""
        with db_service.get_session() as session:
            from ..models import SearchResult
            
            # Get last search time
            last_result = session.query(SearchResult).order_by(
                SearchResult.retrieved_date.desc()
            ).first()
            last_search = last_result.retrieved_date.isoformat() if last_result else None
            
            # Count unprocessed results
            pending = session.query(SearchResult).filter_by(processed=False).count()
            
            return jsonify({
                'last_search': last_search,
                'pending_processing': pending,
                'active_roles': len(config.SEARCH_ROLES),
                'schedule_times': config.SCHEDULE_TIMES
            })
    
    # ==================== System Status API ====================
    
    @app.route('/api/system/status', methods=['GET'])
    def get_system_status():
        """Get system status."""
        db_status = db_service.get_status()
        return jsonify({
            'database': db_status,
            'config_secure': config.is_secure_mode(),
            'search_roles': len(config.SEARCH_ROLES),
            'schedule_times': len(config.SCHEDULE_TIMES)
        })
    
    @app.route('/api/system/health', methods=['GET'])
    def get_health():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'version': '2.0.0',
            'features': ['search', 'processing', 'admin']
        })

    # ==================== API Usage Tracking ====================

    @app.route('/api/usage/summary', methods=['GET'])
    def get_api_usage_summary():
        """Get API usage summary for the last N days."""
        try:
            from ..services.api_tracker import APITracker

            days = int(request.args.get('days', 7))
            summary = APITracker.get_usage_summary(days=days)

            return jsonify(summary)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/usage/hourly', methods=['GET'])
    def get_api_usage_hourly():
        """Get hourly API usage breakdown."""
        try:
            from ..services.api_tracker import APITracker

            api_name = request.args.get('api')
            days = int(request.args.get('days', 7))
            hourly = APITracker.get_hourly_breakdown(api_name=api_name, days=days)

            return jsonify({'hourly': hourly})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/usage/top-queries', methods=['GET'])
    def get_api_top_queries():
        """Get the most frequent API queries."""
        try:
            from ..services.api_tracker import APITracker

            api_name = request.args.get('api')
            days = int(request.args.get('days', 7))
            limit = int(request.args.get('limit', 10))
            queries = APITracker.get_top_queries(api_name=api_name, days=days, limit=limit)

            return jsonify({'top_queries': queries})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/usage/errors', methods=['GET'])
    def get_api_errors():
        """Get API error summary."""
        try:
            from ..services.api_tracker import APITracker

            api_name = request.args.get('api')
            days = int(request.args.get('days', 7))
            errors = APITracker.get_error_summary(api_name=api_name, days=days)

            return jsonify({'errors': errors})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/usage/daily', methods=['GET'])
    def get_api_daily():
        """Get detailed stats for a specific day."""
        try:
            from ..services.api_tracker import APITracker

            date_str = request.args.get('date')
            stats = APITracker.get_daily_stats(date_str=date_str)

            return jsonify(stats)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # ==================== Search Results Transparency API ====================
    
    @app.route('/api/search-results', methods=['GET'])
    def get_search_results():
        """Get search results with extraction details for transparency."""
        with db_service.get_session() as session:
            from ..models import SearchResult
            import json
            
            limit = int(request.args.get('limit', 50))
            processed_only = request.args.get('processed', 'false').lower() == 'true'
            query_filter = request.args.get('query')
            
            query = session.query(SearchResult)
            
            if processed_only:
                query = query.filter_by(processed=True)
            
            if query_filter:
                query = query.filter(SearchResult.query.ilike(f'%{query_filter}%'))
            
            results = query.order_by(
                SearchResult.retrieved_date.desc()
            ).limit(limit).all()
            
            output = []
            for r in results:
                keywords = []
                if r.extracted_keywords:
                    try:
                        keywords = json.loads(r.extracted_keywords)
                    except:
                        pass
                
                output.append({
                    'id': r.id,
                    'query': r.query,
                    'title': r.title,
                    'url': r.url,
                    'content_preview': r.content[:200] + '...' if r.content and len(r.content) > 200 else r.content,
                    'score': r.score,
                    'retrieved_date': r.retrieved_date.isoformat() if r.retrieved_date else None,
                    'processed': r.processed,
                    'processed_date': r.processed_date.isoformat() if r.processed_date else None,
                    'extraction': {
                        'company': r.extracted_company,
                        'job_title': r.extracted_job_title,
                        'role_type': r.extracted_role_type,
                        'location': r.extracted_location,
                        'keywords': keywords
                    },
                    'signal': {
                        'detected': r.detected_signal,
                        'type': r.signal_type,
                        'confidence': r.signal_confidence,
                        'description': r.signal_description
                    },
                    'error': r.processing_error
                })
            
            return jsonify(output)
    
    @app.route('/api/search-result/<int:result_id>', methods=['GET'])
    def get_search_result_detail(result_id):
        """Get detailed view of a single search result."""
        with db_service.get_session() as session:
            from ..models import SearchResult
            import json
            
            result = session.query(SearchResult).get(result_id)
            if not result:
                return jsonify({'error': 'Result not found'}), 404
            
            keywords = []
            if result.extracted_keywords:
                try:
                    keywords = json.loads(result.extracted_keywords)
                except:
                    pass
            
            return jsonify({
                'id': result.id,
                'query': result.query,
                'title': result.title,
                'url': result.url,
                'content': result.content,
                'score': result.score,
                'published_date': result.published_date,
                'retrieved_date': result.retrieved_date.isoformat() if result.retrieved_date else None,
                'processed': result.processed,
                'processed_date': result.processed_date.isoformat() if result.processed_date else None,
                'extraction': {
                    'company': result.extracted_company,
                    'job_title': result.extracted_job_title,
                    'role_type': result.extracted_role_type,
                    'location': result.extracted_location,
                    'keywords': keywords
                },
                'signal': {
                    'detected': result.detected_signal,
                    'type': result.signal_type,
                    'confidence': result.signal_confidence,
                    'description': result.signal_description
                },
                'error': result.processing_error
            })
    
    @app.route('/api/search-queries', methods=['GET'])
    def get_search_queries():
        """Get list of recent search queries with stats."""
        with db_service.get_session() as session:
            from ..models import SearchResult
            from sqlalchemy import func, desc
            
            # Get unique queries with counts and dates
            queries = session.query(
                SearchResult.query,
                func.count(SearchResult.id).label('result_count'),
                func.max(SearchResult.retrieved_date).label('last_search'),
                func.sum(func.cast(SearchResult.processed, Integer)).label('processed_count')
            ).group_by(
                SearchResult.query
            ).order_by(
                desc('last_search')
            ).limit(50).all()
            
            return jsonify([
                {
                    'query': q.query,
                    'result_count': q.result_count,
                    'processed_count': q.processed_count,
                    'last_search': q.last_search.isoformat() if q.last_search else None
                }
                for q in queries
            ])

    @app.route('/api/data/clear', methods=['POST'])
    def clear_all_data():
        """Clear all companies, opportunities, signals, and search results."""
        try:
            from ..models import Company, Opportunity, HiringSignal, SearchResult

            with db_service.get_session() as session:
                # Count before deletion
                company_count = session.query(Company).count()
                opportunity_count = session.query(Opportunity).count()
                signal_count = session.query(HiringSignal).count()
                result_count = session.query(SearchResult).count()

                # Delete in order of dependencies
                session.query(HiringSignal).delete()
                session.query(Opportunity).delete()
                session.query(SearchResult).delete()
                session.query(Company).delete()
                session.commit()

                return jsonify({
                    'success': True,
                    'message': 'All data cleared successfully',
                    'deleted': {
                        'companies': company_count,
                        'opportunities': opportunity_count,
                        'signals': signal_count,
                        'search_results': result_count
                    }
                })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/data/delete-company/<int:company_id>', methods=['DELETE'])
    def delete_company(company_id):
        """Delete a specific company and its related data."""
        try:
            from ..models import Company, Opportunity, HiringSignal

            with db_service.get_session() as session:
                company = session.query(Company).get(company_id)
                if not company:
                    return jsonify({'error': 'Company not found'}), 404

                company_name = company.name

                # Delete related opportunities and signals
                session.query(HiringSignal).filter_by(company_id=company_id).delete()
                session.query(Opportunity).filter_by(company_id=company_id).delete()
                session.delete(company)
                session.commit()

                return jsonify({
                    'success': True,
                    'message': f'Deleted company: {company_name}'
                })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(
        host=config.FLASK_HOST,
        port=config.FLASK_PORT,
        debug=False
    )
