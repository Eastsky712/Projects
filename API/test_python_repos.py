import unittest
import python_repos   # this runs the API request when imported

class TestPythonRepos(unittest.TestCase):

    def test_status_code(self):
        """Test that the API request succeeded."""
        self.assertEqual(python_repos.r.status_code, 200)

    def test_items_returned(self):
        """Test that some repositories were returned."""
        repo_dicts = python_repos.response_dict['items']
        self.assertTrue(len(repo_dicts) > 0)

    def test_total_repositories(self):
        """Test that total_count is reasonably large."""
        total_repos = python_repos.response_dict['total_count']
        
        # Because the query is for stars > 10000, expect more than ~50.
        self.assertGreater(total_repos, 50)

    def test_incomplete_results(self):
        """GitHub should return complete results for this call."""
        self.assertFalse(python_repos.response_dict['incomplete_results'])

if __name__ == '__main__':
    unittest.main()
