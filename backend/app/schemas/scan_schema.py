from pydantic import BaseModel

class ScanRequest(BaseModel):
    raw_text: str


### Response Schema

from typing import List

class IngedientResult(BaseModel):
    name: str
    status: str
    category: str
    description: str

class ScanResponse(BaseModel):
    ingredients: List[IngedientResult]