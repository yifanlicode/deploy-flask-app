from flask import Flask, render_template, request
from PIL import Image
from pytube import YouTube


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    image = request.files['image']
    output_format = request.form['output_format']

    try:
        # Open the image
        im = Image.open(image)

        # Convert to RGB if necessary
        if im.mode != 'RGB':
            im = im.convert('RGB')

        # Save the converted image to a file
        converted_image_path = 'converted_image.' + output_format
        im.save(converted_image_path, format=output_format)

        # Return the message with the converted image
        return render_template('index.html', message='Image successfully converted!')
    except Exception as e:
        return render_template('index.html', message=f'Error: {str(e)}')

@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == 'POST':
        video_url = request.form['video_url']
        try:
            yt = YouTube(video_url)
            stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            stream.download(output_path='downloads')
            return 'Video downloaded successfully!'
        except Exception as e:
            return f'Error: {str(e)}'
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
