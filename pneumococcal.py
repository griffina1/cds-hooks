from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

def calculate_age(birth_date_str):
    today = datetime.today()
    dob = datetime.strptime(birth_date_str, "%Y-%m-%d")
    age = today.year - dob.year

    # Adjust if birthday hasn't occurred yet this year
    if (today.month, today.day) < (dob.month, dob.day):
        age -= 1

    return age


# =========================
# CDS service discovery
# =========================
@app.route("/cds-services", methods=["GET"])
def discovery():
    return jsonify({
        "services": [
            {
                "id": "pneumococcal-65-plus",
                "hook": "patient-view",
                "title": "Pneumococcal Vaccine Reminder",
                "description": "Recommends pneumococcal vaccine for patients 65+",
                "prefetch": {
                    "patient": "Patient/{{context.patientId}}"
                }
            }
        ]
    })


# =========================
# CDS hook endpoint
# =========================
@app.route("/cds-services/pneumococcal-65-plus", methods=["POST"])
def patient_view_hook():
    try:
        body = request.json

        # For patient-view, Patient is typically in prefetch
        patient = body.get("prefetch", {}).get("patient", {})

        birth_date = patient.get("birthDate")
        cards = []

        if birth_date:
            age = calculate_age(birth_date)

            if age >= 65:
                cards.append({
                    "summary": "Pneumococcal Vaccine Recommendation",
                    "detail": (
                        "This patient is 65 or older. "
                        "Consider administering a pneumococcal vaccine if not already given."
                    ),
                    "indicator": "info",
                    "source": {
                        "label": "BMDS210 vaccine recommendation demo" },
#                       , "links": [
#                {
#                    "label": "View CDC Pneumococcal Vaccine Guidelines",
#                    "url": "https://www.cdc.gov/pneumococcal/hcp/vaccine-recommendations/index.html",
#                    "type": "absolute"
#                }
#         ]
                    }
                )


                

        return jsonify({"cards": cards})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500


# =========================
# Run server
# =========================
if __name__ == "__main__":
    app.run(port=3000, debug=True)
