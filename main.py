from flask import Flask, jsonify, request, render_template, send_file
from werkzeug.utils import secure_filename
import tempfile
import os
import sys
import json
import DyMat
from OMPython import OMCSessionZMQ
app = Flask(__name__)

omc = OMCSessionZMQ()
omc.sendExpression("installPackage(Modelica)")

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
    data = {}
    dirname = ''
    if 'file' not in request.files:
        return jsonify({"message": "no file object found in request"}), 500
    filein = request.files['file']
    if filein.filename == '':
        return jsonify({"message": "file is missing filename property"}), 500
    if filein and allowed_file(filein.filename):
        filename = secure_filename(filein.filename)
        results_filename = filename.replace('.mo', '_res.mat')
        with tempfile.TemporaryDirectory() as tmpdirname:
            form_data = dict(request.form)

            fullname = os.path.join(tmpdirname, filename)
            filein.save(fullname)

            omc = OMCSessionZMQ()
            omc.sendExpression('cd("' + tmpdirname + '")')
            omc.sendExpression('loadModel(Modelica)')
            omc.sendExpression('loadFile("' + filename + '", "' + form_data['model_name'] + '")')
            omc.sendExpression('instantiateModel(' + form_data['model_name'] + ')')
            metadata = omc.sendExpression("simulate(" + form_data['model_name'] + ", startTime=" + form_data['start_time'] + ", stopTime=" + form_data['stop_time'] + ", numberOfIntervals=" + form_data['interval_count'] + ")")

            sim_data = {}
            dmf = DyMat.DyMatFile(os.path.join(
                tmpdirname,
                form_data['model_name'] + '_res.mat'
            ))
            names = dmf.names()
            vars = []
            ignored = ["theta_const", "y_const", "youngs_modulus", "moment_inertia"]
            for var_name in names:
                if var_name not in ignored:
                    temp_list = dmf.getVarArray([var_name]).tolist()
                    sim_data[var_name] = temp_list

            return jsonify({"simulation_results": sim_data, "metadata": metadata})

    return jsonify({"message": "mysterious file processing failure"}), 500



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
