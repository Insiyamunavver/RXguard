import os

from dotenv import load_dotenv

from crewai import Agent, Task, Crew, LLM


load_dotenv()


class ReviewDecisionAgent:
    """
    Reviews the validation results of all medicines in a prescription
    and decides whether the prescription should be approved or sent
    for manual review.
    """

    def __init__(self):

        self.llm = LLM(
            model="gemini/gemini-2.5-flash",
            api_key=os.getenv("GEMINI_API_KEY")
        )

        self.agent = Agent(
            role="Prescription Review Specialist",

            goal=(
                "Review the validation results of all medicines "
                "in a prescription and determine whether the "
                "prescription can be approved or requires manual review."
            ),

            backstory=(
                "You are responsible for the final prescription-level "
                "review decision. You examine the validation results "
                "provided for every medicine in a prescription. "
                "If all medicines have been successfully validated, "
                "the prescription should be approved. "
                "If even one medicine has not been successfully validated, "
                "the prescription must be sent for manual review."
            ),

            llm=self.llm,

            verbose=False
        )

    def decide(self, medicines):

        # --------------------------------------------------
        # Check validation results
        # --------------------------------------------------

        all_valid = True

        for medicine in medicines:

            verification = medicine.get(
                "verification",
                {}
            )

            if not verification.get(
                "exists",
                False
            ):
                all_valid = False
                break

        # --------------------------------------------------
        # Final review decision
        # --------------------------------------------------

        if all_valid:

            decision = "APPROVE"

            reason = (
                "All medicines in the prescription "
                "were successfully validated."
            )

        else:

            decision = "MANUAL_REVIEW"

            reason = (
                "At least one medicine in the prescription "
                "could not be successfully validated."
            )

        return {
            "decision": decision,
            "reason": reason
        }