import os
import psycopg2
from psycopg2.extras import DictCursor
from typing import Dict, List, Any

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT', '5432')
        )
        self.cur = self.conn.cursor(cursor_factory=DictCursor)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.close()
        self.conn.close()

    def execute(self, query: str, params=None) -> None:
        self.cur.execute(query, params)
        self.conn.commit()

    def fetchall(self) -> List[Dict]:
        return [dict(row) for row in self.cur.fetchall()]

    def fetchone(self) -> Dict:
        row = self.cur.fetchone()
        return dict(row) if row else None

    def store_repository(self, data: Dict[str, Any]) -> int:
        query = """
        INSERT INTO repositories (github_id, name, owner, stars, forks, created_at, updated_at)
        VALUES (%(github_id)s, %(name)s, %(owner)s, %(stars)s, %(forks)s, %(created_at)s, %(updated_at)s)
        ON CONFLICT (github_id) DO UPDATE SET
            stars = EXCLUDED.stars,
            forks = EXCLUDED.forks,
            updated_at = EXCLUDED.updated_at
        RETURNING id;
        """
        self.execute(query, data)
        return self.fetchone()['id']

    def store_contributors(self, repo_id: int, contributors: List[Dict[str, Any]]) -> None:
        for contributor in contributors:
            query = """
            INSERT INTO contributors (repository_id, github_username, contributions)
            VALUES (%(repo_id)s, %(github_username)s, %(contributions)s)
            ON CONFLICT (repository_id, github_username) DO UPDATE SET
                contributions = EXCLUDED.contributions;
            """
            self.execute(query, {**contributor, 'repo_id': repo_id})

    def store_commit_activity(self, repo_id: int, activities: List[Dict[str, Any]]) -> None:
        for activity in activities:
            query = """
            INSERT INTO commit_activity (repository_id, week, total_commits)
            VALUES (%(repo_id)s, %(week)s, %(total_commits)s)
            ON CONFLICT (repository_id, week) DO UPDATE SET
                total_commits = EXCLUDED.total_commits;
            """
            self.execute(query, {**activity, 'repo_id': repo_id})

    def store_languages(self, repo_id: int, languages: List[Dict[str, Any]]) -> None:
        for lang_data in languages:
            query = """
            INSERT INTO language_distribution (repository_id, language, bytes)
            VALUES (%(repo_id)s, %(language)s, %(bytes)s)
            ON CONFLICT (repository_id, language) DO UPDATE SET
                bytes = EXCLUDED.bytes;
            """
            self.execute(query, {**lang_data, 'repo_id': repo_id})

    def store_issues(self, repo_id: int, issues: List[Dict[str, Any]]) -> None:
        for issue in issues:
            query = """
            INSERT INTO issues (repository_id, github_issue_id, title, state, created_at, closed_at)
            VALUES (%(repo_id)s, %(github_issue_id)s, %(title)s, %(state)s, %(created_at)s, %(closed_at)s)
            ON CONFLICT (repository_id, github_issue_id) DO UPDATE SET
                state = EXCLUDED.state,
                closed_at = EXCLUDED.closed_at;
            """
            self.execute(query, {**issue, 'repo_id': repo_id})
