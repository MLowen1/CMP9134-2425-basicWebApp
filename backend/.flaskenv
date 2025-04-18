# Environment variables for Flask

# Points to the file (main.py) and the app instance or factory (create_app function)
# Use the factory pattern: module:factory_function()
FLASK_APP=main:create_app()

# Set the development environment
FLASK_ENV=development
# Enable debug mode (optional, useful for development)
FLASK_DEBUG=1

# Database URL (example using SQLite in instance folder)
# Ensure your config.py uses this or provides a default
# DATABASE_URL=sqlite:///instance/dev.db