from pydantic import BaseModel, Field, field_validator
class DonatorsQueryParams(BaseModel):
    paginationType: str = Field("after", regex="^(after|before)$")
    limit: int = Field(20, gt=0)
    searchValue: str = None
    startCursor: str = None
    endCursor: str = None

    @field_validator("searchValue")
    def sanitize_search_value(cls, v):
        # Allow only alphanumeric, spaces, and a few safe punctuation characters.
        # Adjust the regex as needed for your allowed characters.
        if v and not all(char.isalnum() or char.isspace() or char in "-_.*" for char in v):
            raise ValueError("Invalid characters in searchValue")
        return v
    
class DraftOrderParams(BaseModel):
    quantity: int = Field(1, gt=0)
    price: float = Field(18.00, gt=18.00)
    note: str = '[{"f":"אהרון","m":"שני","g":"בן"}]'
    tags: str = '["שני בן אהרון", "donator"]'
    id: str = "45136044949635"
