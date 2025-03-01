import logging
from fastapi import APIRouter, Query, HTTPException
import httpx
from . import utils
from . import ACCESS_TOKEN, API_URL

router = APIRouter()


@router.get("/donators")
async def read_donators(
    paginationType: str = Query("after", regex="^(after|before)$"),
    limit: int = Query(20, gt=0),
    searchValue: str = None,
    startCursor: str = None,
    endCursor: str = None,
):
    logging.debug("HEYYY" + ACCESS_TOKEN)

    curr_cursor = utils.set_cursor(paginationType, startCursor, endCursor)
    first_or_last = f"first: {limit}" if paginationType == "after" else "last: {limit}"
    curr_search_value = f" AND *{searchValue} " if searchValue else ""
    query_params = f"{first_or_last}, {paginationType}: {curr_cursor}, query: 'tag:donator{curr_search_value}'"

    query = f"""
    query {{
      orders({query_params}) {{
        edges {{
          node {{
            note
          }}
        }}
        pageInfo {{
          hasNextPage
          hasPreviousPage
          startCursor
          endCursor
        }}
      }}
    }}
    """
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


@router.get("/payment")
async def get_payment(data: dict):
    return "payment"


@router.post("/create_donator_checktout")
async def create_checkout(data: dict):
    return "checkout"


@router.post("/create_bundle_checkout")
async def create_bundle_checkout(data: dict):
    return "bundle_checkout"
