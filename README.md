# VizHub
GitHub Repository Insights & Visualizations

VizHub is a full-stack web application designed to extract key insights from public GitHub repositories and transform them into meaningful visualizations. Users can simply enter a GitHub repository name (e.g., `owner/repository`) to receive helpful analytics, including commit activity, top contributors, issue trends, and language usage.

## Features (Planned)

*   **Web-Based Interface:** Accessible from any modern web browser.
*   **GitHub Repository Input:** Easy input for specifying target repositories.
*   **Commit Activity Analysis:** Visualize commit frequency and patterns over time.
*   **Top Contributor Identification:** Display key contributors based on commit activity.
*   **Issue Trend Tracking:** Analyze open vs. closed issues, creation, and resolution rates.
*   **Language Usage Breakdown:** Show the distribution of programming languages used in the repository.
*   **Interactive Visualizations:** Present data through engaging charts and graphs.

## Tech Stack

### Frontend
*   **React.js:** A JavaScript library for building the user interface.
*   **Tailwind CSS:** A utility-first CSS framework for styling.

### Backend
*   **Python (Flask):** A lightweight WSGI web application framework for the REST API.
*   **GitHub REST API:** Used to fetch data directly from GitHub.

### Database
*   **PostgreSQL:** A powerful, open-source object-relational database system to store and cache repository data (planned for future enhancement to manage API rate limits and improve performance).

## Project Structure

This project follows a standard structure for separating frontend and backend concerns:

### Root Directory (`/Users/abda/CascadeProjects/VizHub/`)
*   **`backend/`**: Contains the Python Flask application.
    *   `app.py`: The main entry point for the Flask backend.
    *   `requirements.txt`: Lists Python dependencies for the backend.
    *   `.env.example`: Template for environment variables (e.g., `GITHUB_TOKEN`, `DATABASE_URL`).
    *   `(Other directories like 'routes/', 'services/', 'models/' will be added as the backend develops)`
*   **`frontend/`**: Will contain the React.js application.
    *   `.gitkeep`: Placeholder file.
    *   `(Standard React structure like 'public/', 'src/', 'package.json' will be added when the frontend is initialized)`
*   **`.gitignore`**: Specifies intentionally untracked files that Git should ignore.
*   **`README.md`**: This project documentation file.

*(Note: A `.env` file, based on `.env.example`, should be present in the `backend/` directory for local development to store sensitive credentials. This file is included in `.gitignore` and should not be committed to the repository.)*

## Why This Structure?

*   **Separation of Concerns:** The frontend (client-side) and backend (server-side) code are distinctly organized into `frontend/` and `backend/` directories, promoting modularity.
*   **Scalability & Maintainability:** This separation makes it easier to develop, test, and maintain each part of the application independently.
*   **Standard Practices:** Adheres to common conventions for full-stack web application development.
