from collections import Counter
from utils.Preprocessing import *
from flask import Flask, request, render_template, jsonify
import pandas as pd
import joblib
from data.Modify import (
    calculate_type_char,
    calculate_dup_char,
    calculate_unique_char,
    calculate_consecutive_LC,
    calculate_consecutive_UC,
    calculate_consecutive_number,
    calculate_sequence_character,
)
from password_strength import PasswordStats

DT_RG = joblib.load("model/decision_tree_regressor.pkl")
DT_CL = joblib.load("model/decision_tree_classification.pkl")
RF_RG = joblib.load("model/random_forest_regressor.pkl")
RF_CL = joblib.load("model/random_forest_classification.pkl")
KNN_RG = joblib.load("model/knn_regression.pkl")
KNN_CL = joblib.load("model/knn_classification.pkl")
LGBM_RG = joblib.load("model/lgbm_regression.pkl")
LGBM_CL = joblib.load("model/lgbm_classification.pkl")
LINEAR_RG = joblib.load("model/linear_regression.pkl")
SVC = joblib.load("model/SVC.pkl")
SVR = joblib.load("model/SVR.pkl")
GNB_CL = joblib.load("model/gaussianNB_classification.pkl")

def VOTING_CL(password):
    attr1 = len(password)
    attr2 = calculate_type_char(password)
    attr3 = calculate_dup_char(password)
    attr4 = calculate_unique_char(password)
    attr5 = calculate_consecutive_LC(password)
    attr6 = calculate_consecutive_UC(password)
    attr7 = calculate_consecutive_number(password)
    attr8 = calculate_sequence_character(password)
    
    X_new = pd.DataFrame([[attr1, attr2, attr3, attr4, attr5, attr6, attr7, attr8]],
            columns=['length', 'types_of_character', 'duplicate_character', 'unique_character', 'consecutive_LC', 
                     'consecutive_UC', 'consecutive_number', 'sequence_character']) 
    
    predictions = []
    predictions.append(DT_CL.predict(X_new)[0])
    predictions.append(RF_CL.predict(X_new)[0])
    predictions.append(KNN_CL.predict(X_new)[0])
    predictions.append(LGBM_CL.predict(X_new)[0])
    predictions.append(SVC.predict(X_new)[0])
    count = Counter(predictions)
    return count.most_common(1)[0][0]

available_models = {
    "dt_rg": DT_RG,
    "rf_rg": RF_RG,
    "knn_rg": KNN_RG,
    "lgbm_rg": LGBM_RG,
    "sv_rg": SVR,
    "dt_cl": DT_CL,
    "rf_cl": RF_CL,
    "knn_cl": KNN_CL,
    "lgbm_cl": LGBM_CL,
    "sv_cl": SVC,
    "linear_rg": LINEAR_RG,
    "gnb_cl": GNB_CL,
}

app = Flask(
    __name__, static_url_path="", static_folder="static/", template_folder="templates/"
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/strength", methods=["POST"])
def test_strength():
    result = 0
    model = request.form["model"]
    password_to_test = request.form["password"]
    print("received model:", model)
    print("received password:", password_to_test)
    isClassification = "_cl" in model

    if model == "pwstat_lib":
        result = str(PasswordStats(password_to_test).strength())
        print(f"prediction for the model {model}: {result}")
    elif model == "voting_cl":
        result = str(VOTING_CL(password_to_test))
        print(f"prediction for the model {model}: {result}")
    else:
        attr1 = len(password_to_test)
        attr2 = calculate_type_char(password_to_test)
        attr3 = calculate_dup_char(password_to_test)
        attr4 = calculate_unique_char(password_to_test)
        attr5 = calculate_consecutive_LC(password_to_test)
        attr6 = calculate_consecutive_UC(password_to_test)
        attr7 = calculate_consecutive_number(password_to_test)
        attr8 = calculate_sequence_character(password_to_test)
        X_new = pd.DataFrame(
            [[attr1, attr2, attr3, attr4, attr5, attr6, attr7, attr8]],
            columns=[
                "length",
                "types_of_character",
                "duplicate_character",
                "unique_character",
                "consecutive_LC",
                "consecutive_UC",
                "consecutive_number",
                "sequence_character",
            ],
        )
        prediction = available_models[model].predict(X_new)
        result = str(prediction.tolist()[0])
        print(f"prediction for the model {model}: {result}")

    final_resp = {
        "model": model,
        "strength": result,
        "isClassification": isClassification,
    }
    return jsonify(final_resp)


app.run(host="0.0.0.0", port=8000, debug=False)
