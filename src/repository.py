from datetime import datetime, timedelta
import requests

class GitHubRepository:
    def __init__(self, username, repo_name):
        """
        Initialize a new GitHubRepository object.

        Parameters:
        - username (str): The GitHub username of the repository owner.
        - repo_name (str): The name of the GitHub repository.
        """
        self.username = username
        self.repo_name = repo_name
        self.events = None 

    def fetch_github_events(self):
        """
        Fetch events from GitHub using the GitHub Events API.

        This method retrieves events associated with the repository
        specified by the username and repository name attributes.
        """
        url = f"https://api.github.com/repos/{self.username}/{self.repo_name}/events"
        headers = {"Accept": "application/vnd.github.v3+json"}  # Specify API version

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            self.events = response.json()
        else:
            print(f"Failed to fetch events: {response.status_code} - {response.reason}")
    
    