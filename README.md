## BMDS 210 - Building and Testing a CDS Hook

# Overview
The purpose of this project is to demonstrate the basic structure of a CDS Hooks service, including:
- CDS service discovery
- Handling incoming hook requests
- Using FHIR prefetch data
- Returning CDS cards to the EHR interface


[CDS Hooks](https://cds-hooks.org/) is an open specification that enables Electronic Health Record (EHR) systems to invoke external decision support services in real time. A CDS service can provide clinical guidance, recommendations, alerts, or informational cards during a clinician’s workflow.

In this project, we will:

1. Create a CDS Hooks service using GitHub Codespaces
2. Run the service locally
3. Test the service in the CDS Hooks Sandbox

# Use Cases
1. Patient Greeting Hook (greeting.py): displays a personalized greeting message to clinicians or front-desk staff when a patient chart is opened.
2. Pneumococcal Vaccine Reminder Hook (pneumococcal.py): identify patients 65+ years and present a clinical reminder for the pneumococcal vaccine during the patient encounter.

# References
- CDS Hooks official specification: https://cds-hooks.org/
- HL7 CDS Hooks: https://cds-hooks.hl7.org/
- CDS Hooks Sandbox: https://sandbox.cds-hooks.org/
