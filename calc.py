import json

def recursive_search(data, results):
    if isinstance(data, dict):        
        role = data.get("author", {}).get("role")
        if role in ["user", "assistant"]:            
            content_parts = data.get("content", {}).get("parts", [])
            for part in content_parts:
                if isinstance(part, str):  # Ensure part is a string
                    if role == "user":
                        results["user_total_prompts"] += 1  # Increment prompt count
                        results["user_total_words"] += len(part.split())
                        results["user_total_characters"] += len(part)
                    elif role == "assistant":
                        results["assistant_total_prompts"] += 1  # Increment prompt count
                        results["assistant_total_words"] += len(part.split())
                        results["assistant_total_characters"] += len(part)
        for value in data.values():
            recursive_search(value, results)
    elif isinstance(data, list):
        for item in data:
            recursive_search(item, results)

def calculate_stats(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    results = {
        "user_total_prompts": 0, "user_total_words": 0, "user_total_characters": 0,
        "assistant_total_prompts": 0, "assistant_total_words": 0, "assistant_total_characters": 0
    }
    recursive_search(data, results)

    return results

file_path = 'conversations.json'
try:
    stats = calculate_stats(file_path)
    print(f"User - Total prompts: {stats['user_total_prompts']}, Total words: {stats['user_total_words']}, Total characters: {stats['user_total_characters']}")
    print(f"Assistant - Total prompts: {stats['assistant_total_prompts']}, Total words: {stats['assistant_total_words']}, Total characters: {stats['assistant_total_characters']}")
except Exception as e:
    print(f"An error occurred: {e}")
