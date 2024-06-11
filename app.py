from flask import Flask, request, jsonify, send_file
import os
import gdown
import requests
from moviepy.editor import VideoFileClip, CompositeVideoClip

app = Flask(__name__)

@app.route('/overlay_videos', methods=['POST'])
def overlay_videos():
    data = request.json
    url_1 = data['url_1']
    url_2 = data['url_2']
    
    video_1_path = "video1.mov"
    video_2_path = "video2.mp4"
    
    # Download the first video
    gdown.download(url_1, video_1_path, quiet=False)

    # Download the second video
    response_2 = requests.get(url_2)
    with open(video_2_path, 'wb') as f:
        f.write(response_2.content)
    
    # Load the videos
    main_clip = VideoFileClip(video_1_path)
    overlay_clip = VideoFileClip(video_2_path).resize(width=250)  # Resize overlay video
    
    # Position the overlay clip
    overlay_clip = overlay_clip.set_position((10, 10))  # Set position (x, y)
    
    # Create the composite video
    final_clip = CompositeVideoClip([main_clip, overlay_clip])
    
    # Output file path
    output_path = "output.mp4"
    
    # Write the result to a file
    final_clip.write_videofile(output_path, codec="libx264")

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
