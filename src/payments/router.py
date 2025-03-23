from fastapi import APIRouter, Query, HTTPException, Request
import httpx

from .service import DonatorsQueryParams, DraftOrderParams
from . import utils
from . import ACCESS_TOKEN, API_URL

router = APIRouter()
client = httpx.AsyncClient(
    verify=True,
    headers={
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": ACCESS_TOKEN,
    },
)

@router.get("/donators")
async def read_donators(
    request: Request,
    params: DonatorsQueryParams = Query(...)
):
    curr_cursor = utils.set_cursor(params.paginationType, params.startCursor, params.endCursor)
    first_or_last = f"first: {params.limit}" if params.paginationType == "after" else "last: {limit}"
    curr_search_value = f" AND *{params.searchValue}" if params.searchValue else ""
    query_params = f"{first_or_last}, {params.paginationType}: {curr_cursor}, query: \"tag:'donator'{curr_search_value}\""
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


    response = await client.post(API_URL, headers=headers, json={"query": query})

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail="Error from Shopify API"
        )

    return response.json()


@router.get("/draft_order")
async def create_checkout(request: Request, params: DraftOrderParams = Query(...)):
    params = f"""
    input: {{
      lineItems: [{{
        generatePriceOverride: true,
        variantId: "gid://shopify/ProductVariant/{id}",
        quantity: {params.quantity},
        priceOverride: {{amount: {params.price}, currencyCode: ILS}}
      }}],
      note: "{params.note.replace('"', '\\"')}",
      tags: {params.tags}
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

    
    response = await client.post(API_URL, headers=headers, json={"query": query})

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail="Error from Shopify API"
        )

    return response.json()

async def shutdown_event():
    await client.aclose()
    
def register_events(app):
    app.add_event_handler("shutdown", shutdown_event)
