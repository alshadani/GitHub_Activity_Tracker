from datetime import datetime
from repository import GitHubRepository
from itertools import groupby
import os 
import csv 

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
        return 0  # If only one event, average time is 0

