import json
import os
from typing import Dict, Any, Optional, TypedDict
from langgraph.graph import StateGraph, END
from .schema import AppConfig
from .nodes import (
    generate_fallback_config,
    backend_designer_node,
    ui_architect_node,
    validator_node,
)
# --- 3. GRAPH ORCHESTRATION ---
class GraphState(TypedDict):
    user_input: str
    config: AppConfig
    error_log: Optional[str]
    is_valid: bool
workflow = StateGraph(GraphState)
workflow.add_node("backend_designer", backend_designer_node)
workflow.add_node("ui_architect", ui_architect_node)
workflow.add_node("validator", validator_node)
workflow.set_entry_point("backend_designer")
workflow.add_edge("backend_designer", "ui_architect")
workflow.add_edge("ui_architect", "validator")
workflow.add_conditional_edges(
    "validator",
    lambda state: "retry" if not state["is_valid"] else "end",
    {
        "retry": "backend_designer",
        "end": END,
    },
)
app = workflow.compile()
def generate_software_system(user_prompt: str) -> str:
    """The core entry point that orchestrates the LangGraph workflow."""
    if not os.getenv("GROQ_API_KEY"):
        config = generate_fallback_config(user_prompt)
        if hasattr(config, "model_dump_json"):
            return config.model_dump_json(indent=2)
        return json.dumps(config, indent=2)
    initial_state = {
        "user_input": user_prompt,
        "config": None,
        "error_log": None,
        "is_valid": False,
    }
    try:
        print(f"--- Starting Compiler Pipeline for: '{user_prompt}' ---")
        final_state = app.invoke(initial_state)
        config = final_state.get("config")
        if config and final_state.get("is_valid"):
            if hasattr(config, "model_dump_json"):
                return config.model_dump_json(indent=2)
            return json.dumps(config, indent=2)
        error_details = final_state.get("error_log", "Unknown compilation error.")
        failure_report = {
            "status": "failed",
            "error": error_details,
            "partial_config": str(config) if config else None,
        }
        return json.dumps(failure_report, indent=2)
    except Exception as e:
        error_msg = str(e)
        if "Invalid API Key" in error_msg or "invalid_api_key" in error_msg:
            fallback_config = generate_fallback_config(user_prompt)
            if hasattr(fallback_config, "model_dump_json"):
                return fallback_config.model_dump_json(indent=2)
            return json.dumps(fallback_config, indent=2)
        return json.dumps({"status": "error", "message": error_msg})
