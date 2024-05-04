import sys
import sqlvalidator

def extract_query_lines(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            queries = [line.split("query: '")[1].rstrip("\n'") for line in lines if line.strip().startswith("query:")]
        return queries
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return []

def format_and_validate_query(query, idx):
    query = query.replace('"', "'")
    query = f"SELECT {query} FROM table"
    print(f"Validating query line {idx}: {query}")
    try:
        sql_query = sqlvalidator.parse(query)
        if not sql_query.is_valid():
            print(sql_query.errors)
            for error in sql_query.errors:
                if "The argument of AND must be type boolean" in str(error):
                    print("Ignoring validation error:", error)
                else:
                    print(error)
                    return False
    except sqlvalidator.ValidationError as e:
        print("SQL validation error:", e)
        return False
    return True

file_paths = ['/configmap-vmalertrules.yaml']
invalid_queries = []

for file_path in file_paths:
    query_lines = extract_query_lines(file_path)
    for idx, query in enumerate(query_lines, start=1):
        if not format_and_validate_query(query, idx):
            sys.exit(1)

sys.exit(0)
