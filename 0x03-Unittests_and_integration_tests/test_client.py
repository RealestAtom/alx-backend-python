#!/usr/bin/env python3
"""
Unittests for client.GithubOrgClient
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.utils.get_json")  # patch where it's imported in client.py
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns expected value"""
        mock_get_json.return_value = {"login": org_name}
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert get_json called exactly once with the correct URL
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, {"login": org_name})

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct URL"""
        client = GithubOrgClient("test_org")
        payload = {"repos_url": "https://api.github.com/orgs/test_org/repos"}

        # Patch the org property
        with patch.object(
            GithubOrgClient, "org", new_callable=property
        ) as mock_org:
            mock_org.return_value = payload
            result = client._public_repos_url
            self.assertEqual(result, payload["repos_url"])

    @patch("client.utils.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the correct list of repos"""
        client = GithubOrgClient("test_org")
        payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = payload

        # Patch the _public_repos_url property
        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=property
        ) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/test_org/repos"

            result = client.public_repos()
            self.assertEqual(result, ["repo1", "repo2"])

            # Ensure the mocked property and get_json were called once
            self.assertTrue(mock_url.called)
            mock_get_json.assert_called_once_with(mock_url.return_value)


if __name__ == "__main__":
    unittest.main()
