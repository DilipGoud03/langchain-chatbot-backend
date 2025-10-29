import re

# ------------------------------------------------------------
# Module: utility_service
# Description:
#   Provides utility helper functions for text and SQL processing.
#   - Cleans AI-generated SQL queries by removing markdown syntax,
#     formatting inconsistencies, and extraneous text.
# ------------------------------------------------------------


class UtilityService:
    # ------------------------------------------------------------
    # Method: __init__
    # Description:
    #   Initializes the UtilityService.
    #   Prints an initialization message for debugging/logging.
    # ------------------------------------------------------------
    def __init__(self):
        print("UtilityService initialized")

    # ------------------------------------------------------------
    # Method: clean_sql_query
    # Description:
    #   Cleans and normalizes SQL query text (especially from AI output).
    #
    # Workflow:
    #     1. Removes markdown code block syntax (```sql ... ```).
    #     2. Removes prefixes like “SQLQuery:” or “SQL:”.
    #     3. Extracts only the main SQL statement (starting from SELECT).
    #     4. Removes backticks from identifiers.
    #     5. Normalizes whitespace.
    #     6. Adds line breaks before key SQL clauses for readability.
    #
    # Parameters:
    #   - text (str): The raw SQL text input.
    #
    # Returns:
    #   - str: The cleaned and formatted SQL query.
    # ------------------------------------------------------------
    def clean_sql_query(self, text: str) -> str:
        # Step 1: Remove code block syntax and SQL-related tags
        block_pattern = r"```(?:sql|SQL|SQLQuery|mysql|postgresql)?\s*(.*?)\s*```"
        text = re.sub(block_pattern, r"\1", text, flags=re.DOTALL)

        # Step 2: Remove "SQLQuery" or similar prefixes
        prefix_pattern = r"^(?:SQL\s*Query|SQLQuery|MySQL|PostgreSQL|SQL)\s*:\s*"
        text = re.sub(prefix_pattern, "", text, flags=re.IGNORECASE)

        # Step 3: Extract the first SQL statement (starting from SELECT)
        sql_statement_pattern = r"(SELECT.*?;)"
        sql_match = re.search(sql_statement_pattern, text, flags=re.IGNORECASE | re.DOTALL)
        if sql_match:
            text = sql_match.group(1)

        # Step 4: Remove backticks around identifiers
        text = re.sub(r'`([^`]*)`', r'\1', text)

        # Step 5: Normalize whitespace
        text = re.sub(r'\s+', ' ', text)

        # Step 6: Add line breaks before main SQL keywords
        keywords = ['SELECT', 'FROM', 'WHERE', 'GROUP BY']
        pattern = '|'.join(r'\b{}\b'.format(k) for k in keywords)
        text = re.sub(f'({pattern})', r'\n\1', text, flags=re.IGNORECASE)

        # Step 7: Final cleanup (trim and remove extra newlines)
        text = text.strip()
        text = re.sub(r'\n\s*\n', '\n', text)

        return text
