from pydantic import BaseModel, Field
from typing import List, Literal

class GradeEvidence(BaseModel):
    grade : Literal["weak", "good"] = Field("good means evidence can answer the question; weak means not enough evidence.")