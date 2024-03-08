import json

def recursive_search(data, results):
    if isinstance(data, dict):
        # Check if this dictionary represents a user's message
        if "author" in data and data.get("author", {}).get("role") == "user" and "content" in data:
            # Ensure we're dealing with text content
            parts = data.get("content", {}).get("parts", [])
            if parts and isinstance(parts[0], str):  # Check if the first part is a string
                content = parts[0]
                results["prompts"].add(content)
                results["total_words"] += len(content.split())
                results["total_characters"] += len(content)
        # Recursively search through all dictionary values
        for value in data.values():
            recursive_search(value, results)
    elif isinstance(data, list):
        # Recursively search through all items in the list
        for item in data:
            recursive_search(item, results)

def calculate_stats(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    results = {"prompts": set(), "total_words": 0, "total_characters": 0}
    recursive_search(data, results)

    return len(results["prompts"]), results["total_words"], results["total_characters"]

file_path = 'conversations.json'
try:
    num_prompts, num_words, num_characters = calculate_stats(file_path)
    print(f"Number of different prompts: {num_prompts}")
    print(f"Total number of words sent: {num_words}")
    print(f"Total number of characters sent: {num_characters}")
except Exception as e:
    print(f"An error occurred: {e}")
