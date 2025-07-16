from flask import Flask, jsonify, request
from dotenv import load_dotenv
from functools import wraps
from typing import Callable, Dict, Any
from github_api import GitHubAPI
from database import Database
from data_processor import DataProcessor

load_dotenv()
app = Flask(__name__)
github = GitHubAPI()

def handle_errors(f: Callable) -> Callable:
    """Decorator for consistent error handling across routes"""
    @wraps(f)
    def wrapper(*args, **kwargs) -> Dict[str, Any]:
        try:
            return f(*args, **kwargs)
        except Exception as e:
            app.logger.error(f'Error in {f.__name__}: {str(e)}')
            return jsonify({
                'error': str(e),
                'endpoint': request.path,
                'method': request.method
            }), 500
    return wrapper

@app.route('/api/repository/<owner>/<repo>')
@handle_errors
def get_repository(owner: str, repo: str) -> Dict[str, Any]:
    """Get repository information and store in database
    
    Args:
        owner: Repository owner username
        repo: Repository name
    
    Returns:
        Repository data including basic info, stars, and forks
    """
    raw_data = github.get_repository_info(owner, repo)
    processed_data = DataProcessor.process_repository(raw_data)
    
    with Database() as db:
        repo_id = db.store_repository(processed_data)
        processed_data['id'] = repo_id
    
    return jsonify(processed_data)

@app.route('/api/contributors/<owner>/<repo>')
@handle_errors
def get_contributors(owner: str, repo: str) -> Dict[str, Any]:
    """Get repository contributors and their contributions
    
    Args:
        owner: Repository owner username
        repo: Repository name
    
    Returns:
        List of contributors with their contribution counts
    """
    raw_data = github.get_contributors(owner, repo)
    processed_data = DataProcessor.process_contributors(raw_data)
    
    with Database() as db:
        repo_id = db.store_repository(DataProcessor.process_repository(
            github.get_repository_info(owner, repo)
        ))
        db.store_contributors(repo_id, processed_data)
    
    return jsonify(processed_data)

@app.route('/api/commits/<owner>/<repo>')
@handle_errors
def get_commit_activity(owner: str, repo: str) -> Dict[str, Any]:
    """Get weekly commit activity for the last year
    
    Args:
        owner: Repository owner username
        repo: Repository name
    
    Returns:
        Weekly commit counts for the last year
    """
    raw_data = github.get_commit_activity(owner, repo)
    processed_data = DataProcessor.process_commit_activity(raw_data)
    
    with Database() as db:
        repo_id = db.store_repository(DataProcessor.process_repository(
            github.get_repository_info(owner, repo)
        ))
        db.store_commit_activity(repo_id, processed_data)
    
    return jsonify(processed_data)

@app.route('/api/languages/<owner>/<repo>')
@handle_errors
def get_languages(owner: str, repo: str) -> Dict[str, Any]:
    """Get language distribution in the repository
    
    Args:
        owner: Repository owner username
        repo: Repository name
    
    Returns:
        Dictionary of languages and their byte counts
    """
    raw_data = github.get_language_distribution(owner, repo)
    processed_data = DataProcessor.process_languages(raw_data)
    
    with Database() as db:
        repo_id = db.store_repository(DataProcessor.process_repository(
            github.get_repository_info(owner, repo)
        ))
        db.store_languages(repo_id, processed_data)
    
    return jsonify(processed_data)

@app.route('/api/issues/<owner>/<repo>')
@handle_errors
def get_issues(owner: str, repo: str) -> Dict[str, Any]:
    """Get repository issues
    
    Args:
        owner: Repository owner username
        repo: Repository name
        state: (query param) Issue state filter (all/open/closed)
    
    Returns:
        List of issues with their details
    """
    state = request.args.get('state', 'all')
    raw_data = github.get_issues(owner, repo, state)
    processed_data = DataProcessor.process_issues(raw_data)
    
    with Database() as db:
        repo_id = db.store_repository(DataProcessor.process_repository(
            github.get_repository_info(owner, repo)
        ))
        db.store_issues(repo_id, processed_data)
    
    return jsonify(processed_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
