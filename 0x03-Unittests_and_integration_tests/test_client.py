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
    @patch(
        "client.utils.get_json"
    )  # patch where client.py actually calls get_json
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns expected value"""
        # Mock the return value
        mock_get_json.return_value = {"login": org_name}

        # Instantiate client
        client = GithubOrgClient(org_name)

        # Access org property (do not call as method)
        result = client.org

        # Assert get_json called exactly once with correct URL
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

        # Assert the property returns the mocked value
        self.assertEqual(result, {"login": org_name})


if __name__ == "__main__":
    unittest.main()
