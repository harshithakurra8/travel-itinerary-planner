from config import get_llm
from utils.prompt_loader import load_prompts

llm = get_llm()
prompts = load_prompts()

def budget_agent(state):
    print("\n" + "="*60)
    print("💰 BUDGET AGENT — Estimating your total travel costs...")
    print("="*60)

    if not state.get("validated_input"):
        return {"budget_estimate": None}

    destination = state["validated_input"]["destination"]
    duration = state["validated_input"]["duration"]
    budget_level = state["validated_input"]["budget"]

    context = (
        f"Destination  : {destination}\n"
        f"Duration     : {duration}\n"
        f"Budget level : {budget_level}\n\n"
        f"Hotels info  :\n{state.get('hotels', 'N/A')}\n\n"
        f"Meals info   :\n{state.get('meals', 'N/A')}\n\n"
        f"Activities   :\n{state.get('activities', 'N/A')}\n\n"
        f"Transport    :\n{state.get('transport', 'N/A')}"
    )

    prompt = f"{prompts['budget_prompt']}\n\n{context}"

    response = llm.invoke(prompt)
    result = response.content

    print(result)
    return {"budget_estimate": result}
