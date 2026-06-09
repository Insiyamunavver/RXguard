from google import genai
from dotenv import load_dotenv
from pathlib import Path
import os


class GeminiClient:
    """Gemini wrapper for V2."""

    def __init__(self):

        env_path = (
            Path(__file__).parent.parent / ".env"
        )

        load_dotenv(
            dotenv_path=env_path
        )

        api_key = os.getenv(
            "GEMINI_API_KEY"
        )

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found"
            )

        self.client = genai.Client(
            api_key=api_key
        )

    def ask(
        self,
        prompt
    ):
        response = (
            self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
        )

        return response.text.strip()

    def analyze_image(
        self,
        image_path,
        prompt
    ):
        """
        Gemini Vision API
        """

        uploaded_file = (
            self.client.files.upload(
                file=image_path
            )
        )

        response = (
            self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    prompt,
                    uploaded_file
                ]
            )
        )

        return response.text.strip()