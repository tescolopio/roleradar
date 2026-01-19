"""Flask dashboard for RoleRadar."""

from flask import Flask, render_template, jsonify, request
from ..services import ProcessingService, TavilySearchService, GroqAnalysisService
from ..database import db_service
from ..config import config
import json


def create_app():
    """Create Flask application."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config.FLASK_SECRET_KEY
    
    # Initialize database tables
    db_service.create_tables()
    
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
    
    @app.route('/api/opportunities')
    def get_opportunities():
        """Get active opportunities."""
        limit = int(request.args.get('limit', 50))
        opportunities = processing_service.get_active_opportunities(limit=limit)
        return jsonify(opportunities)
    
    # ==================== Credentials Management API ====================
    
    @app.route('/api/credentials/status', methods=['GET'])
    def get_credentials_status():
        """Get credential configuration status (not the values)."""
        return jsonify({
            'tavily_configured': bool(config.TAVILY_API_KEY),
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
            groq_key = data.get('groq_api_key', '').strip()
            database_url = data.get('database_url', '').strip()
            
            if not any([tavily_key, groq_key, database_url]):
                return jsonify({'error': 'At least one credential must be provided'}), 400
            
            updated_fields = []
            
            # Update Tavily API Key
            if tavily_key:
                config.TAVILY_API_KEY = tavily_key
                if hasattr(config, '_secure_store') and config._secure_store:
                    config._secure_store.set("TAVILY_API_KEY", tavily_key)
                updated_fields.append('Tavily API Key')
            
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
            
            # Test Tavily API
            if config.TAVILY_API_KEY:
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
            else:
                results['tavily'] = {
                    'status': 'not_configured',
                    'message': 'Tavily API key not configured'
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
            
            # Update config
            config.update_search_roles(roles)
            
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
            
            # Update config
            config.update_schedule_times(times)
            
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
        return jsonify({
            'entity_extraction': getattr(config, 'ENTITY_EXTRACTION_PROMPT', 'default'),
            'hiring_signals': getattr(config, 'HIRING_SIGNALS_PROMPT', 'default'),
            'growth_detection': getattr(config, 'GROWTH_DETECTION_PROMPT', 'default')
        })
    
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
            
            if hasattr(config, '_secure_store') and config._secure_store:
                config._secure_store.save()
            
            return jsonify({
                'success': True,
                'message': 'Updated extraction prompts',
                'prompts': get_extraction_prompts().get_json()
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
            
            tavily = TavilySearchService()
            if query:
                results = tavily.search(query)
                message = f'Searched for: {query}'
            else:
                results = tavily.daily_search()
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
    
    @app.route('/api/search/process', methods=['POST'])
    def trigger_processing():
        """Trigger processing of unprocessed results."""
        try:
            limit = request.args.get('limit', 100, type=int)
            
            processor = ProcessingService()
            processed_count = processor.process_unprocessed_results(limit=limit)
            
            return jsonify({
                'success': True,
                'message': f'Processed results',
                'processed_count': processed_count
            })
        except Exception as e:
            return jsonify({'error': str(e), 'message': 'Processing failed'}), 500
    
    @app.route('/api/search/status', methods=['GET'])
    def get_search_status():
        """Get status of current searches."""
        return jsonify({
            'last_search': None,  # TODO: Track last search time
            'pending_processing': 0,  # TODO: Count unprocessed results
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
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(
        host=config.FLASK_HOST,
        port=config.FLASK_PORT,
        debug=False
    )
