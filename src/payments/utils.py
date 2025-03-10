def set_cursor(pagination_type, start_cursor, end_cursor):
    if pagination_type == "after" and end_cursor:
        return f'"{end_cursor}"'

    return f'"{start_cursor}"' if start_cursor else "null"


def set_query(table_name, params, node_params, pageInfo_params):
    return f"""
    query {{
      {table_name}({params}) {{
        edges {{
          node {{
            {node_params}
          }}
        }}
        pageInfo {{
          {pageInfo_params}
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
