from pydantic import BaseModel, Field, field_validator
from typing import Literal

class TaskCreate(BaseModel):

    title: str = Field(min_length=3,max_length=50)
    priority: Literal["low", "medium", "high"]
    description: str | None = Field(default="No description")

    
    @field_validator("title")
    @classmethod
    def checkUppercase(cls,value):
        if not value[0].isupper():
            raise ValueError(f"Warning title {value} should start with an uppercase letter")
        return value 

class TaskUpdate(BaseModel):

    title: str | None = Field(default=None, min_length=3,max_length=50)
    priority:  Literal["low", "medium", "high"] | None = None
    description: str | None = Field(default="No description")

    @field_validator("title")
    @classmethod
    def checkUppercase(cls,value):
        if value and not value[0].isupper():
            raise ValueError(f"Warning title {value} should start with an uppercase letter")
        return value

    
class TaskResponse(BaseModel):
    task_id: int
    title: str
    priority: str
    description: str
    status: str

    @field_validator("title")
    @classmethod
    def checkUppercase(cls,value):
        if not value[0].isupper():
            raise ValueError(f"Warning title {value} should start with an uppercase letter")
        return value  


# Demonstrate serialization
if __name__ == "__main__":
    task = TaskCreate(
        title="Study FastAPI",
        priority="high"
    )

    print(task.model_dump())
    print(type(task.model_dump()))

    print(task.model_dump_json())
    print(type(task.model_dump_json()))

