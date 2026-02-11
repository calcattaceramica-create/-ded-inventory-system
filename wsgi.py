"""WSGI entry point for production deployment"""
import os
import sys

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(__file__))

# Set production environment
os.environ['FLASK_ENV'] = 'production'

# Import the app
from run import app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

