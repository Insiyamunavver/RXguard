class FormFillAgent:
    """Handles dynamic patient and doctor form filling."""

    def fill_patient_form(self, page, patient_data):
        """Fill patient details dynamically."""

        page.get_by_role(
            "textbox",
            name="e.g. Rahul Sharma"
        ).fill(patient_data["patient_name"])

        page.locator(
            'select[name="patient_gender"]'
        ).select_option(patient_data["gender"])

        page.get_by_role(
            "textbox",
            name="e.g. 45"
        ).fill(str(patient_data["age"]))

        page.get_by_role(
            "textbox",
            name="e.g. UH-"
        ).fill(patient_data["uhid"])

        print("✅ Patient form filled!")

    def fill_doctor_form(self, page, doctor_data):
        """Fill doctor details dynamically."""

        page.get_by_role(
            "textbox",
            name="e.g. Dr. Meena Gupta"
        ).fill(doctor_data["doctor_name"])

        page.get_by_role(
            "textbox",
            name="e.g. OPD"
        ).fill(doctor_data["department"])

        page.get_by_role(
            "textbox",
            name="e.g. Main Hospital"
        ).fill(doctor_data["hospital"])

        print("✅ Doctor form filled!")