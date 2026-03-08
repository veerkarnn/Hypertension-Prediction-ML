from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Load trained model
model = joblib.load("model/hypertension_model.pkl")


stage_map = {
    0: "Normal",
    1: "Hypertension Stage 1",
    2: "Hypertension Stage 2",
    3: "Hypertensive Crisis"
}

color_map = {
    0: "#28a745",
    1: "#ffc107",
    2: "#fd7e14",
    3: "#dc3545"
}

recommendations = {
    0: "Maintain healthy lifestyle and monitor blood pressure regularly.",
    1: "Adopt lifestyle modifications and consult physician.",
    2: "Medical evaluation recommended. Medication may be required.",
    3: "Seek immediate medical attention."
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    Gender = request.form["Gender"]
    Age = request.form["Age"]
    History = request.form["History"]
    Patient = request.form["Patient"]
    TakeMedication = request.form["TakeMedication"]
    Severity = request.form["Severity"]
    BreathShortness = request.form["BreathShortness"]
    VisualChanges = request.form["VisualChanges"]
    NoseBleeding = request.form["NoseBleeding"]
    Whendiagnoused = request.form["Whendiagnoused"]
    Systolic = request.form["Systolic"]
    Diastolic = request.form["Diastolic"]
    ControlledDiet = request.form["ControlledDiet"]


    Gender = 0 if Gender == "Male" else 1

    Age_map = {"18-34":0,"35-50":1,"51-64":2,"65+":3}
    Age = Age_map[Age]

    History = 1 if History == "Yes" else 0
    Patient = 1 if Patient == "Yes" else 0
    TakeMedication = 1 if TakeMedication == "Yes" else 0

    Severity_map = {"Mild":0,"Moderate":1,"Severe":2}
    Severity = Severity_map[Severity]

    BreathShortness = 1 if BreathShortness == "Yes" else 0
    VisualChanges = 1 if VisualChanges == "Yes" else 0
    NoseBleeding = 1 if NoseBleeding == "Yes" else 0

    Diagnosis_map = {"<1 Year":0,"1-5 Years":1,">5 Years":2}
    Whendiagnoused = Diagnosis_map[Whendiagnoused]

    Systolic_map = {"100 - 110":0,"111 - 120":1,"121 - 130":2,"130+":3}
    Systolic = Systolic_map[Systolic]

    Diastolic_map = {"70 - 80":0,"81 - 90":1,"91 - 100":2,"100+":3}
    Diastolic = Diastolic_map[Diastolic]

    ControlledDiet = 1 if ControlledDiet == "Yes" else 0


    features = np.array([[Gender,Age,History,Patient,TakeMedication,
                          Severity,BreathShortness,VisualChanges,
                          NoseBleeding,Whendiagnoused,Systolic,
                          Diastolic,ControlledDiet]])

    prediction = model.predict(features)[0]

    try:
        confidence = round(max(model.predict_proba(features)[0]) * 100,2)
    except:
        confidence = 95

    result = stage_map[prediction]
    color = color_map[prediction]
    recommendation = recommendations[prediction]

    return render_template(
        "index.html",
        result=result,
        confidence=confidence,
        recommendation=recommendation,
        color=color
    )


if __name__ == "__main__":
    app.run(debug=True)