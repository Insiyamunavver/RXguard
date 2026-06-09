from pathlib import Path


class PipelineAgent:
    """Main orchestrator for prescription processing."""

    def __init__(
        self,
        uploader,
        filler,
        extractor,
        drug_validator,
        reviewer
    ):
        self.uploader = uploader
        self.filler = filler
        self.extractor = extractor
        self.drug_validator = (
            drug_validator
        )
        self.reviewer = reviewer

    def run(
        self,
        page,
        image_path,
        patient_data,
        doctor_data
    ):
        print("\n🚀 STARTING AGENT PIPELINE")
        print("=" * 50)

        # STEP 1
        print("📤 Uploading prescription...")

        self.uploader.upload(
            page,
            image_path
        )

        # STEP 2
        print("📝 Filling patient form...")

        self.filler.fill_patient_form(
            page,
            patient_data
        )

        print("📝 Filling doctor form...")

        self.filler.fill_doctor_form(
            page,
            doctor_data
        )

        # STEP 3
        print("🤖 Triggering RxAI extraction...")

        page.get_by_role(
            "button",
            name=" Extract Prescription"
        ).click()

        print(
            "⏳ Waiting for RxAI extraction..."
        )

        page.get_by_text(
            "Extracting Prescription Data"
        ).wait_for(
            state="hidden",
            timeout=180000
        )

        page.wait_for_timeout(
            3000
        )

        # STEP 4
        print(
            "📄 Reading RxAI data..."
        )

        platform_data = (
            self.extractor.extract_all(
                page
            )
        )

        medicines = (
            platform_data[
                "medicines"
            ]
        )

        # STEP 5
        print(
            "💊 Validating medicines..."
        )

        verified_medicines = []

        for medicine in medicines:

            medicine_name = (
                medicine.get(
                    "name",
                    ""
                )
            )

            print(
                f"🔍 Validating: "
                f"{medicine_name}"
            )

            try:

                verification = (
                    self.drug_validator
                    .validate_medicine(
                        medicine_name
                    )
                )

            except Exception as e:

                print(
                    f"⚠ Validation failed: {e}"
                )

                verification = {
                    "medicine":
                        medicine_name,

                    "exists":
                        False,

                    "drug_type":
                        "Unknown",

                    "uses":
                        [],

                    "confidence":
                        0
                }

            verified_medicines.append(
                {
                    **medicine,
                    "verification":
                        verification
                }
            )

        # STEP 6
        print(
            "🚀 Running review agent..."
        )

        self.reviewer.review(
            page
        )

        print("=" * 50)
        print("🎉 PIPELINE COMPLETE")
        print("=" * 50)

        return {
            "image_name":
                Path(
                    image_path
                ).name,

            "total_medicines":
                len(
                    verified_medicines
                ),

            "medicines":
                verified_medicines
        }