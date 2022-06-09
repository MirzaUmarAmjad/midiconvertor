import requests
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from flask import send_file
from audio2midi import run

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "static/"


@app.route('/')
def upload_file():
    return render_template('index.html')


@app.route('/display', methods=['GET', 'POST'])
def save_file():
    if request.method == 'POST':

        if request.files['file']:
            f = request.files['file']
            filename = secure_filename(f.filename)

            f.save(app.config['UPLOAD_FOLDER'] + filename)

            # file = open(app.config['UPLOAD_FOLDER'] + filename, "r")
            # print(file)
            run(app.config['UPLOAD_FOLDER'] + filename, "output_midi_file.mid")

        else:
            url = request.form.get('url')
            r = requests.get(url, allow_redirects=True)
            open('input.wav', 'wb').write(r.content)
            run("input.wav", "output_midi_file.mid")

    path = "output_midi_file.mid"
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run()