from config import get_llm
from utils.prompt_loader import load_prompts

llm = get_llm()
prompts = load_prompts()

def meal_agent(state):
    print("\n" + "="*60)
    print("🍽️  MEAL AGENT — Crafting your daily food journey...")
    print("="*60)

    if not state.get("validated_input"):
        return {"meals": None}

    destination = state["validated_input"]["destination"]
    duration = state["validated_input"]["duration"]
    budget = state["validated_input"]["budget"]

    prompt = (
        f"{prompts['meal_prompt']}\n\n"
        f"Destination : {destination}\n"
        f"Duration    : {duration}\n"
        f"Budget level: {budget}"
    )

    response = llm.invoke(prompt)
    result = response.content

    print(result)
    return {"meals": result}
