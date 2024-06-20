import re

def prepend_schema(sql_query, schema="DATAWAREHOUSE"):
    """
    Ensure that schema and table names in the SQL query are properly quoted.
    """
    if sql_query is None:
        return None

    # Define a regex pattern to find occurrences of schema.table
    pattern = rf'\b{schema}\.FACTURACION\b'

    # Function to add double quotes around schema and table names
    def replacement(match):
        return f'"{schema}"."FACTURACION"'

    # Apply the replacement pattern to quote schema and table names
    modified_query = re.sub(pattern, replacement, sql_query, flags=re.IGNORECASE)

    return modified_query