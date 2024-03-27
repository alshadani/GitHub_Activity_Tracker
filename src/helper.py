from datetime import datetime
from repository import GitHubRepository
from itertools import groupby
import os 
import csv 

'''Utilities for processing .csv files
   A .csv file is created for each repository. 
   file in the statistics folder, which can then be 
   can be read. 
   
   Another good solution would be to create only one 
   .csv file, but I decided to make it separate, because
    in some cases it can be more convinient to work with data
    as the app tracks only up to 5 repositories
    
    To fetch data from the repositories again just delete
    folder statistics.'''

def group_event_by_type(events):
    """
    Group events by their type.

    Parameters:
    - events (list): A list of event dictionaries.

    Returns:
    - dict: A dictionary where keys are event types and values are lists of corresponding timestamps.
    """
    if events is None:
        print("Error: No events were read")
        return None
    
    # Sort events by type
    sorted_events = sorted(events, key=lambda x: x['type'])
    
    # Group events by type
    grouped_events = {}
    for key, group in groupby(sorted_events, key=lambda x: x['type']):
        grouped_events[key] = [event['created_at'] for event in group]

    return grouped_events

def calculate_average_time(timestamps):
    """
    Calculate the average time between consecutive timestamps.

    Parameters:
    - timestamps (list): A list of ISO-formatted timestamps.

    Returns:
    - float: The average time between consecutive timestamps, in seconds.
    """
    if len(timestamps) > 1:
        time_diffs = []
        # Calculate time differences 
        for i in range(1, len(timestamps)):
            time_diff = -(datetime.fromisoformat(timestamps[i]) - datetime.fromisoformat(timestamps[i-1]))
            time_diffs.append(time_diff.total_seconds())  # Convert timedelta to seconds

        average_time = sum(time_diffs) / len(time_diffs)
        return average_time
    else:
        # If only one event, average time is 0
        return 0 

def load_statistics_from_csv(csv_filename):
    """
    Load statistics from a CSV file.

    Parameters:
    - csv_filename (str): The filename of the CSV file containing statistics.

    Returns:
    - dict: A dictionary containing event types as keys and average times as values.
    """
    with open(csv_filename, 'r') as file:
        reader = csv.DictReader(file)
        return {row['event_type']: float(row['average_time']) for row in reader}

def save_statistics_to_csv(csv_filename, average_times):
    """
    Save statistics to a CSV file.

    Parameters:
    - csv_filename (str): The filename of the CSV file to save statistics to.
    - username (str): The GitHub username of the repository owner.
    - repo_name (str): The name of the GitHub repository.
    - average_times (dict): A dictionary containing event types as keys and average times as values.
    """

    if average_times == []:
        return 
    
    os.makedirs('statistics', exist_ok=True)
    # Check if CSV file already exists
    if os.path.exists(csv_filename):
        # Load existing statistics
        existing_stats = load_statistics_from_csv(csv_filename)
        # Update existing statistics with new data
        existing_stats.update(average_times)
        # Write updated statistics to the CSV file
        with open(csv_filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['event_type', 'average_time'])
            writer.writeheader()
            for event_type, avg_time in existing_stats.items():
                writer.writerow({'event_type': event_type, 'average_time': avg_time})
    else:
        # Create new CSV file and save statistics
        with open(csv_filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['event_type', 'average_time'])
            writer.writeheader()
            for event_type, avg_time in average_times.items():
                writer.writerow({'event_type': event_type, 'average_time': avg_time})

def fetch_and_calculate_statistics(repo):
    """
    Fetch events from GitHub and calculate statistics.

    Parameters:
    - repo (GitHubRepository): The GitHub repository object.

    Returns:
    - dict: A dictionary containing event types as keys and average times as values.
    """
    repo.fetch_github_events()
    data = repo.get_data()
    grouped_events = group_event_by_type(data)
    
    # Calculate average times for each event type
    average_times = {}
    for event_type, timestamps in grouped_events.items():
        average_time = calculate_average_time(timestamps)
        if average_time != 0:  # Exclude event types with an average time of 0
            average_times[event_type] = average_time
    
    return average_times

def get_statistics(repositories):
    """
    Get statistics for a list of GitHub repositories.

    Parameters:
    - repositories (list): A list of GitHubRepository objects.

    Returns:
    - list: A list of dictionaries, each containing repository information and its associated statistics.
    """
    statistics = []
    # check if data has been added before 
    for repo in repositories:
        csv_filename = f"statistics/{repo.username}_{repo.repo_name}_statistics.csv"
        if os.path.exists(csv_filename):
            average_times = load_statistics_from_csv(csv_filename)
        else:
            average_times = fetch_and_calculate_statistics(repo)
            save_statistics_to_csv(csv_filename, average_times)

        statistics.append({'repository': repo, 'average_times': average_times})
    return statistics
