"""WSGI entry point for production deployment"""
import os

# Set production environment before importing app
os.environ['FLASK_ENV'] = 'production'

# Import the Flask app instance from run.py
from run import app

# This is what gunicorn will use
application = app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

