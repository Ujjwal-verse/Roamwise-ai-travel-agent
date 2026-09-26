# Roamwise-ai-travel-agent
<<<<<<< HEAD
# roamwise-ai-travel-agent
=======
# Roamwise — AI Travel Agent

**Team:** Ujjwal Yadav, Kaustav Nandi, Ved Amrit

Requires Python 3.10+. No extra packages needed.

## Setup

1. Copy `.env.example` to `.env`.
2. Enter your Azure OpenAI endpoint ending in `/openai/v1`, private API key, and exact model deployment name.
3. Run `python3 app.py` from this folder.

Keep your API key private. `.gitignore` excludes `.env` from Git.

## Try it

Plan a 5-day trip from Delhi for 2 people under INR 50,000 total, focused on nature and food, with a relaxed itinerary.

Then: Make it 3 days under INR 20,000 total.

Commands: `/save` exports the latest itinerary, `/reset` clears the trip, `/quit` exits.
For an offline demo without an API key, run `python3 app.py --demo`.

## Files

- `app.py`: starts the agent and handles terminal input.
- `agent.py`: manages conversation and replanning.
- `planner.py`: validates preferences and builds budgeted itineraries.
- `providers.py`: connects to Azure and the weather API.
- `catalog.py`: contains destination data and cost assumptions.
- `.env.example`: configuration template.
- `.gitignore`: keeps private configuration out of Git.

## Current scope

Delhi departures to Rishikesh or Jaipur; 2–7 days and 1–8 travellers.
All costs are illustrative estimates, not live prices. No bookings are made.
Weather is optional and requires dates within the forecast window and network access.
The offline demo does not use AI. Live Azure inference requires your credentials and a
chat deployment supporting Chat Completions and JSON mode; it has not been verified here.
>>>>>>> 902a3d5 (Add AI travel agent with Azure Grok integration)
