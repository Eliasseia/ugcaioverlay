from flask import Flask, request, send_file
import os
from moviepy.editor import VideoFileClip, CompositeVideoClip

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return 'Video overlay service is running.'

@app.route('/overlay', methods=['POST'])
def overlay_videos():
    video1 = request.files.get('video1')
    video2 = request.files.get('video2')

    if not video1 or not video2:
        return 'Both video1 and video2 files are required', 400

    video1_path = os.path.join(UPLOAD_FOLDER, video1.filename)
    video2_path = os.path.join(UPLOAD_FOLDER, video2.filename)
    output_path = os.path.join(OUTPUT_FOLDER, 'output.mp4')

    video1.save(video1_path)
    video2.save(video2_path)

    try:
        clip1 = VideoFileClip(video1_path)
        clip2 = VideoFileClip(video2_path).set_position(("center", "center")).set_duration(clip1.duration)

        final_clip = CompositeVideoClip([clip1, clip2])
        final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

        return send_file(output_path, as_attachment=True, download_name='output.mp4')
    finally:
        os.remove(video1_path)
        os.remove(video2_path)
        if os.path.exists(output_path):
            os.remove(output_path)

if __name__ == '__main__':
    app.run(debug=True)


