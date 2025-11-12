#!/usr/bin/env python3
"""
GithubOrgClient module
"""

import utils


class GithubOrgClient:
    """Github organization client"""

    def __init__(self, org_name):
        self.org_name = org_name

    @property
    def org(self):
        """Return JSON payload of organization from GitHub API"""
        return utils.get_json(f"https://api.github.com/orgs/{self.org_name}")

    @property
    def _public_repos_url(self):
        """Return the repos_url from org payload"""
        return self.org.get("repos_url")

    def public_repos(self):
        """Return list of repo names for the organization"""
        url = self._public_repos_url
        repos = utils.get_json(url)
        return [repo["name"] for repo in repos]

    def has_license(self, repo, license_key):
        """Return True if repo has the given license"""
        license_info = repo.get("license")
        return license_info and license_info.get("key") == license_key
