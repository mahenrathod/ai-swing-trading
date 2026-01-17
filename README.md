# ai-swing-trading
Step-1: Create an empty github repo and follow:
- Create an empty folder in your macboo called "ai-swing-trading"
- cd ai-swing-trading
- echo "# ai-swing-trading" >> README.md
- git init
- git add README.md
- git commit -m "first commit Mahen"
- git branch -M main
- git remote add origin https://github.com/mahenrathod/ai-swing-trading.git
- git push -u origin main

Step-2: Create project structure
- uv --version
- uv init command will create initial project with pyproject.toml
- add below dependencies in pyproject.toml
    fastapi
    uvicorn
    pandas
    numpy
    yfinance
- uv sync command will install all depenencies provided in pyproject.toml inside .venv folder
- create .env file to store secrets and api keys


# Commands
uv init
uv sync
uv pip list