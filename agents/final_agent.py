from config import get_llm
from utils.prompt_loader import load_prompts

llm = get_llm()
prompts = load_prompts()

def final_agent(state):
    print("\n" + "="*60)
    print("📋 FINAL AGENT — Compiling your complete itinerary...")
    print("="*60)

    if not state.get("validated_input"):
        return {"final_itinerary": None}

    vi = state["validated_input"]

    summary = (
        f"Destination : {vi['destination']}\n"
        f"Duration    : {vi['duration']}\n"
        f"Budget      : {vi['budget']}\n"
        f"Interests   : {vi['interests']}\n\n"
        f"--- HOTELS ---\n{state.get('hotels', 'N/A')}\n\n"
        f"--- MEALS ---\n{state.get('meals', 'N/A')}\n\n"
        f"--- ACTIVITIES ---\n{state.get('activities', 'N/A')}\n\n"
        f"--- TRANSPORT ---\n{state.get('transport', 'N/A')}\n\n"
        f"--- BUDGET ESTIMATE ---\n{state.get('budget_estimate', 'N/A')}"
    )

    prompt = f"{prompts['final_prompt']}\n\n{summary}"

    response = llm.invoke(prompt)
    result = response.content

    print("\n" + "🌟"*30)
    print("\n✈️  YOUR COMPLETE TRAVEL ITINERARY\n")
    print("🌟"*30)
    print(result)

    return {"final_itinerary": result}
