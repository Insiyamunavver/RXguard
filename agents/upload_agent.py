from utils.config import BASE_URL


class UploadAgent:
    """Handles prescription upload flow."""

    def upload(self, page, image_path):
        # Navigate to upload page
        page.goto(f"{BASE_URL}/rx-upload")
        page.wait_for_load_state("networkidle")

        # Upload prescription image
        page.get_by_role(
            "button",
            name="Choose File"
        ).set_input_files(image_path)

        page.wait_for_timeout(2000)

        print("✅ Prescription uploaded successfully!")

        return True