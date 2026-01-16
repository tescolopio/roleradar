"""Flask dashboard for RoleRadar."""

from flask import Flask, render_template, jsonify, request
from ..services import ProcessingService
from ..database import db_service
from ..config import config


def create_app():
    """Create Flask application."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config.FLASK_SECRET_KEY
    
    # Initialize database tables
    db_service.create_tables()
    
    processing_service = ProcessingService()
    
    @app.route('/')
    def index():
        """Dashboard home page."""
        return render_template('index.html')
    
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
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(
        host=config.FLASK_HOST,
        port=config.FLASK_PORT,
        debug=True
    )
