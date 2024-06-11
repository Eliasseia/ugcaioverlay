from flask import Flask, request, send_file, jsonify
import os
import gdown
import requests
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World! The Flask app is running."

@app.route('/overlay_videos', methods=['POST'])
def overlay_videos():
    try:
        data = request.json
        url_1 = data['url_1']
        url_2 = data['url_2']

        video_1_path = "video1.mov"
        video_2_path = "video2.mp4"
        output_path = "output.mp4"

        app.logger.info("Downloading video 1 from URL: %s", url_1)
        gdown.download(url_1, video_1_path, quiet=False)

        app.logger.info("Downloading video 2 from URL: %s", url_2)
        response_2 = requests.get(url_2)
        with open(video_2_path, 'wb') as f:
            f.write(response_2.content)

        app.logger.info("Overlaying videos using ffmpeg")
        command = [
            'ffmpeg', '-i', video_1_path, '-i', video_2_path,
            '-filter_complex', '[1:v]scale=250:-1[ovr];[0:v][ovr]overlay=10:10',
            '-codec:a', 'copy', output_path
        ]
        subprocess.run(command, check=True)

        app.logger.info("Overlay complete, sending file: %s", output_path)
        return send_file(output_path, as_attachment=True)
    except Exception as e:
        app.logger.error("Error processing video: %s", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

