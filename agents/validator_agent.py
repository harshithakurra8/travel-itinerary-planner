from config import get_llm
from utils.prompt_loader import load_prompts

llm = get_llm()
prompts = load_prompts()

# Known unrecognizable or clearly fake destinations
INVALID_DESTINATIONS = {"asdfgh", "xyzabc", "nowhere", "fakecity", "randomplace"}

def validate_input(state):
    print("\n" + "="*60)
    print("🔍 VALIDATOR AGENT — Checking your travel input...")
    print("="*60)

    user_input = state.get("input", {})

    # ── Field presence checks ──────────────────────────────────
    missing = []
    if not user_input.get("destination", "").strip():
        missing.append("destination")
    if not user_input.get("duration", "").strip():
        missing.append("duration")
    if not user_input.get("budget", "").strip():
        missing.append("budget")
    if not user_input.get("interests", "").strip():
        missing.append("interests")

    if missing:
        msg = f"❌ Validation failed. Missing required fields: {', '.join(missing)}. Please provide all fields."
        print(msg)
        return {"error": msg, "validated_input": None}

    # ── Budget value check ─────────────────────────────────────
    budget = user_input["budget"].strip().lower()
    if budget not in {"low", "medium", "high"}:
        msg = f"❌ Invalid budget '{user_input['budget']}'. Please use one of: low, medium, high."
        print(msg)
        return {"error": msg, "validated_input": None}

    # ── Destination sanity check via LLM ──────────────────────
    destination = user_input["destination"].strip()
    if destination.lower() in INVALID_DESTINATIONS:
        msg = f"❌ '{destination}' is not a recognizable destination. Please enter a valid city or country."
        print(msg)
        return {"error": msg, "validated_input": None}

    validation_prompt = (
        f"{prompts['validator_prompt']}\n\n"
        f"Destination: {destination}\n"
        f"Duration: {user_input['duration']}\n"
        f"Budget: {budget}\n"
        f"Interests: {user_input['interests']}\n\n"
        "Reply with VALID if everything looks good, otherwise reply with INVALID followed by a short reason."
    )
    response = llm.invoke(validation_prompt)
    verdict = response.content.strip()

    if verdict.upper().startswith("INVALID"):
        msg = f"❌ Input validation failed: {verdict}"
        print(msg)
        return {"error": msg, "validated_input": None}

    print(f"✅ Input validated successfully!")
    print(f"   📍 Destination : {destination}")
    print(f"   📅 Duration    : {user_input['duration']}")
    print(f"   💵 Budget      : {budget}")
    print(f"   🎯 Interests   : {user_input['interests']}")

    return {
        "validated_input": {
            "destination": destination,
            "duration": user_input["duration"].strip(),
            "budget": budget,
            "interests": user_input["interests"].strip(),
        }
    }
