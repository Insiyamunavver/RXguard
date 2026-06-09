from agents.gemini_vision_agent import (
    GeminiVisionAgent
)

agent = GeminiVisionAgent()

result = agent.extract(
    "prescriptions/1757654664355.jpg"
)

print(result)