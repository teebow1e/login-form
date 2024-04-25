import pandas as pd
import joblib
from data.Modify import calculate_type_char, calculate_dup_char, calculate_unique_char, calculate_consecutive_LC, calculate_consecutive_UC, calculate_consecutive_number, calculate_sequence_character
from password_strength import PasswordStats

while True:
    test_data = input()
    if test_data == "###": break

    attr1 = len(test_data)
    attr2 = calculate_type_char(test_data)
    attr3 = calculate_dup_char(test_data)
    attr4 = calculate_unique_char(test_data)
    attr5 = calculate_consecutive_LC(test_data)
    attr6 = calculate_consecutive_UC(test_data)
    attr7 = calculate_consecutive_number(test_data)
    attr8 = calculate_sequence_character(test_data)
    X_new = pd.DataFrame([[attr1, attr2, attr3, attr4, attr5, attr6, attr7, attr8]],
            columns=['length', 'types_of_character', 'duplicate_character', 'unique_character', 'consecutive_LC', 'consecutive_UC', 'consecutive_number', 'sequence_character']) 

    DT_RG = joblib.load('model/decision_tree_regressor.pkl')
    RF_RG = joblib.load('model/random_forest_regressor.pkl')
    DT_CL = joblib.load('model/decision_tree_classification.pkl')
    RF_CL = joblib.load('model/random_forest_classification.pkl')

    y_pred1 = DT_RG.predict(X_new)
    print("DECISION TREE PREDICT: ", y_pred1)
    y_pred2 = RF_RG.predict(X_new)
    print("RANDOM FOREST PREDICT: ", y_pred2)
    print("PASSWORD STRENGTH LIBRARY PREDICT", PasswordStats(test_data).strength())

    print("-----------------------------------")

    y_pred3 = DT_CL.predict(X_new)
    print("DECISION TREE PREDICT: ", y_pred3)
    y_pred4 = RF_CL.predict(X_new)
    print("RANDOM FOREST PREDICT: ", y_pred4)
    classification = None
    strength = PasswordStats(test_data).strength()
    if strength < 0.2:
        classification = "1"
    elif 0.2 <= strength < 0.4:
        classification = "2"
    elif 0.4 <= strength < 0.6:
        classification = "3"
    elif 0.6 <= strength < 0.8:
        classification = "4"
    else:
        classification = "Very Strong"
    print("PASSWORD STRENGTH LIBRARY PREDICT:", classification)
    print("-----------------------------------")

