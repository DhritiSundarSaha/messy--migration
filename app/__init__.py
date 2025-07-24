from flask import Flask, jsonify, Response

def create_app() -> Flask:
    """
    Creates and configures an instance of the Flask application.
    This is the application factory.
    """
    app = Flask(__name__)
    
    # Load configuration from a file.
    # Using from_pyfile allows you to easily change the config without touching the code.
    app.config.from_pyfile('../config.py')

    # Initialize database connection handling with the app
    from . import db
    db.init_app(app)

    # --- Centralized Error Handlers ---
    # Registering handlers makes error responses consistent and DRY.
    
    @app.errorhandler(400)
    def bad_request(error) -> tuple[Response, int]:
        """Handler for 400 Bad Request errors."""
        return jsonify({
            "status": "error", 
            "message": getattr(error, 'description', "The browser (or proxy) sent a request that this server could not understand.")
        }), 400

    @app.errorhandler(401)
    def unauthorized(error) -> tuple[Response, int]:
        """Handler for 401 Unauthorized errors."""
        return jsonify({
            "status": "error", 
            "message": getattr(error, 'description', "Authentication is required and has failed or has not yet been provided.")
        }), 401

    @app.errorhandler(404)
    def not_found(error) -> tuple[Response, int]:
        """Handler for 404 Not Found errors."""
        return jsonify({
            "status": "error", 
            "message": getattr(error, 'description', "The requested resource was not found on the server.")
        }), 404
        
    @app.errorhandler(409)
    def conflict(error) -> tuple[Response, int]:
        """Handler for 409 Conflict errors."""
        return jsonify({
            "status": "error", 
            "message": getattr(error, 'description', "A conflict occurred with the current state of the resource.")
        }), 409

    @app.errorhandler(500)
    def internal_server_error(error) -> tuple[Response, int]:
        """A catch-all handler for 500 Internal Server Error."""
        return jsonify({
            "status": "error", 
            "message": "An internal server error occurred."
        }), 500

    # Register the routes blueprint
    from . import routes
    app.register_blueprint(routes.bp)

    return app