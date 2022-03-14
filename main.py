from flask import Flask, jsonify, request, render_template
from werkzeug.utils import secure_filename
import tempfile
import os
from OMPython import OMCSessionZMQ
app = Flask(__name__)

omc = OMCSessionZMQ()

ALLOWED_EXTENSIONS = {'mo'}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/health")
def health():
    return jsonify({"value": "OK"})

@app.route("/api")
def api():
    return jsonify({"message": "This is the base URL for the Modelicor API"})

@app.route("/api/health")
def api_health():
    version = omc.sendExpression("getVersion()")
    return jsonify({"value": "OK", "version": version})

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.errorhandler(500)
@app.route("/api/solve_file", methods=["POST"])
def solve_file():
    dirname = ''
    if 'file' not in request.files:
        return jsonify({"message": "no file object found in request"}), 500
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "file is missing filename property"}), 500
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        with tempfile.TemporaryDirectory() as tmpdirname:
            dirname += os.path.join(tmpdirname, filename)
            print('created temporary directory', tmpdirname)
            file.save(os.path.join(tmpdirname, filename))

    return jsonify({"dirmade": dirname})



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
