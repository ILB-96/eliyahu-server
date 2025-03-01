def set_cursor(pagination_type, start_cursor, end_cursor):
    if pagination_type == "after" and end_cursor:
        return f'"{end_cursor}"'

    return f'"{start_cursor}"' if start_cursor else "null"
