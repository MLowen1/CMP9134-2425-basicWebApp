from flask import Blueprint, request, jsonify
from ..extensions import ov_client

audio_bp = Blueprint('audio', __name__)

@audio_bp.route('/search', methods=['GET'])
def search_audio():
    """Route for searching audio using Openverse, with optional filters."""
    query = request.args.get('q')
    license = request.args.get('license')
    audio_count = request.args.get('audioCount', type=int) or 20
    audio_duration = request.args.get('audioDuration')
    audio_category = request.args.get('audioCategory')
    audio_genre = request.args.get('audioGenre')

    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    try:
        ov_params = {
            'query': query,
            'page_size': audio_count,
        }
        if license:
            ov_params['license_type'] = license
        # Add more mappings as needed for Openverse audio API
        results = ov_client.search_audio(**ov_params)
        if isinstance(results, dict) and 'error' in results:
            return jsonify(results), 500
        audios = results.get('results', [])
        # Filter by duration (example logic)
        if audio_duration:
            if audio_duration == 'short':
                audios = [a for a in audios if a.get('duration', 0) < 60]
            elif audio_duration == 'medium':
                audios = [a for a in audios if 60 <= a.get('duration', 0) <= 300]
            elif audio_duration == 'long':
                audios = [a for a in audios if a.get('duration', 0) > 300]
        # Filter by category
        if audio_category:
            audios = [a for a in audios if audio_category.lower() in (a.get('category', '') or '').lower()]
        # Filter by genre
        if audio_genre:
            audios = [a for a in audios if audio_genre.lower() in (a.get('genre', '') or '').lower()]
        if audio_count:
            audios = audios[:audio_count]
        return jsonify({**results, 'results': audios})
    except Exception as e:
        print(f"Error during audio search: {str(e)}")
        return jsonify({"error": "An unexpected error occurred during audio search"}), 500
