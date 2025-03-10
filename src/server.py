import os
from flask import Flask, request, jsonify
from src.upload.youtube import dowload_youtube, get_last_livestream_data
from src.upload.manipulate_file import compress_audio, generate_id3_tags
from src.upload.send_file import check_if_file_on_server
from utils import extract_date, writable_path

app = Flask(__name__)

@app.route('/post', methods=['POST'])
def handle_post():
    data = request.get_json()  # Get JSON data from the request
    response = {
        "message": "Data received",
        "received_data": data
    }
    return jsonify(response), 200  # Return a JSON response with HTTP status code 200


@app.route('/get_latest_streams_data/<int:limit>', methods=['GET'])
def handle_get_limit(limit):
    latest = get_last_livestream_data(limit=limit)
    return jsonify({"data": latest}), 200

@app.route('/download_vide/<string:URL>', methods=['GET'])
def handle_download_video(URL):
    path = dowload_youtube(URL)
    return jsonify({"path": path}), 200

@app.route('/compress_audio/<string:file_name>', methods=['GET'])
def handle_compress_audio(file_name):
    path = compress_audio(file_name)
    return jsonify({"path": path}), 200

@app.route('/add_tag/<string:file_name>', methods=['POST'])
def handle_add_tags(file_name):
    # Get data from request JSON body
    data = request.get_json()
    
    # Check if all required fields are present
    required_fields = ['prediger', 'predigt_titel', 'datum', 'year']
    if not all(field in data for field in required_fields):
        return jsonify({
            "error": "Missing required fields",
            "required": required_fields
        }), 400
    
    try:
        generate_id3_tags(
            file_name,
            data['prediger'],
            data['predigt_titel'],
            data['datum'],
            data['year']
        )
        return jsonify({"message": "Tags added successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/get_stored_files/<int:limit>', methods=['GET'])
def handle_get_stored_files(limit):
    try:
        if not os.path.exists(writable_path('stored')):
            os.mkdir(writable_path('stored'))
        stored_files = os.listdir(writable_path('stored/'))
        
        try:
            filtered_files = sorted(stored_files, key=extract_date, reverse=True)[:limit]
        except Exception as e:
            return jsonify({"error": f"Error sorting files: {str(e)}"}), 500
        
        files_status = []
        for file_name in filtered_files:
            files_status.append({
                "name": file_name,
                "on_server": check_if_file_on_server(file_name),
                "path": writable_path(f'stored/{file_name}')
            })
        
        return jsonify({
            "files": files_status,
            "total_count": len(filtered_files)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#@app.route('/send_file/<string:file_name>', methods=['POST'])
#def handle_send_file(file_name):
#    try:
#        file_path = writable_path(f'stored/{file_name}')
#        if not os.path.exists(file_path):
#            return jsonify({"error": "File not found"}), 404
#            
#        success = upload_file_to_server(file_path)
#        if success:
#            return jsonify({"message": "File uploaded successfully"}), 200
#        else:
#            return jsonify({"error": "Upload failed"}), 500
#            
#    except Exception as e:
#        return jsonify({"error": str(e)}), 500
#
#@app.route('/send_file/<string:file_name>', methods=['POST'])
#def handle_send_file(file_name):
#    try:
#        file_path = writable_path(f'stored/{file_name}')
#        if not os.path.exists(file_path):
#            return jsonify({"error": "File not found"}), 404
#            
#        success = upload_file_to_server(file_path)
#        if success:
#            return jsonify({"message": "File uploaded successfully"}), 200
#        else:
#            return jsonify({"error": "Upload failed"}), 500
#            
#    except Exception as e:
#        return jsonify({"error": str(e)}), 500
#
#@app.route('/change_title/<string:file_name>', methods=['POST'])
#def handle_change_title(file_name):
#    try:
#        data = request.get_json()
#        if 'title' not in data:
#            return jsonify({"error": "Missing title in request"}), 400
#            
#        file_path = writable_path(f'stored/{file_name}')
#        if not os.path.exists(file_path):
#            return jsonify({"error": "File not found"}), 404
#            
#        change_predigt_title(file_path, data['title'])
#        return jsonify({"message": "Title updated successfully"}), 200
#            
#    except Exception as e:
#        return jsonify({"error": str(e)}), 500
#
#@app.route('/change_prediger/<string:file_name>', methods=['POST'])
#def handle_change_prediger(file_name):
#    try:
#        data = request.get_json()
#        if 'prediger' not in data:
#            return jsonify({"error": "Missing prediger in request"}), 400
#            
#        file_path = writable_path(f'stored/{file_name}')
#        if not os.path.exists(file_path):
#            return jsonify({"error": "File not found"}), 404
#            
#        change_prediger(file_path, data['prediger'])
#        return jsonify({"message": "Prediger updated successfully"}), 200
#            
#    except Exception as e:
#        return jsonify({"error": str(e)}), 500