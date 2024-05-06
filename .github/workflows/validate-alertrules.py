# import sys
# import sqlvalidator
# import subprocess

# def extract_query_lines(file_path):
#     try:
#         with open(file_path, 'r') as file:
#             lines = file.readlines()
#             queries = [line.split("query: '")[1].rstrip("\n'") for line in lines if line.strip().startswith("query:")]
#         return queries
#     except Exception as e:
#         print(f"Error reading file {file_path}: {e}")
#         return []

# def extract_query(file_path):
#     grep_command = ["grep", "^ *query:", file_path]
#     awk_command = ["awk", '{$1=""; print $0}']
    
#     try:
#         grep_process = subprocess.Popen(grep_command, stdout=subprocess.PIPE)
#         awk_process = subprocess.Popen(awk_command, stdin=grep_process.stdout, stdout=subprocess.PIPE)
#         grep_process.stdout.close()  # Close grep stdout to allow awk to finish
        
#         output, _ = awk_process.communicate()
#         return output.decode().splitlines()
#     except subprocess.CalledProcessError as e:
#         print(f"Error: {e}")
#         return []

# def validate_query(query, idx):
#     errors = []

#     # Check if there are equal number of opening and closing brackets
#     if query.count('(') != query.count(')'):
#         errors.append("Unbalanced parentheses")

#     # Check if there are equal number of single quotes
#     if query.count("'") % 2 != 0:
#         errors.append("Unbalanced single quotes")

#     # Check if there are equal number of double quotes
#     if query.count('"') % 2 != 0:
#         errors.append("Unbalanced double quotes")

#     if errors:
#         print(f"Query line {idx} is invalid: {query}")
#         for error in errors:
#             print(f"    - {error}")
#         return False
#     else:
#         print(f"Query line {idx} is valid: {query}")
#         return True
    
# def format_and_validate_query(query, idx):
#     query = query.replace('"', "'")
#     query = f"SELECT {query} FROM table"
#     print(f"Validating query line {idx}: {query}")
#     try:
#         sql_query = sqlvalidator.parse(query)
#         if not sql_query.is_valid():
#             print(sql_query.errors)
#             for error in sql_query.errors:
#                 if "The argument of AND must be type boolean" in str(error):
#                     print("Ignoring validation error:", error)
#                 else:
#                     print(error)
#                     return False
#     except sqlvalidator.ValidationError as e:
#         print("SQL validation error:", e)
#         return False
#     return True

# file_paths = ['../../configmap-vmalertrules.yaml']
# invalid_queries = []

# for file_path in file_paths:
#     query_lines = extract_query_lines(file_path)
#     queryies = extract_query(file_path)
#     for idx, query in enumerate(query_lines, start=1):
#         if not format_and_validate_query(query, idx):
#             sys.exit(1)
#     for idx, line in enumerate(queryies, start=1):
#         if not validate_query(line, idx):
#             invalid_queries.append(line)
#     if invalid_queries:
#         sys.exit(1)
#     else:
#         sys.exit(0)

import sys
import sqlvalidator
import yaml

def extract_queries(file_path):
    queries = []
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            for item in data.get('data', {}).values():
                if item and item.startswith("query:"):
                    query = item.split("query: ")[1]
                    queries.append(query)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return queries

def validate_query(query, idx):
    errors = []
    if query.count('(') != query.count(')'):
        errors.append("Unbalanced parentheses")
    if query.count("'") % 2 != 0:
        errors.append("Unbalanced single quotes")
    if query.count('"') % 2 != 0:
        errors.append("Unbalanced double quotes")
    if errors:
        print(f"Query line {idx} is invalid: {query}")
        for error in errors:
            print(f"    - {error}")
        return False
    else:
        print(f"Query line {idx} is valid: {query}")
        return True

def validate_queries(file_paths):
    for file_path in file_paths:
        queries = extract_queries(file_path)
        if not queries:
            continue
        for idx, query in enumerate(queries, start=1):
            if not validate_query(query, idx):
                return False
    return True

file_paths = ['../../configmap-vmalertrules.yaml']
if not validate_queries(file_paths):
    sys.exit(1)
sys.exit(0)
