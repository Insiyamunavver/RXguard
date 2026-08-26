from utils.config import BASE_URL


class ReviewHandler:
    """Handles review and classify/push flow."""

    def review(self, page):
        # Go to review page
        page.goto(f"{BASE_URL}/rx-review")
        page.wait_for_load_state("load")

        print("🔍 On Review Page")

        # Move to Needs Review tab
        page.locator(
            'div.status-tab[data-status="needs_review"]'
        ).click()

        page.wait_for_timeout(1000)

        classify_btn = page.get_by_role(
            "button",
            name=" Classify & Push"
        )

        # If prescription available → push
        if classify_btn.is_visible():
            classify_btn.click()
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2000)

            print("✅ Prescription classified & pushed!")

            return "pushed"

        print("⚠️ No prescription available for push.")
        return "needs_manual_review"