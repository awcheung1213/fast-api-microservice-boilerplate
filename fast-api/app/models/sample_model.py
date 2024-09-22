from datetime import datetime
from pydantic import AfterValidator, BaseModel, Field, UUID5
from typing import Annotated, Dict, List, Optional
from uuid import UUID


class SampleModel(BaseModel): #A sample model containing various types of data for a product order
    id: UUID5 | Annotated[str, AfterValidator(lambda x: UUID(x, version=5))]
    name: str = Field(..., description="A string value representing the name")
    quantity: int = Field(..., ge=0, description="An integer representing quantity in stock")
    price: float = Field(..., gt=0, description="A floating point value for price")
    created: Optional[datetime] = Field(default_factory=datetime.now(datetime.timezone.utc), description="A timestamp for when the record is created")
    is_available: Optional[bool] = Field(default=True, description="A boolean indicating availability")
    metadata: Optional[Dict[str, str]] = Field(default_factory=dict, description="A dictionary for storing metadata")
    categories: Optional[List[str]] = Field(default_factory=list, description="A list of categories")
