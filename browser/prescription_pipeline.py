from pathlib import Path


class PrescriptionPipeline:
    """Main orchestrator for prescription processing."""

    def __init__(
        self,
        rxai_client,
        parser,
        drug_validator,
        review_agent
    ):
        self.rxai = rxai_client
        self.parser = parser
        self.drug_validator = drug_validator
        self.review_agent = review_agent

    def run(
        self,
        image_path,
        patient_data,
        doctor_data
    ):
        print("\n🚀 STARTING PRESCRIPTION PIPELINE")
        print("=" * 50)

        # =====================================================
        # STEP 1 — Upload Prescription
        # =====================================================

        print("📤 Uploading prescription...")

        self.rxai.upload_prescription(
            image_path
        )

        # =====================================================
        # STEP 2 — Fill Patient Details
        # =====================================================

        print("📝 Filling patient form...")

        self.rxai.fill_patient_form(
            patient_data
        )

        # =====================================================
        # STEP 3 — Fill Doctor Details
        # =====================================================

        print("📝 Filling doctor form...")

        self.rxai.fill_doctor_form(
            doctor_data
        )

        # =====================================================
        # STEP 4 — Trigger RxAI Extraction
        # =====================================================

        print("🤖 Triggering RxAI extraction...")

        self.rxai.trigger_extraction()

        # =====================================================
        # STEP 5 — Parse Extracted Medicines
        # =====================================================

        print("📄 Reading RxAI prescription data...")

        platform_data = self.parser.extract_all(
            self.rxai.page
        )

        medicines = platform_data.get(
            "medicines",
            []
        )

        print(
            f"💊 Medicines extracted: "
            f"{len(medicines)}"
        )

        # =====================================================
        # STEP 6 — Validate Medicines
        # =====================================================

        print("💊 Validating medicines...")

        verified_medicines = []

        for medicine in medicines:

            medicine_name = medicine.get(
                "name",
                ""
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
                    f"⚠ Validation failed "
                    f"for {medicine_name}: {e}"
                )

                verification = {
                    "medicine": medicine_name,
                    "exists": False,
                    "drug_type": "Unknown",
                    "uses": [],
                    "confidence": 0
                }

            verified_medicines.append(
                {
                    **medicine,
                    "verification": verification
                }
            )

        # =====================================================
        # STEP 7 — Review Decision Agent
        # =====================================================

        print(
            "\n🧠 Reviewing prescription..."
        )

        review_decision = (
            self.review_agent.decide(
                verified_medicines
            )
        )

        print(
            f"📋 Review decision: "
            f"{review_decision['decision']}"
        )

        print(
            f"💡 Reason: "
            f"{review_decision['reason']}"
        )

        # =====================================================
        # STEP 8 — Review Prescription
        # =====================================================

        print(
            "\n🚀 Moving prescription "
            "to review..."
        )

        self.rxai.go_to_review()

        # -----------------------------------------------------
        # APPROVE
        # -----------------------------------------------------

        if review_decision["decision"] == "APPROVE":

            print(
                "✅ All medicines were validated."
            )

            print(
                "🤖 Review Agent decision: APPROVE"
            )

            review_status = "approved"
        else:
            print(
                "At least one medicine could not be validated"
            )
            print(
                "Review Agent decision: NEEDS_MANUAL_REVIEW"
            )
            review_status = "needs_manual_review"

        # =====================================================
        # STEP 9 — Build Final Result
        # =====================================================

        result = {
            "image_name":
                Path(
                    image_path
                ).name,

            "total_medicines":
                len(
                    verified_medicines
                ),

            "medicines":
                verified_medicines,

            "review_decision":
                review_decision,

            "review_status":
                review_status
        }

        # =====================================================
        # COMPLETE
        # =====================================================

        print("=" * 50)

        if review_status == "approved":

            print(
                "🎉 PRESCRIPTION APPROVED "
                "SUCCESSFULLY"
            )

        else:

            print(
                "⚠️ PRESCRIPTION SENT "
                "FOR MANUAL REVIEW"
            )

        print("=" * 50)

        return result