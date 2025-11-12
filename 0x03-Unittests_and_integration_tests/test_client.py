#!/usr/bin/env python3
"""
Unittests for client.GithubOrgClient
"""

import unittest
from unittest.mock import patch, Mock
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

        # Mock the org property
        payload = {"repos_url": "https://api.github.com/orgs/test_org/repos"}
        with patch.object(
            GithubOrgClient, "org", new_callable=property
        ) as mock_org:
            mock_org.return_value = payload

            result = client._public_repos_url
            self.assertEqual(result, payload["repos_url"])


if __name__ == "__main__":
    unittest.main()
