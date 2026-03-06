from config import get_llm
from utils.prompt_loader import load_prompts

llm = get_llm()
prompts = load_prompts()

def transport_agent(state):
    print("\n" + "="*60)
    print("🚌 TRANSPORT AGENT — Mapping out how you'll get around...")
    print("="*60)

    if not state.get("validated_input"):
        return {"transport": None}

    destination = state["validated_input"]["destination"]
    budget = state["validated_input"]["budget"]

    prompt = (
        f"{prompts['transport_prompt']}\n\n"
        f"Destination : {destination}\n"
        f"Budget level: {budget}"
    )

    response = llm.invoke(prompt)
    result = response.content

    print(result)
    return {"transport": result}
