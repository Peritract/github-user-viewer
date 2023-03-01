"""Contains the GitHub user viewer application."""

import requests as req


class APIError(Exception):
    """Class for errors caused by an API."""

    def __init__(self, message: str, code: int):
        self.message = message
        self.code = code


def prompt_user_for_github_username() -> str:
    """Repeatedly prompts the user for a valid username."""
    username = ""
    while len(username) < 1:
        username = input("Enter a GitHub username: ")
    return username


def get_github_user_details(username: str) -> dict:
    """Returns a dict containing user details."""
    res = req.get(f"https://api.github.com/users/{username}", timeout=5)

    if res.status_code == 400:
        raise APIError("Invalid username.", 400)
    if res.status_code == 500:
        raise APIError("Server error.", 500)

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
    res = req.get(f"https://api.github.com/users/{username}/repos?per_page={per_page}", timeout=5)
    data = res.json()
    return data


def display_repository_information(repositories: list):
    """Prints key information about each repository."""
    for repo in repositories:
        print(f"  - {repo['name']} ({repo['stargazers_count']})")


if __name__ == "__main__":
    try:
        username_to_search = prompt_user_for_github_username()
        user_details = get_github_user_details(username_to_search)
        display_github_user_details(user_details)
        repos = get_user_repository_information(username_to_search, 5)
        display_repository_information(repos)
    except APIError as err:
        print(err.message)
