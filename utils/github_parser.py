import requests

def get_repo_info(github_url):
    try:
        owner_repo = github_url.split("github.com/")[1]
        api_url = f"https://api.github.com/repos/{owner_repo}"
        response = requests.get(api_url)
        data = response.json()
        return data.get("name", "Unknown Project"), data.get("description", "")
    except Exception as e:
        return "Unknown", ""
