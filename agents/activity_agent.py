from config import get_llm
from utils.prompt_loader import load_prompts

llm = get_llm()
prompts = load_prompts()

def activity_agent(state):
    print("\n" + "="*60)
    print("🎯 ACTIVITY AGENT — Planning your daily adventures...")
    print("="*60)

    if not state.get("validated_input"):
        return {"activities": None}

    destination = state["validated_input"]["destination"]
    interests = state["validated_input"]["interests"]
    duration = state["validated_input"]["duration"]

    prompt = (
        f"{prompts['activity_prompt']}\n\n"
        f"Destination: {destination}\n"
        f"Interests  : {interests}\n"
        f"Duration   : {duration}"
    )

    response = llm.invoke(prompt)
    result = response.content

    print(result)
    return {"activities": result}
