from datetime import datetime
from typing import Dict, List, Any

class DataProcessor:
    @staticmethod
    def process_repository(repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and transform repository data"""
        return {
            'github_id': repo_data.get('id'),
            'name': repo_data.get('name'),
            'owner': repo_data.get('owner', {}).get('login'),
            'stars': repo_data.get('stargazers_count', 0),
            'forks': repo_data.get('forks_count', 0),
            'created_at': repo_data.get('created_at'),
            'updated_at': repo_data.get('updated_at')
        }

    @staticmethod
    def process_contributors(contributors_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Clean and transform contributor data"""
        return [{
            'github_username': contributor.get('login'),
            'contributions': contributor.get('contributions', 0)
        } for contributor in contributors_data]

    @staticmethod
    def process_commit_activity(activity_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Clean and transform commit activity data"""
        return [{
            'week': datetime.fromtimestamp(week.get('week', 0)),
            'total_commits': week.get('total', 0)
        } for week in activity_data]

    @staticmethod
    def process_languages(languages_data: Dict[str, int]) -> List[Dict[str, Any]]:
        """Clean and transform language distribution data"""
        return [{
            'language': lang,
            'bytes': bytes_count
        } for lang, bytes_count in languages_data.items()]

    @staticmethod
    def process_issues(issues_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Clean and transform issues data"""
        return [{
            'github_issue_id': issue.get('id'),
            'title': issue.get('title'),
            'state': issue.get('state'),
            'created_at': issue.get('created_at'),
            'closed_at': issue.get('closed_at')
        } for issue in issues_data]
