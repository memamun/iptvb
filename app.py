from flask import Flask, request, render_template, redirect, url_for
import re
import urllib.parse

app = Flask(__name__)

def parse_m3u(content):
    # Regular expression to parse M3U8 content
    pattern = re.compile(r'#EXTINF:.*?,(?P<name>.*?)\n(?P<url>.*?)\n')
    channels = pattern.findall(content)
    return [{'name': name.strip(), 'url': url.strip()} for name, url in channels]

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        content = file.read().decode('utf-8')
        channels = parse_m3u(content)
        return render_template('channels.html', channels=channels)
    return render_template('upload.html')

@app.route('/play/<path:url>')
def play(url):
    # Decode URL for safety
    url = urllib.parse.unquote(url)
    return render_template('player.html', url=url)

if __name__ == '__main__':
    app.run(debug=True)
