from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_link = request.form['video_link']
    yt = YouTube(video_link)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_stream.download(filename='audio')
    convert_to_mp3('audio.mp4', 'audio.mp3')
    os.remove('audio.mp4')
    return send_file('audio.mp3', as_attachment=True)

def convert_to_mp3(input_file, output_file):
    import ffmpeg
    stream = ffmpeg.input(input_file)
    stream = ffmpeg.output(stream, output_file)
    ffmpeg.run(stream)

if __name__ == '__main__':
    app.run(debug=True)
