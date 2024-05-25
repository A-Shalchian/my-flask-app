from flask import Flask, render_template, request, send_from_directory, redirect, url_for, session
from pytube import YouTube
import os


#  This application will download youtube videos with the use of urls, I was inspired to make this because for so long in my country I had to download yt videos
# due to the restrictions that Iran had with using youtube. 
app = Flask(__name__)
app.secret_key = os.urandom(24).hex()  
DOWNLOAD_FOLDER = 'static/downloads'

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        if url:
            try:
                session['video_url'] = url
                yt = YouTube(url)
                return redirect(url_for('confirm_download'))
            except Exception as e:
                return render_template('index.html', error=str(e))
    return render_template('index.html')

@app.route('/confirm', methods=['GET', 'POST'])
def confirm_download():
    url = session.get('video_url')
    if request.method == 'POST' and url:
        try:
            yt = YouTube(url)
            stream = yt.streams.get_highest_resolution()
            stream.download(DOWNLOAD_FOLDER)
            return render_template('confirm.html', success=True, video_title=yt.title)
        except Exception as e:
            return render_template('confirm.html', error=str(e))
    return render_template('confirm.html', url=url)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
