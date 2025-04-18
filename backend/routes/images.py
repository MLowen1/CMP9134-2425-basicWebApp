from flask import Blueprint, jsonify, request
# Import the client instance from extensions
from backend.extensions import ov_client

images_bp = Blueprint('images', __name__)

# Example route - adapt as needed
@images_bp.route('/search', methods=['GET'])
def search_images():
    """Route for searching images using Openverse."""
    query = request.args.get('q') # Get query param
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    try:
        # Use the imported ov_client instance
        results = ov_client.search_images(query)
        # Check if the client returned an error dictionary
        if isinstance(results, dict) and 'error' in results:
             # Propagate the error from the client
             return jsonify(results), 500 # Or appropriate status code

        # Assuming results is the dictionary returned by the client on success
        return jsonify(results)

    except Exception as e:
        # Log the exception for debugging
        print(f"Error during image search: {str(e)}")
        return jsonify({"error": "An unexpected error occurred during image search"}), 500

# Add other image-related routes if needed
