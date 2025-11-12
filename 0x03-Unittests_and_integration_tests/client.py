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
