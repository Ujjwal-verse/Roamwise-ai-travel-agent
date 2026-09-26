"""Validated planning tools: all arithmetic and feasibility decisions run outside the LLM."""
import math
from datetime import date, timedelta
from catalog import CATALOG, ASSUMPTIONS

FIELDS = {"origin", "days", "people", "budget", "interests", "pace", "destination", "start_date"}

def validate(raw):
    if not isinstance(raw, dict) or set(raw) - FIELDS:
        raise ValueError("Unexpected trip fields.")
    missing = [k for k in ("origin", "days", "people", "budget") if raw.get(k) is None]
    if missing:
        raise ValueError("Please provide: " + ", ".join(missing))
    p = dict(raw)
    if not isinstance(p["origin"], str) or p["origin"].strip().lower() not in ("delhi", "new delhi"):
        raise ValueError("This prototype supports departures from Delhi only.")
    p["origin"] = "Delhi"
    for key, low, high in (("days", 2, 7), ("people", 1, 8), ("budget", 1, 1000000)):
        if type(p[key]) is not int or not low <= p[key] <= high:
            raise ValueError(f"{key} must be an integer between {low} and {high}.")
    p.setdefault("interests", ["nature", "food"])
    if not isinstance(p["interests"], list) or not p["interests"] or any(
        i not in ["nature", "food", "wellness", "culture", "history"] for i in p["interests"]
    ):
        raise ValueError("Supported interests: nature, food, wellness, culture, history.")
    p.setdefault("pace", "relaxed")
    if p["pace"] not in ("relaxed", "balanced"):
        raise ValueError("Choose relaxed or balanced pace.")
    if p.get("destination") not in (None, *CATALOG):
        raise ValueError("Supported destinations: Rishikesh and Jaipur.")
    if p.get("start_date"):
        try:
            start = date.fromisoformat(p["start_date"])
        except (ValueError, TypeError):
            raise ValueError("start_date must be YYYY-MM-DD.") from None
        if start < date.today():
            raise ValueError("Please choose a present or future travel date.")
    return p

def build_candidate(p, name, weather=None):
    c = CATALOG[name]
    forecast = (weather or {}).get("rain_by_date", {})
    start = date.fromisoformat(p["start_date"]) if p.get("start_date") else None
    activities = sorted(c["activities"], key=lambda a: a[1] not in p["interests"])
    used, days, tickets = set(), [], 0
    for number in range(1, p["days"] + 1):
        day_date = (start + timedelta(days=number-1)).isoformat() if start else None
        rain = forecast.get(day_date)
        items = []
        if number in (1, p["days"]):
            items = ["Travel to destination, check in and rest" if number == 1 else "Check out and return to Delhi"]
        else:
            limit = 1 if p["pace"] == "relaxed" else 2
            for title, tag, outdoor, cost in activities:
                if title in used or (rain is not None and rain >= 5 and outdoor):
                    continue
                items.append(title)
                used.add(title)
                tickets += cost * p["people"]
                if len(items) == limit:
                    break
            if not items:
                items = ["Flexible rest time; choose a locally verified indoor activity"]
            items.append("Meals and unscheduled rest time")
        days.append({"day": number, "date": day_date, "activities": items,
                     "rain_mm": rain, "rain_adjusted": rain is not None and rain >= 5})
    breakdown = {
        "round_trip_transport": c["return_fare"] * p["people"],
        "accommodation": c["room"] * math.ceil(p["people"] / 2) * (p["days"] - 1),
        "food": c["food"] * p["people"] * p["days"],
        "local_transport": c["local"] * p["people"] * p["days"],
        "activities": tickets,
    }
    breakdown["contingency"] = math.ceil(sum(breakdown.values()) * 15 / 100)
    total = sum(breakdown.values())
    return {"destination": name, "estimated_total_inr": total, "budget_breakdown": breakdown,
            "within_budget": total <= p["budget"], "remaining_inr": p["budget"] - total,
            "interest_matches": sorted(set(p["interests"]) & set(c["tags"])),
            "itinerary": days, "sources": [c["source"]]}

def plan(raw, weather_tool=None):
    p = validate(raw)
    candidates = [build_candidate(p, n) for n in CATALOG if not p.get("destination") or n == p["destination"]]
    candidates.sort(key=lambda c: (not c["within_budget"], -len(c["interest_matches"]), c["estimated_total_inr"]))
    chosen = candidates[0]
    weather = {"status": "not_requested", "rain_by_date": {}}
    if weather_tool and p.get("start_date"):
        weather = weather_tool(chosen["destination"], p["start_date"], p["days"])
        chosen = build_candidate(p, chosen["destination"], weather)
    feasible = chosen["within_budget"]
    return {"status": "estimated_feasible" if feasible else "over_budget", "preferences": p,
            "plan": chosen, "alternatives": [{k: c[k] for k in ("destination", "estimated_total_inr", "within_budget")} for c in candidates[1:]],
            "weather": weather, "assumptions": ASSUMPTIONS,
            "explanation": ("Selected a budget-feasible destination, then matched interests and lower estimated cost."
                            if feasible else "No evaluated option fits this budget. Increase the budget, reduce days/people, or request another supported destination."),
            "tool_trace": ["validate_preferences", "search_local_catalog", "calculate_group_budget", "rank_candidates", "build_itinerary"] + (["weather_forecast"] if weather_tool and p.get("start_date") else [])}
