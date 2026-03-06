from config import get_llm
from utils.prompt_loader import load_prompts

llm = get_llm()
prompts = load_prompts()

def hotel_agent(state):
    print("\n" + "="*60)
    print("🏨 HOTEL AGENT — Finding the best stays for you...")
    print("="*60)

    # Skip if validation failed
    if not state.get("validated_input"):
        return {"hotels": None}

    destination = state["validated_input"]["destination"]
    budget = state["validated_input"]["budget"]
    duration = state["validated_input"]["duration"]

    prompt = (
        f"{prompts['hotel_prompt']}\n\n"
        f"Destination : {destination}\n"
        f"Budget level: {budget}\n"
        f"Stay duration: {duration}"
    )

    response = llm.invoke(prompt)
    result = response.content

    print(result)
    return {"hotels": result}
