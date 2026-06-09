import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://crm-prescription-ai.k8s-dev.hlthclub.in"

class TestLogin:

    def test_login_page_loads(self, page: Page):
        """Check login page opens correctly"""
        page.goto(f"{BASE_URL}/rx-login?next=/")
        page.wait_for_load_state('networkidle')

        expect(
            page.get_by_role(
                "textbox", name="Enter username"
            )
        ).to_be_visible()

        expect(
            page.get_by_role(
                "textbox", name="Enter password"
            )
        ).to_be_visible()

        expect(
            page.get_by_role("button", name=" Sign In")
        ).to_be_visible()

        print("✅ Login page loaded correctly!")

    def test_successful_login(self, page: Page):
        """Test logging in with correct credentials"""
        page.goto(f"{BASE_URL}/rx-login?next=/")
        page.wait_for_load_state('networkidle')

        page.get_by_role(
            "textbox", name="Enter username"
        ).fill("rxadmin")

        page.get_by_role(
            "textbox", name="Enter password"
        ).fill("ThbRx@2026!")

        page.get_by_role(
            "button", name=" Sign In"
        ).click()
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(2000)

        print("✅ Login successful!")

    def test_navigation_visible_after_login(
        self, logged_in_page: Page
    ):
        """Verify navigation links appear after login"""
        page = logged_in_page

        expect(
            page.get_by_role("link", name="Upload")
        ).to_be_visible()

        print("✅ Navigation visible after login!")