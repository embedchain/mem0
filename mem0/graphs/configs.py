from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator

class Neo4jConfig(BaseModel):
    url: Optional[str] = Field(None, description="Host address for the graph database")
    username: Optional[str] = Field(None, description="Username for the graph database")
    password: Optional[str] = Field(None, description="Password for the graph database")

    @model_validator(mode="before")
    def check_host_port_or_path(cls, values):
        url, username, password = (
            values.get("url"),
            values.get("username"),
            values.get("password"),
        )
        if not url and not username and not password:
            raise ValueError(
                "Please provide 'url', 'username' and 'password'."
            )
        return values


class GraphStoreConfig(BaseModel):
    provider: str = Field(
        description="Provider of the data store (e.g., 'neo4j')", 
        default=None
    )
    config: Neo4jConfig = Field(
        description="Configuration for the specific data store",
        default=None
    )

    @field_validator("config")
    def validate_config(cls, v, values):
        provider = values.data.get("provider")
        if provider == "neo4j":
            return Neo4jConfig(**v.model_dump())
        else:
            raise ValueError(f"Unsupported graph store provider: {provider}")