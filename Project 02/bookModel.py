from pydantic import BaseModel, Field
from typing import Optional

class BookModel(BaseModel):
    id : Optional[int] = Field(description='id is not neeeded on create', default = None)
    title : str = Field(min_length=3, max_length=20)
    author : str = Field(min_length=1)
    description : str = Field(min_length=1, max_length=100)
    rating : int = Field(gt = 0, lt = 6)   #1 to 5
    published_date : int = Field(gt=1999, le=2030)

    model_config = {
        "json_schema_extra" : {
            "example" : {
                "title" : "A new book",
                "author" : "rahat",
                "description" : "des 2",
                "rating" : 5,
                "published_date" : 2012
                

            }
        }
    }