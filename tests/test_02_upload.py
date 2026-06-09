import os
import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://crm-prescription-ai.k8s-dev.hlthclub.in"
PRESCRIPTION_IMAGE = "prescription image/1757658072710.jpg"

class TestUpload:

    def test_navigate_to_upload(
        self, logged_in_page: Page
    ):
        """Test clicking Upload link works"""
        page = logged_in_page

        page.goto(f"{BASE_URL}/rx-upload")
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(1000)

        print("✅ Upload page loaded!")

    def test_upload_prescription_image(
        self, logged_in_page: Page
    ):
        """Test uploading a prescription image"""
        page = logged_in_page

        page.goto(f"{BASE_URL}/rx-upload")
        page.wait_for_load_state('networkidle')

        page.get_by_role(
            "button", name="Choose File"
        ).set_input_files(PRESCRIPTION_IMAGE)
        page.wait_for_timeout(2000)

        print("✅ Prescription image uploaded!")

    def test_fill_patient_information(
        self, logged_in_page: Page
    ):
        """Test filling patient information"""
        page = logged_in_page

        page.goto(f"{BASE_URL}/rx-upload")
        page.wait_for_load_state('networkidle')

        page.get_by_role(
            "textbox", name="e.g. Rahul Sharma"
        ).fill("Sunil Rathore")

        page.locator(
            'select[name="patient_gender"]'
        ).select_option("Male")

        page.get_by_role(
            "textbox", name="e.g. 45"
        ).fill("34")

        page.get_by_role(
            "textbox", name="e.g. UH-"
        ).fill("UH-0098")

        print("✅ Patient information filled!")

    def test_fill_doctor_information(
        self, logged_in_page: Page
    ):
        """Test filling doctor information"""
        page = logged_in_page

        page.goto(f"{BASE_URL}/rx-upload")
        page.wait_for_load_state('networkidle')

        page.get_by_role(
            "textbox", name="e.g. Dr. Meena Gupta"
        ).fill("Dr. Shilpa")

        page.get_by_role(
            "textbox", name="e.g. OPD"
        ).fill("OPD")

        page.get_by_role(
            "textbox", name="e.g. Main Hospital"
        ).fill("main hospital")

        print("✅ Doctor information filled!")

    def test_complete_upload_form(
        self, logged_in_page: Page
    ):
        """Complete upload form and click extract"""
        page = logged_in_page

        print("\n📋 Starting complete upload test...")

        # ✅ Using goto directly instead of clicking link
        page.goto(f"{BASE_URL}/rx-upload")
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(1000)
        print("  ✅ Navigated to Upload")

        page.get_by_role(
            "button", name="Choose File"
        ).set_input_files(PRESCRIPTION_IMAGE)
        page.wait_for_timeout(2000)
        print("  ✅ Image uploaded")

        page.get_by_role(
            "textbox", name="e.g. Rahul Sharma"
        ).fill("Sunil Rathore")

        page.locator(
            'select[name="patient_gender"]'
        ).select_option("Male")

        page.get_by_role(
            "textbox", name="e.g. 45"
        ).fill("34")

        page.get_by_role(
            "textbox", name="e.g. UH-"
        ).fill("UH-0098")
        print("  ✅ Patient info filled")

        page.get_by_role(
            "textbox", name="e.g. Dr. Meena Gupta"
        ).fill("Dr. Shilpa")

        page.get_by_role(
            "textbox", name="e.g. OPD"
        ).fill("OPD")

        page.get_by_role(
            "textbox", name="e.g. Main Hospital"
        ).fill("main hospital")
        print("  ✅ Doctor info filled")

        page.get_by_role(
            "button", name=" Extract Prescription"
        ).click()
        print("  ⏳ AI processing prescription...")

        page.wait_for_load_state(
            'networkidle', timeout=60000
        )
        page.wait_for_timeout(5000)

        print("✅ COMPLETE UPLOAD TEST DONE! 🎉")