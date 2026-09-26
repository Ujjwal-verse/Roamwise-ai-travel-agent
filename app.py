"""Run: python3 app.py --demo, or python3 app.py for Azure chat."""
import argparse
import json
import os
from pathlib import Path
from agent import TravelAgent
from planner import plan

ROOT = Path(__file__).resolve().parent

def load_env():
    path = ROOT / ".env"
    if path.exists():
        for line in path.read_text().splitlines():
            if line.strip() and not line.lstrip().startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                if k.strip() in {"AZURE_OPENAI_BASE_URL", "AZURE_OPENAI_API_KEY", "AZURE_OPENAI_DEPLOYMENT"}:
                    os.environ.setdefault(k.strip(), v.strip().strip("\"'"))

def safe_text(value):
    # Prevent model/provider text from injecting terminal escape sequences.
    return "".join(c for c in str(value) if c in "\n\t" or (c.isprintable() and c != "\x1b"))

def display(result):
    if result["status"] == "needs_clarification":
        print(safe_text("\n".join(result["questions"])))
        print(result["note"])
        return
    trip = result["plan"]
    print(f"\n{trip['destination']} | {result['status']} | ESTIMATES ONLY")
    print(f"Group total: INR {trip['estimated_total_inr']:,} | Remaining: INR {trip['remaining_inr']:,}")
    for category, amount in trip["budget_breakdown"].items():
        print(f"  {category.replace('_', ' ')}: INR {amount:,}")
    for day in trip["itinerary"]:
        print(f"Day {day['day']} ({day['date'] or 'date unspecified'}): " + "; ".join(day["activities"]))
    print(result["explanation"])
    print("Weather:", result["weather"]["status"])
    for assumption in result["assumptions"]:
        print("-", assumption)
    print("Sources:", ", ".join(trip["sources"]))

def main():
    parser = argparse.ArgumentParser(description="Roamwise travel planning prototype")
    parser.add_argument("--demo", action="store_true", help="Offline deterministic demo; no LLM or network")
    parser.add_argument("--budget", type=int, default=50000)
    parser.add_argument("--days", type=int, default=5)
    parser.add_argument("--people", type=int, default=2)
    args = parser.parse_args()
    load_env()
    if args.demo:
        print("OFFLINE DEMO: synthetic costs; no AI model or live data called.")
        display(plan({"origin": "Delhi", "days": args.days, "people": args.people,
                      "budget": args.budget, "interests": ["nature", "food"], "pace": "relaxed"}))
        return
    print("ROAMWISE | Azure travel agent | /save, /reset, /quit")
    print("Supported: Delhi to Rishikesh/Jaipur, 2–7 days, 1–8 travellers. Prices are estimates.")
    agent = TravelAgent()
    while True:
        try:
            text = input("\nYou: ").strip()
            if text == "/quit":
                break
            if text == "/reset":
                agent = TravelAgent()
                print("Trip state cleared.")
            elif text == "/save":
                if agent.last_plan:
                    out = ROOT / "output"
                    out.mkdir(exist_ok=True)
                    (out / "itinerary.json").write_text(json.dumps(agent.last_plan, indent=2), encoding="utf-8")
                    print("Saved output/itinerary.json (overwrites previous export).")
                else:
                    print("Create a plan first.")
            else:
                display(agent.reply(text))
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break
        except ValueError as exc:
            print("Please check:", safe_text(exc))

if __name__ == "__main__":
    main()
