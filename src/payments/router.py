from typing import Annotated
from fastapi import APIRouter, Query, Request
from .service import DonatorsQueryParams, DraftOrderParams
from . import utils

router = APIRouter()

@router.get("/donators")
async def read_donators(
    request: Request,
    data: Annotated[DonatorsQueryParams, Query()]
) -> dict:
    data.set_cursor().set_first_or_last().set_search_value() \
        .build_query_params().build_page_info_params().build_query()

    result = await utils.post_to_api(data.query, request)
    return result


@router.get("/draft_order")
async def create_checkout(request: Request, data: Annotated[DraftOrderParams, Query()]):
    data.set_params().set_return_params().build_mutation()
    
    result = await utils.post_to_api(data.mutation, request)
    return result["data"]["draftOrderCreate"]
