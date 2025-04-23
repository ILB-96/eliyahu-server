from fastapi import HTTPException, Request
from src.constants import API_URL

def set_cursor(pagination_type, start_cursor, end_cursor):
    if pagination_type == "after" and end_cursor:
        return f'"{end_cursor}"'

    return f'"{start_cursor}"' if start_cursor else "null"


def set_query(table_name, params, node_params, page_info_params):
    return f"""
    query {{
      {table_name}({params}) {{
        edges {{
          node {{
            {node_params}
          }}
        }}
        pageInfo {{
          {page_info_params}
        }}
      }}
    }}
    """

def set_mutation(table_name, params, return_params):
    return f"""
    mutation {{
      {table_name}({params}) {{
        {return_params}
        userErrors {{
          field
          message
        }}
      }}
    }}
    """

async def post_to_api(query: str, request: Request) -> dict:
    """Helper function to make a POST request to the API and return its JSON data."""
    response = await request.app.state.client.post(API_URL, json={"query": query})
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail="Error from Shopify API"
        )
    return response.json()