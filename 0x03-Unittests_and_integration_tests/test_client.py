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
    @patch("client.utils.get_json")  # patch where get_json is looked up in client.py
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns expected value"""
        # Setup mock return value
        mock_get_json.return_value = {"login": org_name}

        # Instantiate client and access org property
        client = GithubOrgClient(org_name)
        result = client.org  # property, not a method

        # Assert get_json called once with correct URL
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

        # Assert org property returns expected value
        self.assertEqual(result, {"login": org_name})


if __name__ == "__main__":
    unittest.main()
