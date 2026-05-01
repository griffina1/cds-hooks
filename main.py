from flask import Flask, request, jsonify

app = Flask(__name__)

# -------------------------
# CDS Hooks discovery
# -------------------------
@app.route("/cds-services", methods=["GET"])
def services():
    return jsonify({
        "services": [
            {
                "id": "allergy-alert",
                "hook": "medication-prescribe",
                "title": "Allergy Alert Service",
                "description": "Warns about penicillin-amoxicillin interaction",
                "prefetch": {
                    "allergies": "AllergyIntolerance?patient={{context.patientId}}"
                }
            }
        ]
    })

# -------------------------
# CDS Hooks execution
# -------------------------
@app.route("/cds-services/allergy-alert", methods=["POST"])
def allergy_alert():
    body = request.json

    medication = (
        body.get("context", {})
        .get("medicationCodeableConcept", {})
        .get("text", "")
        .lower()
    )

    allergies_bundle = body.get("prefetch", {}).get("allergies", {})
    entries = allergies_bundle.get("entry", [])

    allergies = []
    for e in entries:
        resource = e.get("resource", {})
        text = resource.get("code", {}).get("text", "").lower()
        allergies.append(text)

    # Clinical rule
    if "penicillin" in " ".join(allergies) and "amoxicillin" in medication:
        return jsonify({
            "cards": [
                {
                    "summary": "Allergy Alert",
                    "detail": "Patient has a penicillin allergy. Amoxicillin may cause a reaction.",
                    "indicator": "warning",
                    "source": {
                        "label": "CDS Hooks Demo (Codespaces)"
                    }
                }
            ]
        })

    return jsonify({"cards": []})

# -------------------------
# Run server
# IMPORTANT for Codespaces
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
