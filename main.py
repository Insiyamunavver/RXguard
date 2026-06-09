import json
import random
from pathlib import Path
from playwright.sync_api import sync_playwright

from utils.config import (
    BASE_URL,
    USERNAME,
    PASSWORD
)

from agents.upload_agent import UploadAgent
from agents.form_fill_agent import FormFillAgent
from agents.extraction_agent import ExtractionAgent
from agents.drug_validation_agent import (
    DrugValidationAgent
)
from agents.review_agent import ReviewAgent
from agents.pipeline_agent import PipelineAgent


PRESCRIPTION_FOLDER = "prescriptions"
OUTPUT_FOLDER = "outputs"
FAILED_FOLDER = "failed_prescriptions"

# TEST ONLY FIRST 20 PRESCRIPTIONS
BATCH_SIZE = 1
MAX_IMAGES = 20

def login(page):
    """Login to RxAI."""

    page.goto(
        f"{BASE_URL}/rx-login?next=/rx-upload"
    )
    page.wait_for_load_state(
        "networkidle"
    )

    page.get_by_role(
        "textbox",
        name="Enter username"
    ).fill(USERNAME)

    page.get_by_role(
        "textbox",
        name="Enter password"
    ).fill(PASSWORD)

    page.get_by_role(
        "button",
        name=" Sign In"
    ).click()

    page.wait_for_load_state(
        "networkidle"
    )

    print("✅ Logged in!")


def create_pipeline():
    """Create all agents."""

    uploader = UploadAgent()

    filler = FormFillAgent()

    extractor = ExtractionAgent()

    drug_validator = (
        DrugValidationAgent()
    )

    reviewer = (
        ReviewAgent()
    )

    return PipelineAgent(
        uploader,
        filler,
        extractor,
        drug_validator,
        reviewer
    )

def reset_upload_page(page):
    """Reset UI back to upload page."""

    try:
        print(
            "↩ Resetting to upload page..."
        )

        page.goto(
            f"{BASE_URL}/rx-upload",
        timeout=60000
        )

        page.wait_for_load_state(
            "networkidle"
        )

        print(
            "✅ Upload page ready."
        )

    except Exception as e:
        print(
            f"⚠ Reset failed: {e}"
        )


def get_random_patient():
    """Random dummy patient data."""

    names = [
        "Rahul Sharma",
        "Amit Verma",
        "Priya Singh",
        "Karan Patel",
        "Neha Jain"
    ]

    genders = [
        "Male",
        "Female"
    ]

    return {
        "patient_name":
            random.choice(names),
        "gender":
            random.choice(genders),
        "age":
            random.randint(18, 80),
        "uhid":
            f"UH-{random.randint(1000,9999)}"
    }


def get_random_doctor():
    """Random dummy doctor data."""

    doctors = [
        "Dr. Gupta",
        "Dr. Mehta",
        "Dr. Sharma",
        "Dr. Rao"
    ]

    departments = [
        "Oncology",
        "OPD",
        "Medicine",
        "Surgery"
    ]

    return {
        "doctor_name":
            random.choice(doctors),
        "department":
            random.choice(departments),
        "hospital":
            "Regency Hospital"
    }


def main():
    Path(
        OUTPUT_FOLDER
    ).mkdir(exist_ok=True)
    Path(
        FAILED_FOLDER
    ).mkdir(exist_ok=True)

    # Load images
    images = sorted([
        str(p)
        for p in Path(
            PRESCRIPTION_FOLDER
        ).glob("*")
        if p.suffix.lower()
        in [".jpg", ".jpeg", ".png"]
    ])

    # TEST FIRST 2
    images = images[:MAX_IMAGES]

    total_images = len(images)

    if total_images == 0:
        print("❌ No images found.")
        return

    print(
        f"\n📁 Total images found: {total_images}"
    )

    batch_count = 0

    for batch_start in range(
        0,
        total_images,
        BATCH_SIZE
    ):
        batch_count += 1

        batch_images = images[
            batch_start:
            batch_start + BATCH_SIZE
        ]

        print("\n" + "=" * 60)
        print(
            f"🚀 STARTING BATCH {batch_count}"
        )
        print(
            f"Images {batch_start+1} "
            f"to "
            f"{min(batch_start+BATCH_SIZE, total_images)}"
        )
        print("=" * 60)

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False
            )

            context = (
                browser.new_context()
            )

            page = (
                context.new_page()
            )

            login(page)

            pipeline = (
                create_pipeline()
            )

            for index, image_path in enumerate(
                batch_images,
                start=1
            ):
                image_name = Path(
                    image_path
                ).stem

                print(
                    f"\n📸 Processing "
                    f"{index}/{len(batch_images)}"
                    f" → {image_name}"
                )

                patient_data = (
                    get_random_patient()
                )

                doctor_data = (
                    get_random_doctor()
                )

                try:
                    result = pipeline.run(
                        page=page,
                        image_path=image_path,
                        patient_data=patient_data,
                        doctor_data=doctor_data
                    )

                    output_file = (
                        Path(OUTPUT_FOLDER)
                        / f"{image_name}.json"
                    )

                    with open(
                        output_file,
                        "w",
                        encoding="utf-8"
                    ) as file:
                        json.dump(
                            result,
                            file,
                            indent=4
                        )

                    print(
                        f"✅ Saved: "
                        f"{output_file}"
                    )
                    has_failed_medicine = any(
                        not medicine["verification"].get(
                            "exists",
                            False
                        )
                        for medicine in result[
                            "medicines"
                        ]
                    )

                    if has_failed_medicine:

                        failed_file = (
                            Path(FAILED_FOLDER)
                            / f"{image_name}.json"
                        )

                        with open(
                            failed_file,
                            "w",
                            encoding="utf-8"
                        ) as file:
                            json.dump(
                                result,
                                file,
                                indent=4
                            )

                        print(
        f"⚠ Failed prescription saved: "
        f"{failed_file}"
    )

                except Exception as e:
                    print(
                        f"❌ Failed: "
                        f"{image_name}"
                    )
                    print(
                        f"Reason: {e}"
                    )

                finally:
                    reset_upload_page(
                        page
                    )

            context.close()
            browser.close()

        print(
            f"✅ Batch {batch_count} complete."
        )

    print(
        "\n🎉 TEST COMPLETE!"
    )


if __name__ == "__main__":
    main()