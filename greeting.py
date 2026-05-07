from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# ---------------------------
# CDS Service Discovery
# ---------------------------
@app.route("/cds-services", methods=["GET"])
def discovery():
    return jsonify({
        "services": [
            {
                "hook": "patient-view",
                "id": "hello-bmds210",
                "title": "Hello from BMDS 210",
                "description": "Patient Greeting CDS Hook",
                "prefetch": {
                    "patient": "Patient/{{context.patientId}}"
#                    ,"conditionBundle": "Condition?patient={{context.patientId}}"
                }
            }
        ]
    })


# ---------------------------
# CDS Hook Endpoint
# ---------------------------
@app.route("/cds-services/hello-bmds210", methods=["POST"])
def patient_view_hook():

    # Read incoming CDS Hooks request
    hook_request = request.json

    print("Received hook:", hook_request.get("hook"))

    # -----------------------------------
    # Extract prefetched Patient resource
    # -----------------------------------
    patient = hook_request.get("prefetch", {}).get("patient", {})

    # -----------------------------------
    # Default patient name values
    # -----------------------------------
    given_name = "Unknown"
    family_name = "Patient"

    # -----------------------------------
    # Extract patient name
    # -----------------------------------
    if patient.get("name"):

        # Use first name entry
        name_entry = patient["name"][0]

        # Extract first/given name
        if name_entry.get("given"):
            given_name = name_entry["given"][0]

        # Extract family/last name
        if name_entry.get("family"):
            family = name_entry["family"]

    # Handle both string and list formats
    if isinstance(family, list):
        family_name = family[0]
    else:
        family_name = family

    # Handle both string and list formats
        if isinstance(family, list):
            family_name = family[0]
        else:
            family_name = family

    # Full patient name
    full_name = f"{given_name} {family_name}"

    print("PATIENT NAME:", full_name)


   # ---------------------------
    # Extract Conditions from Prefetch
    # ---------------------------
 #   prefetch = hook_request.get("prefetch", {})
 #   condition_bundle = prefetch.get("conditionBundle", {})

 #   conditions_list = []

 #   if condition_bundle.get("resourceType") == "Bundle":
 #      for entry in condition_bundle.get("entry", []):
 #           resource = entry.get("resource", {})
 #           if resource.get("resourceType") == "Condition":
 #               coding = resource.get("code", {}).get("coding", [])
 #               if coding:
 #                   condition_name = coding[0].get("display", "Unknown condition")
 #                   conditions_list.append(condition_name)

    # Format output
 #   if conditions_list:
 #       conditions_text = "\n".join(f"- {c}" for c in conditions_list)
 #   else:
 #       conditions_text = "No conditions found for this patient."


    # -----------------------------------
    # Return CDS card
    # -----------------------------------
    return jsonify({
        "cards": [
            {
                "summary": f"Viewing chart for {full_name}",
                "detail": "This response is generated from a CDS Hooks service running in Codespaces.",
 #               "detail": f"Conditions:\n{conditions_text}",
                "indicator": "info",

                "source": {
                    "label": "BMDS210 Patient Greeting Demo"
                }
            }
        ]
    })


# ---------------------------
# Run server
# ---------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)

