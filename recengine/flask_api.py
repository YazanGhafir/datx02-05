import sys
import json

from flask import Flask, request, jsonify, render_template
from flask.json import JSONEncoder
from recengine import RecommendationEngine, fetch_program_from_model, ProgramSet
import numpy as np

class ExtendedJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ProgramSet):
            return obj.__dict__()

        return JSONEncoder.default(self, obj)

app = Flask(__name__)
app.json_encoder = ExtendedJSONEncoder


@app.route("/")
def index():
    print('Hello world!', file=sys.stderr)
    return render_template('index.html')


@app.route("/formpbar", methods=["POST"])
def formpbar():
    recengine = RecommendationEngine("pbar")
    name = request.form.get("fname")
    age = int(request.form.get("fage"))
    sex = int(request.form.get("fsex"))
    weight = float(request.form.get("fweight"))
    performance = float(request.form.get("fperformance"))

    data = np.array([age, weight, sex,
                     performance]).reshape(1, -1)
    best_pred, _ = recengine.recommend_training(data)
    program = fetch_program_from_model(best_pred["model"])
    return render_template("index.html", age=age, sex=sex, weight=weight, performance=performance,
                           best_pred=best_pred["model"].name,
                           predicted_performance=best_pred["predicted_performance"],
                           program=program,
                           name=name)


@app.route('/api/v1/pbar', methods=['POST'])
def pbar():

    recengine = RecommendationEngine("pbar")
    age = int(request.json.get('age', ''))
    weight = float(request.json.get('weight', ''))
    sex = request.json.get('sex', '')
    performance = float(request.json.get('performance', ''))
    if sex == 'MAN':
        converted_sex = 0
    elif sex == 'WOMAN':
        converted_sex = 1
    else:
        converted_sex = 2
    data = np.array([age, weight, converted_sex,
                     performance]).reshape(1, -1)
    best_pred, all_predictions = recengine.recommend_training(data)
    program = fetch_program_from_model(best_pred["model"])

    res = {
        "predicted_performance": best_pred["predicted_performance"],
        "training_program": best_pred["model"].name,
        "program_structure": program
    }

    return jsonify(res)


if __name__ == "__main__":
    app.run(debug=True)
