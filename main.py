import json
import random
from pathlib import Path

from playwright.sync_api import sync_playwright

from browser.rxai_client import RxAIClient
from browser.prescription_parser import PrescriptionParser
from browser.prescription_pipeline import PrescriptionPipeline

from agents.drug_validation_agent import DrugValidationAgent
from agents.review_decision_agent import ReviewDecisionAgent


# ============================================================
# FOLDERS
# ============================================================

PRESCRIPTION_FOLDER = "prescriptions"
OUTPUT_FOLDER = "outputs"
FAILED_FOLDER = "failed_prescriptions"


# ============================================================
# TEST SETTINGS
# ============================================================

# Keep these small while testing.
# Increase them later when the pipeline is stable.
BATCH_SIZE = 1
MAX_IMAGES = 5


# ============================================================
# PIPELINE CREATION
# ============================================================

def create_pipeline(page):
    """
    Create all components required by the prescription pipeline.

    The RxAIClient handles all browser interaction.
    The PrescriptionParser handles extraction parsing.
    The DrugValidationAgent handles AI-based medicine validation.
    """

    rxai_client = RxAIClient(page)

    parser = PrescriptionParser()

    drug_validator = DrugValidationAgent()

    review_agent =  ReviewDecisionAgent()

    return PrescriptionPipeline(
        rxai_client=rxai_client,
        parser=parser,
        drug_validator=drug_validator,
        review_agent=review_agent
    )


# ============================================================
# RANDOM PATIENT DATA
# ============================================================

def get_random_patient():
    """Generate random dummy patient data."""

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
        "patient_name": random.choice(names),
        "gender": random.choice(genders),
        "age": random.randint(18, 80),
        "uhid": f"UH-{random.randint(1000, 9999)}"
    }


# ============================================================
# RANDOM DOCTOR DATA
# ============================================================

def get_random_doctor():
    """Generate random dummy doctor data."""

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
        "doctor_name": random.choice(doctors),
        "department": random.choice(departments),
        "hospital": "Regency Hospital"
    }


# ============================================================
# MAIN PIPELINE
# ============================================================

def main():

    # --------------------------------------------------------
    # Create required output folders
    # --------------------------------------------------------

    Path(OUTPUT_FOLDER).mkdir(
        exist_ok=True
    )

    Path(FAILED_FOLDER).mkdir(
        exist_ok=True
    )

    # --------------------------------------------------------
    # Load prescription images
    # --------------------------------------------------------

    images = sorted(
        [
            str(p)
            for p in Path(
                PRESCRIPTION_FOLDER
            ).glob("*")
            if p.suffix.lower()
            in [
                ".jpg",
                ".jpeg",
                ".png"
            ]
        ]
    )

    # Limit number of images during testing
    images = images[:MAX_IMAGES]

    total_images = len(images)

    if total_images == 0:
        print("❌ No prescription images found.")
        return

    print(
        f"\n📁 Total images found: "
        f"{total_images}"
    )

    # --------------------------------------------------------
    # Process images in batches
    # --------------------------------------------------------

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

        print(
            "\n" + "=" * 60
        )

        print(
            f"🚀 STARTING BATCH "
            f"{batch_count}"
        )

        print(
            f"Images "
            f"{batch_start + 1} "
            f"to "
            f"{min(batch_start + BATCH_SIZE, total_images)}"
        )

        print(
            "=" * 60
        )

        # ----------------------------------------------------
        # Start browser
        # ----------------------------------------------------

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=False
            )

            context = browser.new_context()

            page = context.new_page()

            # ------------------------------------------------
            # Create RxAI client
            # ------------------------------------------------

            rxai_client = RxAIClient(page)

            # ------------------------------------------------
            # Login
            # ------------------------------------------------

            rxai_client.login()

            # ------------------------------------------------
            # Create pipeline
            # ------------------------------------------------

            pipeline = create_pipeline(page)

            # ------------------------------------------------
            # Process each prescription in the batch
            # ------------------------------------------------

            for index, image_path in enumerate(
                batch_images,
                start=1
            ):

                image_name = Path(
                    image_path
                ).stem

                print(
                    f"\n📸 Processing "
                    f"{index}/"
                    f"{len(batch_images)}"
                    f" → {image_name}"
                )

                # --------------------------------------------
                # Generate dummy patient and doctor data
                # --------------------------------------------

                patient_data = get_random_patient()

                doctor_data = get_random_doctor()

                try:

                    # ----------------------------------------
                    # Run prescription pipeline
                    # ----------------------------------------

                    result = pipeline.run(
                        image_path=image_path,
                        patient_data=patient_data,
                        doctor_data=doctor_data
                    )

                    # ----------------------------------------
                    # Save output JSON
                    # ----------------------------------------

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

                    # ----------------------------------------
                    # Check whether any medicine failed
                    # validation
                    # ----------------------------------------

                    has_failed_medicine = any(
                        not medicine[
                            "verification"
                        ].get(
                            "exists",
                            False
                        )
                        for medicine in result[
                            "medicines"
                        ]
                    )

                    # ----------------------------------------
                    # Save failed prescriptions separately
                    # ----------------------------------------

                    if has_failed_medicine:

                        failed_file = (
                            Path(
                                FAILED_FOLDER
                            )
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
                            f"⚠ Failed prescription "
                            f"saved: {failed_file}"
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

                    # ----------------------------------------
                    # Reset RxAI browser to upload page
                    # ----------------------------------------

                    rxai_client.reset_to_upload()

            # ------------------------------------------------
            # Close browser
            # ------------------------------------------------

            context.close()

            browser.close()

        print(
            f"✅ Batch {batch_count} complete."
        )

    print(
        "\n🎉 TEST COMPLETE!"
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()