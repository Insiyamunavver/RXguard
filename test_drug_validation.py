from agents.drug_validation_agent import (
    DrugValidationAgent
)

validator = (
    DrugValidationAgent()
)

result = (
    validator.validate_medicine(
        "Mesacol"
    )
)

print(result)