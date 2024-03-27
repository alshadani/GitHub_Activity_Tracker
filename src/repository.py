from datetime import datetime, timedelta
import requests

'''Repository class for fetching and pre 
   preprocessing events, may be extended in the 
   in the future by possibly adding new 
   data from the events.'''

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
            self.events = []


    def get_weekly_events(self):
        """
        Retrieve events from the past week.

        This method filters the events stored in the GitHubRepository object
        to retain only those events that occurred within the last week.
        """
        current_time = datetime.now()
        one_week_ago = current_time - timedelta(weeks=1)

        events_within_last_week = [event for event in self.events if datetime.fromisoformat(event['created_at'][:-1]) >= one_week_ago]

        return events_within_last_week

    def get_data(self):
        """
        Retrieve data for statistics.

        This method retrieves data necessary for generating statistics,
        either 500 events or events from the past 7 days, whichever is less.
        """
        if (len(self.events) > 500):
            return self.get_weekly_events()
        
        return self.events
    
    def __repr__(self):
        """
        Return a string representation of the GitHubRepository object.

        This method returns a string containing the GitHub username and repository name.
        """
        return f"GitHubRepository(username='{self.username}', repo_name='{self.repo_name}')"
