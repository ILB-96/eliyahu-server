from fastapi import APIRouter, Query, HTTPException, Request
import httpx
from . import utils
from . import ACCESS_TOKEN, API_URL

router = APIRouter()

@router.get("/donators")
async def read_donators(
    request: Request,
    paginationType: str = Query("after", regex="^(after|before)$"),
    limit: int = Query(20, gt=0),
    searchValue: str = None,
    startCursor: str = None,
    endCursor: str = None,
):
    curr_cursor = utils.set_cursor(paginationType, startCursor, endCursor)
    first_or_last = f"first: {limit}" if paginationType == "after" else "last: {limit}"
    curr_search_value = f" AND *{searchValue}" if searchValue else ""
    query_params = f"{first_or_last}, {paginationType}: {curr_cursor}, query: \"tag:'donator'{curr_search_value}\""
    pageInfo_params = "hasNextPage hasPreviousPage startCursor endCursor"
    query = utils.set_query(
        "orders",
        query_params,
        "note",
        pageInfo_params=pageInfo_params,
    )
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": ACCESS_TOKEN,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(API_URL, headers=headers, json={"query": query})

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail="Error from Shopify API"
        )

    return response.json()


@router.get("/draft_order")
async def create_checkout(request: Request, quantity: int=1, price: float=18.00, note: str='[{"f":"אהרון","m":"שני","g":"בן"}]', tags: str='["שני בן אהרון", "donator"]', id: str= "45136044949635",):
    params = f"""
    input: {{
      lineItems: [{{
        generatePriceOverride: true,
        variantId: "gid://shopify/ProductVariant/{id}",
        quantity: {quantity},
        priceOverride: {{amount: {price}, currencyCode: ILS}}
      }}],
      note: "{note.replace('"', '\\"')}",
      tags: {tags}
    }}
    """
    return_params = "draftOrder { invoiceUrl }"
    query = utils.set_mutation(
        "draftOrderCreate",
        params,
        return_params,
    )
    
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": ACCESS_TOKEN,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(API_URL, headers=headers, json={"query": query})

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail="Error from Shopify API"
        )

    return response.json()
