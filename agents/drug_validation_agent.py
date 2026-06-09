import os
import json
import asyncio
import nest_asyncio

from pathlib import Path
from dotenv import load_dotenv

from crewai import (
    Agent,
    Task,
    Crew,
    LLM
)

from crewai_tools import (
    SerperDevTool
)

nest_asyncio.apply()

load_dotenv()


class DrugValidationAgent:
    """Validates medicines using CrewAI + SerperDev + Gemini."""

    def __init__(self):

        self.search_tool = (
            SerperDevTool()
        )

        self.llm = LLM(
            model="gemini/gemini-2.5-flash",
            api_key=os.getenv(
                "GEMINI_API_KEY"
            )
        )

        self.agent = Agent(
            role=(
                "Pharmaceutical Validation Specialist"
            ),

            goal=(
                "Validate whether a medicine exists, "
                "identify its drug type, and "
                "identify its common uses."
            ),

            backstory=(
                "You are an experienced pharmacist "
                "and medicine validation expert."
            ),

            tools=[
                self.search_tool
            ],

            llm=self.llm,

            verbose=False
        )

        self.cache = (
            self.load_cache()
        )

    def load_cache(self):

        cache_file = Path(
            "cache/medicine_cache.json"
        )

        if not cache_file.exists():
            return {}

        try:

            with open(
                cache_file,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(
                    file
                )

        except Exception:

            return {}

    def save_cache(self):

        cache_file = Path(
            "cache/medicine_cache.json"
        )

        cache_file.parent.mkdir(
            exist_ok=True
        )

        with open(
            cache_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.cache,
                file,
                indent=4,
                ensure_ascii=False
            )

    def clean_medicine_name(
        self,
        medicine_name
    ):
        prefixes = [
            "T.",
            "TAB",
            "TAB.",
            "TABLET",
            "CAP",
            "CAP.",
            "CAPSULE",
            "SYR",
            "SYR.",
            "INJ",
            "INJ."
        ]

        clean_name = (
            medicine_name.strip()
        )

        for prefix in prefixes:

            if clean_name.upper().startswith(
                prefix
            ):
                clean_name = (
                    clean_name[
                        len(prefix):
                    ]
                    .strip()
                )
                break

        return clean_name

    async def _run_validation(
        self,
        medicine_name
    ):

        task = Task(
            description=f"""
Validate the medicine:

{medicine_name}

Use SerperDev search results.

Determine:

1. Does this medicine exist?
2. What type of drug is it?
3. What are its common uses?
4. Give confidence score.

Return ONLY valid JSON.

Format:

{{
    "medicine": "{medicine_name}",
    "exists": true,
    "drug_type": "",
    "uses": [],
    "confidence": 0
}}
""",

            expected_output=(
                "Valid JSON only."
            ),

            agent=self.agent
        )

        crew = Crew(
            agents=[
                self.agent
            ],

            tasks=[
                task
            ],

            verbose=False
        )

        result = (
            await crew.kickoff_async()
        )

        return result

    def validate_medicine(
        self,
        medicine_name
    ):

        medicine_name = (
            self.clean_medicine_name(
                medicine_name
            )
        )

        if (
            medicine_name
            in self.cache
        ):

            print(
                f"📦 Cache hit: "
                f"{medicine_name}"
            )

            return self.cache[
                medicine_name
            ]

        try:

            loop = (
                asyncio.get_event_loop()
            )

            result = (
                loop.run_until_complete(
                    self._run_validation(
                        medicine_name
                    )
                )
            )

            result_text = (
                str(result)
                .replace(
                    "```json",
                    ""
                )
                .replace(
                    "```",
                    ""
                )
                .strip()
            )

            validation_result = (
                json.loads(
                    result_text
                )
            )

            self.cache[
                medicine_name
            ] = validation_result

            self.save_cache()

            print(
                f"💾 Cached: "
                f"{medicine_name}"
            )

            return (
                validation_result
            )

        except Exception as e:

            print(
                f"⚠ Drug validation failed: {e}"
            )

            return {
                "medicine":
                    medicine_name,

                "exists":
                    False,

                "drug_type":
                    "Unknown",

                "uses":
                    [],

                "confidence":
                    0,

                "error":
                    str(e)
            }