import requests as req


def prompt_user_for_github_username() -> str:
    """Repeatedly prompts the user for a valid username."""
    username = ""
    while len(username) < 1:
        username = input("Enter a GitHub username: ")
    return username


def get_github_user_details(username: str) -> dict:
    """Returns a dict containing user details."""
    res = req.get(f"https://api.github.com/users/{username}")
    if res.status_code >= 400:
        raise Exception("Invalid username.")
    data = res.json()
    return data


def display_github_user_details(details: dict):
    """Prints key information about the user to the console."""
    if details["name"]:
        print(f"User: {details['name']} ({details['login']})")
    else: print(f"User: {details['login']}")
    print(f"Followers: {details['followers']}")


def get_user_repository_information(username: str, per_page: int=5) -> list:
    """Returns a list of repositories for a given user."""
    res = req.get(f"https://api.github.com/users/{username}/repos?per_page={per_page}")
    data = res.json()
    return data


def display_repository_information(repositories: list):
    """Prints key information about each repository."""
    for repo in repositories:
        print(f"  - {repo['name']} ({repo['stargazers_count']})")


if __name__ == "__main__":
    try:
        username = prompt_user_for_github_username()
        details = get_github_user_details(username)
        display_github_user_details(details)
        repos = get_user_repository_information(username, 5)
        display_repository_information(repos)
    except Exception as err:
        print(err.args[0])