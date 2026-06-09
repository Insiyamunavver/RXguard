from playwright.sync_api import Page


class ExtractionAgent:
    """Reads extracted RxAI medicine results from UI."""

    def wait_for_extraction(
        self,
        page: Page
    ):
        page.wait_for_timeout(
            2000
        )

    def extract_drugs(
        self,
        page: Page
    ):
        """
        Extract medicine name,
        dosage and frequency
        from MEDICATIONS section.
        """

        text = page.locator(
            "body"
        ).inner_text()

        print("\n===== PAGE TEXT =====")
        print(text)
        print("=====================\n")

        medicines = []

        lines = text.split("\n")

        capture = False

        i = 0

        while i < len(lines):

            clean = (
                lines[i]
                .strip()
            )

            # Start MEDICATIONS section
            if (
                "MEDICATIONS"
                in clean.upper()
            ):
                capture = True
                i += 1
                continue

            if not capture:
                i += 1
                continue

            # Skip count row
            if (
                "found"
                in clean.lower()
            ):
                i += 1
                continue

            # End section
            if clean == (
                "Go to Review Page"
            ):
                break

            if not clean:
                i += 1
                continue

            medicine_name = clean

            dosage = ""
            frequency = ""

            # Next line contains:
            # 500mg | BD
            if (
                i + 1 < len(lines)
                and "|" in lines[i + 1]
            ):

                dose_line = (
                    lines[i + 1]
                    .strip()
                )

                parts = (
                    dose_line.split("|")
                )

                if len(parts) >= 2:

                    dosage = (
                        parts[0]
                        .strip()
                    )

                    frequency = (
                        parts[1]
                        .strip()
                    )

            medicines.append(
                {
                    "name":
                        medicine_name,

                    "dosage":
                        dosage,

                    "frequency":
                        frequency
                }
            )

            i += 2

        print(
            "\n===== EXTRACTED MEDICINES ====="
        )

        print(
            medicines
        )

        print(
            "===============================\n"
        )

        return medicines

    def extract_all(
        self,
        page: Page
    ):
        self.wait_for_extraction(
            page
        )

        return {
            "medicines":
                self.extract_drugs(
                    page
                )
        }