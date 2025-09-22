import re


class UtilityService:
    def __init__(self):
        print("You are In utility service")
        pass

    def clean_sql_query(self, text: str) -> str:
        
        # step 1: remove code block syntax any SQL related tags
        block_pattern = r"```(?:sql|SQL|SQLQuery|mysql|postgresql)?\s*(.*?)\s*```"
        text = re.sub(block_pattern, r"\1", text, flags=re.DOTALL)

        # Step 2: Handle the "SQLQuery" prefix and similar variations
        prefix_pattern = r"^(?:SQL\s*Query|SQLQuery|MySQL|PostgreSQL|SQL)\s*:\s*"
        text = re.sub(prefix_pattern, "", text, flags=re.IGNORECASE)

        # step3: Extract the first SQL statement if there's random text after it
        sql_statement_pattern = r"(SELECT.*?;)"
        sql_match = re.search(sql_statement_pattern, text,
                              flags=re.IGNORECASE | re.DOTALL)

        if sql_match:
            text = sql_match.group(1)

        # step 4 : REmove backticks around identifiers
        text = re.sub(r'`([^`]*)`', r'\1', text)

        # step 5: Normalise whitespace
        text = re.sub(r'\s+', ' ', text)

        # step 6: Preserve newlines for main SQL keywords
        keywords = ['SELECT', 'FROM', 'WHERE', 'GROUP BY']

        # case sensitive replacement for keywords
        pattern = '|'.join(r'\b{}\b'.format(k) for k in keywords)
        text = re.sub(f'({pattern})', r'\n\1', text, flags=re.IGNORECASE)

        # Step 7:Final Cleanup

        # remove leading trailing whitespace
        text = text.strip()
        text = re.sub(r'\n\s*\n', '\n', text)

        return text
