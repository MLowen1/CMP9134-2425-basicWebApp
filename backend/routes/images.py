from flask import Blueprint, request, jsonify
# Use relative import
from ..extensions import ov_client

images_bp = Blueprint('images', __name__)

@images_bp.route('/search', methods=['GET'])
def search_images():
    """Route for searching images using Openverse, with optional filters."""
    query = request.args.get('q')
    license = request.args.get('license')
    orientation = request.args.get('orientation')
    # Use page_size for the API call, default to 20 if not provided or 0
    page_size = request.args.get('imageCount', type=int) or 20
    image_size = request.args.get('imageSize')
    # Remove image_type and image_sort
    image_color = request.args.get('imageColor')
    image_category = request.args.get('imageCategory')

    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    try:
        # Only pass supported params to OpenverseClient
        ov_params = {
            'query': query,
            'page_size': page_size,
        }
        if license:
            ov_params['license_type'] = license
        # Remove imageType and imageSort mapping to Openverse API params
        # Fetch results from Openverse
        results = ov_client.search_images(**ov_params)
        if isinstance(results, dict) and 'error' in results:
            return jsonify(results), 500

        images = results.get('results', [])
        # Orientation filter
        if orientation:
            if orientation == 'landscape':
                images = [img for img in images if img.get('width', 0) > img.get('height', 0)]
            elif orientation == 'portrait':
                images = [img for img in images if img.get('height', 0) > img.get('width', 0)]
            elif orientation == 'square':
                images = [img for img in images if img.get('width', 0) == img.get('height', 0)]
        # Image size filter (simple example: based on width)
        if image_size:
            if image_size == 'small':
                images = [img for img in images if img.get('width', 0) < 500]
            elif image_size == 'medium':
                images = [img for img in images if 500 <= img.get('width', 0) < 1500]
            elif image_size == 'large':
                images = [img for img in images if 1500 <= img.get('width', 0) < 3000]
            elif image_size == 'xlarge':
                images = [img for img in images if img.get('width', 0) >= 3000]
        # Remove the Python-side image_type filter!
        # Image color filter (example: based on color field if available)
        if image_color:
            images = [img for img in images if image_color.lower() in (img.get('color', '') or '').lower()]
        # Image category filter (example: based on tags or category field)
        if image_category:
            def tag_names(img):
                tags = img.get('tags', [])
                return [t['name'] if isinstance(t, dict) and 'name' in t else str(t) for t in tags]
            images = [
                img for img in images
                if image_category.lower() in (
                    ','.join(tag_names(img)) + ',' + str(img.get('category', ''))
                ).lower()
            ]
        # Remove Python-side image_sort filter
        # Limit to image_count if specified
        if page_size:
            images = images[:page_size]
        return jsonify({**results, 'results': images})

    except TypeError as te:
        # Catch TypeError specifically for incorrect arguments
        # This error now indicates that the combination of positional and keyword arguments is incorrect.
        print(f"TypeError during image search (check OpenverseClient parameters): {str(te)}")
        return jsonify({"error": f"Backend configuration error: The way parameters are passed to the Openverse API client is incorrect. Please consult the client library's documentation. Details: {str(te)}"}), 500
    except Exception as e:
        # Catch any other unexpected errors
        print(f"Error during image search: {str(e)}")
        # Return a generic server error message
        return jsonify({"error": "An unexpected error occurred during image search"}), 500

# Add other image-related routes if needed
