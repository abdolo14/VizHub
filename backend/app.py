from flask import Flask, jsonify, request
from dotenv import load_dotenv
from github_api import GitHubAPI
from database import Database

load_dotenv()
app = Flask(__name__)
github = GitHubAPI()

@app.route('/api/repository/<owner>/<repo>')
def get_repository(owner, repo):
    try:
        data = github.get_repository_info(owner, repo)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contributors/<owner>/<repo>')
def get_contributors(owner, repo):
    try:
        data = github.get_contributors(owner, repo)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/commits/<owner>/<repo>')
def get_commit_activity(owner, repo):
    try:
        data = github.get_commit_activity(owner, repo)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/languages/<owner>/<repo>')
def get_languages(owner, repo):
    try:
        data = github.get_language_distribution(owner, repo)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/issues/<owner>/<repo>')
def get_issues(owner, repo):
    state = request.args.get('state', 'all')
    try:
        data = github.get_issues(owner, repo, state)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
