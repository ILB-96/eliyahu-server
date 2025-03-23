from pydantic import BaseModel, Field
class DonatorsQueryParams(BaseModel):
    paginationType: str = Field("after", pattern="^(after|before)$")
    limit: int = Field(20, gt=0)
    searchValue: str = Field(None, pattern=r'^[\u0590-\u05FFa-zA-Z ]*$')
    startCursor: str = None
    endCursor: str = None
    
class DraftOrderParams(BaseModel):
    quantity: int = Field(1, gt=0)
    price: float = Field(18.00, ge=18.00)
    note: str = '[{"f":"אהרון","m":"שני","g":"בן"}]'
    tags: str = '["שני בן אהרון", "donator"]'
    id: str = "45136044949635"
