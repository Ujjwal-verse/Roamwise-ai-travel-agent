"""Conversational state machine. LLM extraction feeds deterministic, validated tools."""
from planner import FIELDS, plan, validate
from providers import extract_preferences, get_weather

class TravelAgent:
    def __init__(self, extractor=extract_preferences, weather_tool=get_weather):
        self.preferences = {}
        self.last_plan = None
        self.extractor = extractor
        self.weather_tool = weather_tool

    def reply(self, message):
        extracted = self.extractor(message, dict(self.preferences))
        patch = extracted["patch"]
        if set(patch) - FIELDS:
            raise ValueError("Model returned unsupported fields; please rephrase.")
        proposed = {**self.preferences, **patch}
        if extracted["questions"]:
            # Never replace an accepted plan with unvalidated model data.
            return {"status": "needs_clarification", "questions": extracted["questions"],
                    "note": "Please repeat the complete request with these details; the previous plan is unchanged."}
        validated = validate(proposed)
        result = plan(validated, self.weather_tool)
        result["changed_fields"] = [k for k in validated if validated[k] != self.preferences.get(k)]
        self.preferences = validated
        self.last_plan = result
        return result
