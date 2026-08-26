from pathlib import Path

from playwright.sync_api import Page

from utils.config import BASE_URL, USERNAME, PASSWORD


class RxAIClient:
    """Handles all browser interaction with the RxAI platform."""

    def __init__(self, page: Page):
        self.page = page

    # -------------------------
    # Authentication
    # -------------------------

    def login(self):
        """Log in to the RxAI platform."""

        self.page.goto(
            f"{BASE_URL}/rx-login?next=/rx-upload"
        )

        self.page.wait_for_load_state(
            "networkidle"
        )

        self.page.get_by_role(
            "textbox",
            name="Enter username"
        ).fill(USERNAME)

        self.page.get_by_role(
            "textbox",
            name="Enter password"
        ).fill(PASSWORD)

        self.page.get_by_role(
            "button",
            name=" Sign In"
        ).click()

        self.page.wait_for_load_state(
            "networkidle"
        )

        print("✅ Logged in!")

    # -------------------------
    # Upload
    # -------------------------

    def upload_prescription(
        self,
        image_path: str
    ):
        """Navigate to upload page and upload prescription."""

        self.page.goto(
            f"{BASE_URL}/rx-upload"
        )

        self.page.wait_for_load_state(
            "networkidle"
        )

        self.page.get_by_role(
            "button",
            name="Choose File"
        ).set_input_files(
            image_path
        )

        self.page.wait_for_timeout(
            2000
        )

        print(
            f"✅ Prescription uploaded: "
            f"{Path(image_path).name}"
        )

    # -------------------------
    # Patient Form
    # -------------------------

    def fill_patient_form(
        self,
        patient_data: dict
    ):
        """Fill patient information."""

        self.page.get_by_role(
            "textbox",
            name="e.g. Rahul Sharma"
        ).fill(
            patient_data["patient_name"]
        )

        self.page.locator(
            'select[name="patient_gender"]'
        ).select_option(
            patient_data["gender"]
        )

        self.page.get_by_role(
            "textbox",
            name="e.g. 45"
        ).fill(
            str(patient_data["age"])
        )

        self.page.get_by_role(
            "textbox",
            name="e.g. UH-"
        ).fill(
            patient_data["uhid"]
        )

        print("✅ Patient form filled!")

    # -------------------------
    # Doctor Form
    # -------------------------

    def fill_doctor_form(
        self,
        doctor_data: dict
    ):
        """Fill doctor information."""

        self.page.get_by_role(
            "textbox",
            name="e.g. Dr. Meena Gupta"
        ).fill(
            doctor_data["doctor_name"]
        )

        self.page.get_by_role(
            "textbox",
            name="e.g. OPD"
        ).fill(
            doctor_data["department"]
        )

        self.page.get_by_role(
            "textbox",
            name="e.g. Main Hospital"
        ).fill(
            doctor_data["hospital"]
        )

        print("✅ Doctor form filled!")

    # -------------------------
    # Prescription Extraction
    # -------------------------

    def trigger_extraction(self):
        """Trigger RxAI's prescription extraction."""

        self.page.get_by_role(
            "button",
            name=" Extract Prescription"
        ).click()

        print(
            "🤖 RxAI prescription extraction triggered."
        )

        self.page.get_by_text(
            "Extracting Prescription Data"
        ).wait_for(
            state="hidden",
            timeout=180000
        )

        self.page.wait_for_timeout(
            3000
        )

        print(
            "✅ RxAI prescription extraction completed."
        )

    # -------------------------
    # Review
    # -------------------------

    def go_to_review(self):
        """Navigate to the prescription review page."""

        self.page.goto(
            f"{BASE_URL}/rx-review"
        )

        self.page.wait_for_load_state(
            "load"
        )

        print("🔍 On Review Page")

    # -------------------------
    # Classify & Push
    # -------------------------

    def classify_and_push(self):
        """Classify and push the prescription if available."""

        self.page.locator(
            'div.status-tab[data-status="needs_review"]'
        ).click()

        self.page.wait_for_timeout(
            1000
        )

        classify_btn = self.page.get_by_role(
            "button",
            name=" Classify & Push"
        )

        if classify_btn.is_visible():

            classify_btn.click()

            self.page.wait_for_load_state(
                "networkidle"
            )

            self.page.wait_for_timeout(
                2000
            )

            print(
                "✅ Prescription classified & pushed!"
            )

            return "pushed"

        print(
            "⚠️ No prescription available for push."
        )

        return "needs_manual_review"

    # -------------------------
    # Reset
    # -------------------------

    def reset_to_upload(self):
        """Reset the browser to the upload page."""

        try:

            print(
                "↩ Resetting to upload page..."
            )

            self.page.goto(
                f"{BASE_URL}/rx-upload",
                timeout=60000
            )

            self.page.wait_for_load_state(
                "networkidle"
            )

            print(
                "✅ Upload page ready."
            )

        except Exception as e:

            print(
                f"⚠ Reset failed: {e}"
            )