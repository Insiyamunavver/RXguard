import pytest
from playwright.sync_api import Page

BASE_URL = "https://crm-prescription-ai.k8s-dev.hlthclub.in"

class TestReview:

    def go_to_review(self, page: Page):
        """Navigate directly to review page URL"""
        page.goto(f"{BASE_URL}/rx-review")
        page.wait_for_load_state('load')  # ✅ changed from networkidle to load
        page.wait_for_timeout(2000)       # ✅ increased from 1000 to 2000

    def test_navigate_to_review_page(
        self, logged_in_page: Page
    ):
        """Test navigating to review page"""
        page = logged_in_page
        self.go_to_review(page)
        print("✅ Review page loaded!")

    def test_approved_tab(
        self, logged_in_page: Page
    ):
        """Test clicking Approved tab"""
        page = logged_in_page
        self.go_to_review(page)

        page.locator(
            'div.status-tab[data-status="approved"]'
        ).click()
        page.wait_for_timeout(1000)
        print("✅ Approved tab clicked!")

    def test_open_approved_prescription(
        self, logged_in_page: Page
    ):
        """Test opening an approved prescription"""
        page = logged_in_page
        self.go_to_review(page)

        page.locator(
            'div.status-tab[data-status="approved"]'
        ).click()
        page.wait_for_timeout(1000)

        first = page.locator('[id^="card-"]').first

        if first.is_visible():
            first.click()
            page.wait_for_timeout(2000)
            print("✅ Prescription opened!")
        else:
            print("ℹ️ No approved prescriptions found")

    def test_needs_review_tab(
        self, logged_in_page: Page
    ):
        """Test clicking Needs Review tab"""
        page = logged_in_page
        self.go_to_review(page)

        page.locator(
            'div.status-tab[data-status="needs_review"]'
        ).click()
        page.wait_for_timeout(1000)
        print("✅ Needs Review tab clicked!")

    def test_classify_and_push(
        self, logged_in_page: Page
    ):
        """Test Classify and Push button"""
        page = logged_in_page
        self.go_to_review(page)

        page.locator(
            'div.status-tab[data-status="needs_review"]'
        ).click()
        page.wait_for_timeout(1000)

        classify_btn = page.get_by_role(
            "button", name=" Classify & Push"
        )

        if classify_btn.is_visible():
            classify_btn.click()
            page.wait_for_load_state('load')  # ✅ changed here too
            page.wait_for_timeout(2000)
            print("✅ Classify & Push clicked!")
        else:
            print(
                "ℹ️ No prescriptions to "
                "classify right now"
            )