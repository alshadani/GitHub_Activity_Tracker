import unittest
from unittest.mock import patch
from repository import GitHubRepository

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
            self.assertIsNone(repo.events)

if __name__ == '__main__':
    unittest.main()
