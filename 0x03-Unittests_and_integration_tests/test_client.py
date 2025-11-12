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
    @patch("client.utils.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test org property returns expected value"""
        mock_get_json.return_value = {"login": org_name}
        client = GithubOrgClient(org_name)
        result = client.org
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, {"login": org_name})

    def test_public_repos_url(self):
        """Test _public_repos_url property"""
        client = GithubOrgClient("test_org")
        payload = {"repos_url": "https://api.github.com/orgs/test_org/repos"}
        with patch.object(GithubOrgClient, "org", new_callable=property) as mock_org:
            mock_org.return_value = payload
            result = client._public_repos_url
            self.assertEqual(result, payload["repos_url"])

    @patch("client.utils.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns the correct repo list"""
        client = GithubOrgClient("test_org")
        payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = payload

        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=property
        ) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/test_org/repos"
            result = client.public_repos()
            self.assertEqual(result, ["repo1", "repo2"])
            self.assertTrue(mock_url.called)
            mock_get_json.assert_called_once_with(mock_url.return_value)

    def test_has_license(self):
        """Test has_license method"""
        client = GithubOrgClient("test_org")
        repo = {"license": {"key": "mit"}}
        self.assertTrue(client.has_license(repo, "mit"))
        self.assertFalse(client.has_license(repo, "apache"))
        self.assertFalse(client.has_license({}, "mit"))


if __name__ == "__main__":
    unittest.main()
