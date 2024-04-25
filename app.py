from flask import Flask, request, render_template
import pandas as pd
import joblib
from data.Modify import calculate_type_char, calculate_dup_char, calculate_unique_char, calculate_consecutive_LC, calculate_consecutive_UC, calculate_consecutive_number, calculate_sequence_character
from password_strength import PasswordStats

DT_RG = joblib.load('model/decision_tree_regressor.pkl')
RF_RG = joblib.load('model/random_forest_regressor.pkl')
DT_CL = joblib.load('model/decision_tree_classification.pkl')
RF_CL = joblib.load('model/random_forest_classification.pkl')

available_models = {
    "dt_rg": DT_RG,
    "rf_rg": RF_RG,
    "dt_cl": DT_CL,
    "rf_cl": RF_CL,
}

app = Flask(
    __name__,
    static_url_path='',
    static_folder='static/',
    template_folder='templates/'
)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/strength", methods=["POST"])
def test_strength():
    model = request.form["model"]
    password_to_test = request.form["password"]
    print("received model: ", model)
    print("received password: ", password_to_test)
    if model == "pwstat_lib":
        return str(PasswordStats(password_to_test).strength())

    attr1 = len(password_to_test)
    attr2 = calculate_type_char(password_to_test)
    attr3 = calculate_dup_char(password_to_test)
    attr4 = calculate_unique_char(password_to_test)
    attr5 = calculate_consecutive_LC(password_to_test)
    attr6 = calculate_consecutive_UC(password_to_test)
    attr7 = calculate_consecutive_number(password_to_test)
    attr8 = calculate_sequence_character(password_to_test)
    X_new = pd.DataFrame([[attr1, attr2, attr3, attr4, attr5, attr6, attr7, attr8]],
            columns=['length', 'types_of_character', 'duplicate_character', 'unique_character', 'consecutive_LC', 'consecutive_UC', 'consecutive_number', 'sequence_character']) 

    prediction = available_models[model].predict(X_new)
    # result is a ndarray
    result = str(prediction.tolist()[0])
    return result

app.run(host="0.0.0.0", port=8000, debug=False)