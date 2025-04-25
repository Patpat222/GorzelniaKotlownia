import os
import subprocess

def push_to_github(commit_message: str):
    github_token = os.environ.get("github_token")
    if not github_token:
        return "❌ Brak tokena"

    repo_url = f"https://{github_token}@github.com/Patpat222/GorzelniaKotlownia.git"

    try:
        subprocess.run(["git", "config", "user.name", "kotlownia-bot"], check=True)
        subprocess.run(["git", "config", "user.email", "kotlownia@app.local"], check=True)
        subprocess.run(["git", "add", "data/*.json"], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push", repo_url], check=True)
        return "✅ Dane zostały wysłane do GitHuba"
    except subprocess.CalledProcessError as e:
        return f"⚠️ Błąd przy pushu: {e}"
