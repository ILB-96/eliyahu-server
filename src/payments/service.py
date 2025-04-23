from typing import Optional
from pydantic import BaseModel, Field

from . import utils

class DonatorsQueryParams(BaseModel):
    paginationType: str = Field("after", pattern="^(after|before)$")
    limit: int = Field(20, gt=0)
    searchValue: Optional[str] = Field(None, pattern=r'^[\u0590-\u05FFa-zA-Z ]*$')
    startCursor: Optional[str] = None
    endCursor: Optional[str] = None

    curr_cursor: Optional[str] = None
    first_or_last: Optional[str] = None
    curr_search_value: Optional[str] = None
    query_params: Optional[str] = None
    page_info_params: Optional[str] = None
    query: Optional[str] = None
    def set_cursor(self) -> "QueryBuilder":
        self.curr_cursor = utils.set_cursor(
            self.paginationType, self.startCursor, self.endCursor
        )
        return self

    def set_first_or_last(self) -> "QueryBuilder":
        self.first_or_last = (
            f"first: {self.limit}"
            if self.paginationType == "after"
            else f"last: {self.limit}"
        )
        return self

    def set_search_value(self) -> "QueryBuilder":
        self.curr_search_value = f" AND *{self.searchValue}" if self.searchValue else ""
        return self

    def build_query_params(self) -> "QueryBuilder":
        self.query_params = (
            f"{self.first_or_last}, {self.paginationType}: {self.curr_cursor}, "
            f'query: "tag:\'donator\'{self.curr_search_value}"'
        )
        return self

    def build_page_info_params(self) -> "QueryBuilder":
        self.page_info_params = "hasNextPage hasPreviousPage startCursor endCursor"
        return self

    def build_query(self) -> "QueryBuilder":
        self.query = utils.set_query(
            "orders",
            self.query_params,
            "note",
            page_info_params=self.page_info_params,
        )
        return self
    
class DraftOrderParams(BaseModel):
    quantity: int = Field(1, gt=0)
    price: float = Field(18.00, ge=18.00)
    note: str = '[{"f":"אהרון","m":"שני","g":"בן"}]'
    tags: str = '["שני בן אהרון", "donator"]'
    id: str = "45136044949635"

    params: Optional[str] = None
    return_params: Optional[str] = None
    mutation: Optional[str] = None
    def set_params(self):
        self.params = f"""
    input: {{
      lineItems: [{{
        generatePriceOverride: true,
        variantId: "gid://shopify/ProductVariant/{self.id}",
        quantity: {self.quantity},
        priceOverride: {{amount: {self.price}, currencyCode: ILS}}
      }}],
      note: "{self.note.replace('"', '\\"')}",
      tags: {self.tags}
    }}
    """
        return self
    def set_return_params(self):
        self.return_params = "draftOrder { invoiceUrl }"
        return self
    def build_mutation(self):
        self.mutation = utils.set_mutation(
        "draftOrderCreate",
        self.params,
        self.return_params,
        )
