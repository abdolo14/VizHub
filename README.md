# VizHub

Full-stack application to extract and visualize insights from public GitHub repositories.

## Project Structure

- `/backend`: Python (Flask) backend for API and GitHub integration.
- `/frontend`: React frontend for user interface and visualizations.

## Setup

### Backend

1.  Navigate to the `backend` directory: `cd backend`
2.  Create a virtual environment: `python3 -m venv venv` (or `python -m venv venv`)
3.  Activate the virtual environment:
    *   macOS/Linux: `source venv/bin/activate`
    *   Windows: `venv\Scripts\activate`
4.  Install dependencies: `pip install -r requirements.txt`
5.  Create a `.env` file from `.env.example` and add your GitHub Personal Access Token:
    `cp .env.example .env`
    Then edit `.env` to include `GITHUB_TOKEN=your_actual_token_here`
    **Important**: Add `.env` to your `.gitignore` file if it's not already covered by a general pattern like `*.env` or `!.env.example`. The provided `.gitignore` includes `.env`.
6.  Run the application: `python app.py`

(Frontend setup instructions will be added later)
