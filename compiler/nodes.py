import json
import os
import re
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from .schema import AppConfig, Entity, APIEndpoint, UIComponent, Page

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model_name="openai/gpt-oss-120b",
    temperature=0,
    groq_api_key=GROQ_API_KEY,
    response_format={"type": "json_object"}
)
structured_llm = llm.with_structured_output(AppConfig)


def generate_fallback_config(user_prompt: str) -> AppConfig:
    prompt = user_prompt.lower()
    entities = []
    endpoints = []
    pages = []

    def title_from_prompt(text: str) -> str:
        words = re.findall(r"[a-z0-9]+", text.lower())
        return " ".join(word.capitalize() for word in words[:4]) or "Fallback App"

    app_name = title_from_prompt(user_prompt)

    if any(keyword in prompt for keyword in ['product', 'inventory', 'catalog', 'store', 'shop', 'item']):
        entities.append(Entity(name="Product", fields=["id: integer", "name: string", "quantity: integer", "price: float"]))
        endpoints.extend([
            APIEndpoint(path="/products", method="GET", description="List all products."),
            APIEndpoint(path="/products", method="POST", description="Create a new product."),
            APIEndpoint(path="/products/{id}", method="PUT", description="Update a product."),
            APIEndpoint(path="/products/{id}", method="DELETE", description="Delete a product."),
        ])
        pages.append(Page(
            route="/products",
            title="Products",
            components=[
                UIComponent(component_type="DataTable", label="Product Inventory", data_source="/products", props=["id", "name", "quantity", "price"]),
                UIComponent(component_type="Form", label="Add Product", data_source="/products", props=["name", "quantity", "price"]),
            ]
        ))
    elif any(keyword in prompt for keyword in ['task', 'task management', 'tasks', 'todo']):
        entities.append(Entity(name="Task", fields=["id: integer", "title: string", "status: string", "due_date: date"]))
        endpoints.extend([
            APIEndpoint(path="/tasks", method="GET", description="List all tasks."),
            APIEndpoint(path="/tasks", method="POST", description="Create a new task."),
            APIEndpoint(path="/tasks/{id}", method="PUT", description="Update a task."),
            APIEndpoint(path="/tasks/{id}", method="DELETE", description="Delete a task."),
        ])
        pages.append(Page(
            route="/tasks",
            title="Tasks",
            components=[
                UIComponent(component_type="DataTable", label="Task Board", data_source="/tasks", props=["title", "status", "due_date"]),
                UIComponent(component_type="Form", label="Add Task", data_source="/tasks", props=["title", "status", "due_date"]),
            ]
        ))
    elif any(keyword in prompt for keyword in ['crm', 'customer', 'sales', 'client']):
        entities.append(Entity(name="Customer", fields=["id: integer", "name: string", "email: string", "status: string"]))
        endpoints.extend([
            APIEndpoint(path="/customers", method="GET", description="List all customers."),
            APIEndpoint(path="/customers", method="POST", description="Create a new customer."),
            APIEndpoint(path="/customers/{id}", method="PUT", description="Update a customer."),
            APIEndpoint(path="/customers/{id}", method="DELETE", description="Delete a customer."),
        ])
        pages.append(Page(
            route="/customers",
            title="Customers",
            components=[
                UIComponent(component_type="DataTable", label="Customer List", data_source="/customers", props=["name", "email", "status"]),
                UIComponent(component_type="Form", label="Add Customer", data_source="/customers", props=["name", "email", "status"]),
            ]
        ))
    elif any(keyword in prompt for keyword in ['crypto', 'finance', 'bank', 'wallet', 'payment']):
        entities.append(Entity(name="Account", fields=["id: integer", "name: string", "balance: float", "status: string"]))
        endpoints.extend([
            APIEndpoint(path="/accounts", method="GET", description="List all accounts."),
            APIEndpoint(path="/accounts", method="POST", description="Create a new account."),
            APIEndpoint(path="/accounts/{id}", method="PUT", description="Update an account."),
            APIEndpoint(path="/accounts/{id}", method="DELETE", description="Delete an account."),
        ])
        pages.append(Page(
            route="/accounts",
            title="Accounts",
            components=[
                UIComponent(component_type="Card", label="Account Summary", data_source="/accounts", props=["name", "balance", "status"]),
                UIComponent(component_type="DataTable", label="Account Activity", data_source="/accounts", props=["name", "balance", "status"]),
            ]
        ))
    elif any(keyword in prompt for keyword in ['dashboard', 'analytics', 'report', 'stats']):
        entities.append(Entity(name="Report", fields=["id: integer", "title: string", "value: float", "updated_at: date"]))
        endpoints.extend([
            APIEndpoint(path="/reports", method="GET", description="List all reports."),
            APIEndpoint(path="/reports", method="POST", description="Create a new report."),
        ])
        pages.append(Page(
            route="/dashboard",
            title="Dashboard",
            components=[
                UIComponent(component_type="Chart", label="Performance Chart", data_source="/reports", props=["title", "value"]),
                UIComponent(component_type="Card", label="Summary Cards", data_source="/reports", props=["title", "value"]),
            ]
        ))
    else:
        entities.append(Entity(name="Item", fields=["id: integer", "name: string", "description: string"]))
        endpoints.extend([
            APIEndpoint(path="/items", method="GET", description="List all items."),
            APIEndpoint(path="/items", method="POST", description="Create a new item."),
        ])
        pages.append(Page(
            route="/items",
            title="Items",
            components=[
                UIComponent(component_type="DataTable", label="Item List", data_source="/items", props=["name", "description"]),
                UIComponent(component_type="Form", label="Add Item", data_source="/items", props=["name", "description"]),
            ]
        ))

    return AppConfig(
        app_name=app_name,
        entities=entities,
        endpoints=endpoints,
        ui_layout=pages,
        is_valid=True,
        error_log=None,
    )


def repair_json(json_str: str) -> str:
    """Simple JSON repair engine to fix common issues like missing commas, quotes, etc."""
    json_str = re.sub(r'^[^{]*', '', json_str)
    json_str = re.sub(r'[^}]*$', '', json_str)
    json_str = re.sub(r'"\s*"([^\"]*)"\s*:', r'"\1":', json_str)
    json_str = re.sub(r'(\w+)\s*:', r'"\1":', json_str)
    json_str = re.sub(r',\s*}', '}', json_str)
    json_str = re.sub(r',\s*]', ']', json_str)
    json_str = re.sub(r"'([^']*)'", r'"\1"', json_str)
    return json_str


def validate_and_repair_config(raw_output: str) -> AppConfig:
    """Validate and repair the LLM output to ensure it's a valid AppConfig."""
    try:
        data = json.loads(raw_output)
        config = AppConfig(**data)
        return config
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Repairing malformed output: {e}")
        repaired_json = repair_json(raw_output)
        try:
            data = json.loads(repaired_json)
            config = AppConfig(**data)
            return config
        except Exception as e2:
            print(f"Repair failed: {e2}")
            return generate_fallback_config("default app")


def verify_execution(config: AppConfig):
    """Simulate a runtime check of UI components against API endpoints."""
    valid_paths = {endpoint.path for endpoint in config.endpoints}
    for page in config.ui_layout:
        for component in page.components:
            if component.data_source not in valid_paths:
                return False
    return True


def backend_designer_node(state: Dict[str, Any]):
    """Stage 1: Design Database and API."""
    if not GROQ_API_KEY:
        return {"config": generate_fallback_config(state['user_input'])}

    prompt = f"""
    User Intent: {state['user_input']}
    Previous Errors to fix: {state.get('error_log', 'None')}

    Task: Generate the Backend (Entities and API Endpoints). 
    Ensure entities have clear fields and endpoints follow REST conventions.
    Keep ui_layout as an empty list [].

    Respond with valid JSON matching the AppConfig schema.
    """
    raw_output = llm.invoke(prompt).content
    config = validate_and_repair_config(raw_output)
    return {"config": config}


def ui_architect_node(state: Dict[str, Any]):
    """Stage 2: Design UI based on existing Backend."""
    current_config = state["config"]

    if not GROQ_API_KEY:
        return {"config": current_config}

    prompt = f"""
    User Intent: {state['user_input']}
    Existing Backend: {current_config.entities} and {current_config.endpoints}

    Task: Design the UI layout (Pages and Components). 
    CRITICAL: Every component's 'data_source' MUST match one of the API paths provided above.
    Return the FULL AppConfig including the entities and endpoints I gave you.

    Respond with valid JSON matching the AppConfig schema.
    """
    prediction = structured_llm.invoke(prompt)
    ui_config = validate_and_repair_config(prediction.model_dump_json() if hasattr(prediction, 'model_dump_json') else str(prediction))
    ui_config.entities = current_config.entities
    ui_config.endpoints = current_config.endpoints
    return {"config": ui_config}


def validator_node(state: Dict[str, Any]):
    """Stage 3: Validation logic."""
    config = state["config"]
    errors = []
    api_paths = [ep.path for ep in config.endpoints]
    for page in config.ui_layout:
        for comp in page.components:
            if comp.data_source not in api_paths:
                errors.append(f"UI Error: '{comp.label}' uses non-existent API '{comp.data_source}'")

    entity_names = [e.name.lower() for e in config.entities]
    for ep in config.endpoints:
        if not any(name in ep.path.lower() for name in entity_names):
            errors.append(f"API Error: Endpoint '{ep.path}' relates to no known Entity.")

    if errors:
        error_msg = f"The UI and API are out of sync. Error: {errors[0]}. Please regenerate the UI component to match the API path exactly."
        config.is_valid = False
        config.error_log = error_msg
        return {"is_valid": False, "error_log": error_msg, "config": config}

    if not verify_execution(config):
        error_msg = "Execution verification failed: the UI cannot be instantiated from the generated API endpoints."
        config.is_valid = False
        config.error_log = error_msg
        return {"is_valid": False, "error_log": error_msg, "config": config}

    config.is_valid = True
    config.error_log = None
    return {"is_valid": True, "error_log": None, "config": config}
