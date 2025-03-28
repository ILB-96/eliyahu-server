from typing import Annotated
from fastapi import APIRouter, Query, HTTPException, Request
from src.payments.service import DonatorsQueryParams, DraftOrderParams
from . import utils

router = APIRouter()

@router.get("/donators")
async def read_donators(
    request: Request,
    data: Annotated[DonatorsQueryParams, Query()]
):
    curr_cursor = utils.set_cursor(data.paginationType, data.startCursor, data.endCursor)
    first_or_last = f"first: {data.limit}" if data.paginationType == "after" else f"last: {data.limit}"
    curr_search_value = f" AND *{data.searchValue}" if data.searchValue else ""
    query_params = f"{first_or_last}, {data.paginationType}: {curr_cursor}, query: \"tag:'donator'{curr_search_value}\""
    pageInfo_params = "hasNextPage hasPreviousPage startCursor endCursor"
    query = utils.set_query(
        "orders",
        query_params,
        "note",
        pageInfo_params=pageInfo_params,
    )
    result = await utils.post_to_api(query, request)
    return result


@router.get("/draft_order")
async def create_checkout(request: Request, data: Annotated[DraftOrderParams, Query()]):
    params = f"""
    input: {{
      lineItems: [{{
        generatePriceOverride: true,
        variantId: "gid://shopify/ProductVariant/{data.id}",
        quantity: {data.quantity},
        priceOverride: {{amount: {data.price}, currencyCode: ILS}}
      }}],
      note: "{data.note.replace('"', '\\"')}",
      tags: {data.tags}
    }}
    """
    return_params = "draftOrder { invoiceUrl }"
    query = utils.set_mutation(
        "draftOrderCreate",
        params,
        return_params,
    )

    result = await utils.post_to_api(query, request)
    return result["data"]["draftOrderCreate"]
