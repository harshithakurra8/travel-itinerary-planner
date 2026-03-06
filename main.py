from dotenv import load_dotenv
load_dotenv()

from graph.workflow import graph


def run_planner(user_input: dict):
    """Run the travel itinerary planner for the given input."""
    print("\n" + "*"*20)
    print("        TRAVEL ITINERARY PLANNER  ")
    print("*"*20)
    print(f"\nPlanning trip to: {user_input.get('destination', 'N/A')}")
    print(f"Duration        : {user_input.get('duration', 'N/A')}")
    print(f"Budget          : {user_input.get('budget', 'N/A')}")
    print(f"Interests       : {user_input.get('interests', 'N/A')}")

    result = graph.invoke({"input": user_input})

    # Surface error if validation failed
    if result.get("error") and not result.get("final_itinerary"):
        
        print("\n COULD NOT GENERATE ITINERARY")
        
        print(f"\n{result['error']}\n")
        return result

    return result


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    # ── Interactive mode ───────────────────────────────────────
    if len(sys.argv) == 1:
        print("\nWelcome to the Travel Itinerary Planner!")
        print("─" * 45)
        destination = input(" Enter destination (city/country): ").strip()
        duration    = input(" Enter trip duration (e.g. 5 days): ").strip()
        budget      = input("Enter budget level (low/medium/high): ").strip()
        interests   = input(" Enter your interests (e.g. art, food): ").strip()

        user_input = {
            "destination": destination,
            "duration":    duration,
            "budget":      budget,
            "interests":   interests,
        }
        run_planner(user_input)

    # ── Demo modes ─────────────────────────────────────────────
    elif sys.argv[1] == "--demo-valid":
        # Valid input demo
        run_planner({
            "destination": "Paris",
            "duration":    "5 days",
            "budget":      "medium",
            "interests":   "art, food, history",
        })

    elif sys.argv[1] == "--demo-invalid":
        # Invalid input demo (missing destination)
        run_planner({
            "destination": "",
            "duration":    "5 days",
            "budget":      "extreme",   # also invalid budget
            "interests":   "adventure",
        })

    elif sys.argv[1] == "--demo-fake-city":
        # Invalid destination demo
        run_planner({
            "destination": "Xyzabc",
            "duration":    "3 days",
            "budget":      "low",
            "interests":   "hiking",
        })

    else:
        print("Usage:")
        print("  python main.py                  # interactive mode")
        print("  python main.py --demo-valid     # run with Paris example")
        print("  python main.py --demo-invalid   # run with bad input")
        print("  python main.py --demo-fake-city # run with fake destination")
