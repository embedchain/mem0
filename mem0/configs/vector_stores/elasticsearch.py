from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, model_validator

class ElasticsearchDBConfig(BaseModel):
    collection_name: str = Field("mem0", description="Name of the collection")
    embedding_model_dims: int = Field(2048, description="Dimensions of the embedding model")
    metric_type: str = Field("dot_product", description="Metric type for similarity search")
    api_key: Optional[str] = Field(None, description="API key for Elasticsearch server")
    url: str = Field("http://localhost:9200", description="Full URL for Elasticsearch server")

    @model_validator(mode="before")
    @classmethod
    def validate_extra_fields(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        allowed_fields = set(cls.model_fields.keys())
        input_fields = set(values.keys())
        extra_fields = input_fields - allowed_fields
        if extra_fields:
            raise ValueError(
                f"Extra fields not allowed: {', '.join(extra_fields)}. Please input only the following fields: {', '.join(allowed_fields)}"
            )
        return values

    model_config = {
        "arbitrary_types_allowed": True,
    }

