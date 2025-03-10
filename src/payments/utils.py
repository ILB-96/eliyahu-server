def set_cursor(pagination_type, start_cursor, end_cursor):
    if pagination_type == "after" and end_cursor:
        return f'"{end_cursor}"'

    return f'"{start_cursor}"' if start_cursor else "null"


def set_query(query_type, table_name, params, node_params, pageInfo_params):
    return f"""
    {query_type} {{
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
