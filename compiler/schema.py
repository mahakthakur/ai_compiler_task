from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class Entity(BaseModel):
    name: str = Field(description="Name of the DB table")
    fields: List[str] = Field(description="Columns with types (e.g., 'id: integer')")


class APIEndpoint(BaseModel):
    path: str
    method: Literal["GET", "POST", "PUT", "DELETE"]
    description: str


class UIComponent(BaseModel):
    component_type: Literal["Navbar", "DataTable", "Form", "Chart", "Card"]
    label: str
    data_source: str = Field(description="The API endpoint this component connects to")
    props: List[str]


class Page(BaseModel):
    route: str
    title: str
    components: List[UIComponent]


class AppConfig(BaseModel):
    app_name: str
    entities: List[Entity]
    endpoints: List[APIEndpoint]
    ui_layout: List[Page]
    is_valid: bool = False
    error_log: Optional[str] = None
