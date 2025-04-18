# File: backend/.flaskenv
# Use this setting for running 'flask' from the directory *above* 'backend'
FLASK_APP=backend.main:create_app()
FLASK_DEBUG=1
# Remove the line below if it exists
# FLASK_APP=main:create_app()