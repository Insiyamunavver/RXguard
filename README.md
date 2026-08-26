# RxGuard — AI-Powered Prescription Validation & Review System

RxGuard is an AI-powered prescription processing and review system that automates prescription extraction, medicine validation, and prescription-level review classification.

The system combines AI-based medicine validation, prescription parsing, and browser automation to process prescriptions and determine whether they should be classified as **Approved** or **Manual Review**.

---

## 🚀 Overview

Prescription processing involves multiple steps, including extracting information from prescription images, identifying medicines, validating those medicines, and determining whether a prescription requires human intervention.

RxGuard brings these steps together into a structured automated pipeline.

### High-Level Workflow

```text
Prescription Image
        ↓
RxAI Platform
        ↓
Prescription Extraction
        ↓
Prescription Parser
        ↓
Medicine Validation
        ↓
Review Decision
        ↓
   ┌────┴────┐
   ↓         ↓
APPROVED   MANUAL REVIEW

### Key Features
Automated prescription image upload
Browser-based interaction with the RxAI platform
Automated patient and doctor form filling
AI-powered prescription extraction
Structured extraction of:
Medicine name
Dosage
Frequency
Individual medicine validation
Prescription-level review decision
Classification into:
Approved
Manual Review
Medicine validation caching
JSON-based result storage
Batch processing of multiple prescriptions
Modular separation of browser automation, AI components, parsing, and orchestration


###🏗️ System Architecture

RxGuard follows a modular, sequential processing architecture.

                         RxGuard
                            │
                            ▼
                  ┌───────────────────┐
                  │ Prescription Input│
                  └─────────┬─────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │     RxAIClient    │
                  │ Browser Automation│
                  └─────────┬─────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │  RxAI Extraction  │
                  └─────────┬─────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │PrescriptionParser │
                  └─────────┬─────────┘
                            │
                            ▼
              ┌────────────────────────────┐
              │    Drug Validation Agent   │
              │     Medicine Validation    │
              └─────────────┬──────────────┘
                            │
                            ▼
                    Validation Results
                            │
                            ▼
              ┌────────────────────────────┐
              │   Review Decision Agent    │
              │   Prescription-level       │
              │        Decision            │
              └─────────────┬──────────────┘
                            │
                     ┌──────┴──────┐
                     │             │
                     ▼             ▼
                 APPROVED     MANUAL REVIEW

The complete workflow is orchestrated by the PrescriptionPipeline.

🤖 AI Components
1. Drug Validation Agent

File:

agents/drug_validation_agent.py

The Drug Validation Agent is responsible for validating medicines extracted from a prescription.

For each medicine, it determines whether the medicine can be successfully identified and returns structured validation information.

The validation result can include:

Medicine name
Existence/validation status
Drug type
Common uses
Confidence score
Example
{
  "medicine": "Example Medicine",
  "exists": true,
  "drug_type": "Example Drug Type",
  "uses": [
    "Example Use"
  ],
  "confidence": 0.95
}
2. Review Decision Agent

File:

agents/review_decision_agent.py

The Review Decision Agent evaluates the validation results of all medicines in a prescription and produces the prescription-level review decision.

The current decision rule is:

All medicines successfully validated
                ↓
             APPROVED
Any medicine not successfully validated
                ↓
          MANUAL REVIEW

This separates medicine-level validation from the prescription-level decision.

🌐 Browser Automation
RxAI Client

File:

browser/rxai_client.py

The RxAIClient is responsible for browser interaction with the RxAI platform.

It handles tasks such as:

Logging into the platform
Uploading prescriptions
Filling patient information
Filling doctor information
Triggering prescription extraction
Navigating through the RxAI interface
Accessing prescription review information

Browser automation is implemented using Playwright.

📄 Prescription Parser

File:

browser/prescription_parser.py

The PrescriptionParser converts information extracted from the RxAI interface into structured prescription data.

The parser extracts information such as:

Prescription metadata
Patient information
Doctor information
Medicine names
Dosage
Frequency
Example
{
  "name": "Medicine Name",
  "dosage": "10mg",
  "frequency": "OD"
}
🔄 Prescription Pipeline

File:

browser/prescription_pipeline.py

The PrescriptionPipeline acts as the main workflow orchestrator.

It coordinates the complete prescription-processing flow:

1. Upload Prescription
        ↓
2. Fill Patient Information
        ↓
3. Fill Doctor Information
        ↓
4. Trigger RxAI Extraction
        ↓
5. Parse Extracted Prescription
        ↓
6. Validate Medicines
        ↓
7. Review Prescription
        ↓
8. Generate Final Decision
        ↓
9. Save Result
📊 Review Logic

The prescription-level decision follows a simple and auditable rule.

Approved

A prescription is classified as Approved when all extracted medicines are successfully validated.

Medicine A → Valid       ✓
Medicine B → Valid       ✓
Medicine C → Valid       ✓
Medicine D → Valid       ✓

          ↓

       APPROVED
Manual Review

A prescription is classified as Manual Review when at least one extracted medicine cannot be successfully validated.

Medicine A → Valid       ✓
Medicine B → Valid       ✓
Medicine C → Not Valid   ✗
Medicine D → Valid       ✓

          ↓

    MANUAL REVIEW

This approach ensures that a medicine validation failure is not hidden by an overall prescription-level decision.

📁 Project Structure
rxguard/
│
├── agents/
│   ├── __init__.py
│   ├── drug_validation_agent.py
│   └── review_decision_agent.py
│
├── browser/
│   ├── form_filler.py
│   ├── prescription_parser.py
│   ├── prescription_pipeline.py
│   ├── Review_handler.py
│   ├── rxai_client.py
│   └── Upload_Handler.py
│
├── llm/
│   ├── __init__.py
│   ├── config.py
│   ├── gemini_client.py
│   └── prompts.py
│
├── tests/
│   ├── test_01_login.py
│   ├── test_02_upload.py
│   ├── test_03_review.py
│   └── test_04_full_pipeline.py
│
├── utils/
│   ├── __init__.py
│   └── config.py
│
├── .env.example
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
🛠️ Technology Stack
Python — Core application development
CrewAI — AI agent framework
Google Gemini — LLM-powered validation and reasoning
Playwright — Browser automation
RxAI — Prescription extraction platform
JSON — Structured result storage
Git — Version control
GitHub — Source code management
⚙️ Installation
1. Clone the repository
git clone https://github.com/YOUR_USERNAME/rxguard.git
cd rxguard

Replace YOUR_USERNAME with your GitHub username.

2. Create a virtual environment

For Windows:

python -m venv venv

Activate the environment:

.\venv\Scripts\Activate.ps1
3. Install dependencies
pip install -r requirements.txt
4. Install Playwright browsers
playwright install
🔐 Environment Configuration

Create a .env file in the project root.

Use .env.example as the template.

Example:

RXAI_URL=
RXAI_USER=
RXAI_PASSWORD=

GEMINI_API_KEY=
SERPER_API_KEY=
Security

Do not commit the .env file to GitHub.

The .env.example file contains only placeholder values and is provided to show the required environment variables.

▶️ Running the Project

Place authorized test prescription images inside:

prescriptions/

Then run:

python main.py

The system will:

Start the browser
Log into the RxAI platform
Upload the prescription
Fill patient and doctor information
Trigger AI extraction
Parse the extracted medicines
Validate each medicine
Generate a prescription-level review decision
Save the result
📦 Batch Processing

Batch settings can be configured in main.py.

For example:

BATCH_SIZE = 1
MAX_IMAGES = 5

This processes up to five prescriptions individually.

For larger batches:

BATCH_SIZE = 10
MAX_IMAGES = 15

This would process:

Batch 1 → Prescriptions 1–10
Batch 2 → Prescriptions 11–15
🧪 Testing

The project contains tests for different stages of the workflow.

Examples include:

tests/
├── test_01_login.py
├── test_02_upload.py
├── test_03_review.py
└── test_04_full_pipeline.py

Additional tests can be used for individual AI and integration components.

📤 Output

The pipeline generates structured JSON results containing information such as:

Prescription image name
Number of extracted medicines
Medicine validation results
Review decision
Review status
Example
{
  "image_name": "prescription.jpg",
  "total_medicines": 4,
  "review_decision": {
    "decision": "APPROVE",
    "reason": "All medicines in the prescription were successfully validated."
  },
  "review_status": "approved"
}
🔒 Data Privacy

Prescription images and runtime-generated data are intentionally excluded from version control.

The following directories should remain local:

prescriptions/
outputs/
failed_prescriptions/
logs/
cache/

Prescription data may contain sensitive patient and healthcare information and should only be processed with appropriate authorization.

API keys, passwords, and other credentials must also be stored through environment variables and must never be committed to the repository.

⚠️ Current Limitations

The current version focuses on the prescription validation and review-classification workflow.

The system currently determines whether a prescription should be:

APPROVED

or:

MANUAL REVIEW

However, the final browser action of physically clicking the Approve button on the RxAI review interface is intentionally not forced by the current pipeline.

This allows the prescription-level decision logic to be tested independently from the final UI action.

🔮 Future Improvements

Potential future improvements include:

Automating the final RxAI approval action
Handling prescriptions where no medicines are extracted
Improving medicine-name normalization
Adding confidence-based validation thresholds
Providing detailed explanations for failed medicine validation
Improving browser retry and recovery mechanisms
Separating technical failures from manual-review outcomes
Adding persistent database storage
Adding analytics and monitoring
Building a human-in-the-loop review interface
Integrating with healthcare APIs instead of browser-only workflows
🎯 Design Principles
Separation of Responsibilities

RxGuard separates different responsibilities into dedicated components:

Browser Automation
        ↓
Prescription Extraction
        ↓
Prescription Parsing
        ↓
Medicine Validation
        ↓
Review Decision
        ↓
Final Classification

This makes the system easier to maintain, test, and extend.

Deterministic Review Rule

The final review classification follows a clear business rule:

All medicines validated
        ↓
    APPROVED
Any medicine not validated
        ↓
 MANUAL REVIEW
⚠️ Disclaimer

RxGuard is a software engineering and automation project.

It is not intended to:

Diagnose patients
Prescribe medication
Replace healthcare professionals
Provide medical advice
Make independent clinical decisions

Medicine validation results should be treated as assistive information and appropriate human oversight should be maintained in real-world healthcare workflows.

👩‍💻 Author

Your Name

GitHub: https://github.com/YOUR_USERNAME

📌 Project Status

Status: Functional Prototype

The current implementation demonstrates:

Prescription image processing
AI-powered prescription extraction
Structured medicine parsing
Medicine-level validation
Prescription-level review classification
Approved/manual-review output
Browser-based workflow automation
Batch processing
Modular pipeline architecture
