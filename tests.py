import unittest
from unittest.mock import patch
from repository import GitHubRepository
from helper import group_event_by_type, calculate_average_time, fetch_and_calculate_statistics

class TestGitHubRepository(unittest.TestCase):
    def test_fetch_github_events_success(self):
        # Mock response data
        response_data = [{'id': 1, 'type': 'PushEvent', 'created_at': '2024-03-20T12:00:00Z'},
                         {'id': 2, 'type': 'PullRequestEvent', 'created_at': '2024-03-21T12:00:00Z'}]

        # Mock requests.get to return expected response
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = response_data

            # Create a GitHubRepository object
            repo = GitHubRepository(username='testuser', repo_name='testrepo')
            
            # Call the fetch_github_events method
            repo.fetch_github_events()

            # Assert that events attribute is populated with expected data
            self.assertEqual(repo.events, response_data)

    def test_fetch_github_events_failure(self):
        # Mock requests.get to simulate failed response
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 404
            mock_get.return_value.reason = 'Not Found'

            # Create a GitHubRepository object
            repo = GitHubRepository(username='testuser', repo_name='testrepo')
            
            # Call the fetch_github_events method
            repo.fetch_github_events()

            # Assert that events attribute is None due to failed response
            self.assertEqual(repo.events, [])

    class TestGitHubActivityTracker(unittest.TestCase):
        def test_group_event_by_type(self):
            events = [
                {'type': 'push', 'created_at': '2022-03-30T12:00:00Z'},
                {'type': 'pull_request', 'created_at': '2022-03-31T12:00:00Z'},
                {'type': 'push', 'created_at': '2022-03-31T13:00:00Z'}
            ]
            expected_result = {'push': ['2022-03-30T12:00:00Z', '2022-03-31T13:00:00Z'],
                            'pull_request': ['2022-03-31T12:00:00Z']}
            self.assertEqual(group_event_by_type(events), expected_result)

        def test_calculate_average_time(self):
            timestamps = ['2022-03-30T12:00:00Z', '2022-03-31T12:00:00Z', '2022-03-31T13:00:00Z']
            expected_result = 1800.0  # 30 minutes
            self.assertEqual(calculate_average_time(timestamps), expected_result)

        @patch('your_module.repo.fetch_github_events')
        @patch('your_module.repo.get_data')
        def test_fetch_and_calculate_statistics(self, mock_get_data, mock_fetch_events):
            repo = GitHubRepository('username', 'repository')
            mock_get_data.return_value = [
                {'type': 'push', 'created_at': '2022-03-30T12:00:00Z'},
                {'type': 'push', 'created_at': '2022-03-31T13:00:00Z'}
            ]
            expected_result = {'push': 86400.0}  # 1 day
            self.assertEqual(fetch_and_calculate_statistics(repo), expected_result)

if __name__ == '__main__':
    unittest.main()
