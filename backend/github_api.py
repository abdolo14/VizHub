import os
import requests
from datetime import datetime

class GitHubAPI:
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
            "Accept": "application/vnd.github.v3+json"
        }

    def get_repository_info(self, owner, repo):
        """Get basic repository information"""
        url = f"{self.base_url}/repos/{owner}/{repo}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_contributors(self, owner, repo):
        """Get repository contributors and their stats"""
        url = f"{self.base_url}/repos/{owner}/{repo}/contributors"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_commit_activity(self, owner, repo):
        """Get commit activity for the last year"""
        url = f"{self.base_url}/repos/{owner}/{repo}/stats/commit_activity"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_language_distribution(self, owner, repo):
        """Get language distribution in the repository"""
        url = f"{self.base_url}/repos/{owner}/{repo}/languages"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_issues(self, owner, repo, state="all"):
        """Get repository issues"""
        url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        params = {"state": state}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()
