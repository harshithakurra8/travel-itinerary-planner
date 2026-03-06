from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional

from agents.validator_agent import validate_input
from agents.hotel_agent import hotel_agent
from agents.meal_agent import meal_agent
from agents.activity_agent import activity_agent
from agents.transport_agent import transport_agent
from agents.budget_agent import budget_agent
from agents.final_agent import final_agent


# ── Typed state schema ─────────────────────────────────────────────────────────
class TravelState(TypedDict, total=False):
    input: dict
    validated_input: Optional[dict]
    error: Optional[str]
    hotels: Optional[str]
    meals: Optional[str]
    activities: Optional[str]
    transport: Optional[str]
    budget_estimate: Optional[str]
    final_itinerary: Optional[str]


# ── Routing: skip pipeline if validation failed ────────────────────────────────
def route_after_validation(state: TravelState) -> str:
    if state.get("error") or not state.get("validated_input"):
        return "error_end"
    return "hotels"


def error_end(state: TravelState) -> TravelState:
    """Terminal node that surfaces the validation error."""
    print("\n" + "="*60)
    print("🚫 PIPELINE ABORTED")
    print("="*60)
    print(state.get("error", "Unknown validation error."))
    print("\nPlease fix the issues above and try again.")
    return state


# ── Build the graph ────────────────────────────────────────────────────────────
workflow = StateGraph(TravelState)

workflow.add_node("validator",  validate_input)
workflow.add_node("error_end",  error_end)
workflow.add_node("hotels",     hotel_agent)
workflow.add_node("meals",      meal_agent)
workflow.add_node("activities", activity_agent)
workflow.add_node("transport",  transport_agent)
workflow.add_node("budget",     budget_agent)
workflow.add_node("final",      final_agent)

workflow.set_entry_point("validator")

# Conditional branch after validation
workflow.add_conditional_edges(
    "validator",
    route_after_validation,
    {
        "hotels":    "hotels",
        "error_end": "error_end",
    },
)

# Happy path
workflow.add_edge("hotels",     "meals")
workflow.add_edge("meals",      "activities")
workflow.add_edge("activities", "transport")
workflow.add_edge("transport",  "budget")
workflow.add_edge("budget",     "final")

# Terminal edges
workflow.add_edge("final",     END)
workflow.add_edge("error_end", END)

graph = workflow.compile()
