# portafolio/utils.py

import requests
import os
from django.core.cache import cache # Import cache

GITHUB_API_BASE_URL = "https://api.github.com"
GITHUB_USERNAME = "javiarias000" # This can be made configurable later
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN") # Recommend using environment variable for token

HEADERS = {}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"

def fetch_github_data():
    """
    Fetches GitHub data (repositories, languages, topics) for a given user
    and processes it for the 'Stack & Tools' section. Caches the result.
    """
    cache_key = f"github_stack_data_{GITHUB_USERNAME}"
    cached_data = cache.get(cache_key)
    if cached_data:
        print("Returning cached GitHub data.")
        return cached_data

    print("Fetching GitHub data from API (not cached).")
    try:
        repositories = _fetch_user_repositories(GITHUB_USERNAME)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user repositories: {e}")
        return {"frontend": [], "backend": [], "infrastructure": []}

    # Initialize aggregated data structures
    aggregated_languages = {}
    aggregated_topics = {}

    for repo in repositories:
        repo_name = repo["name"]
        owner = GITHUB_USERNAME # Assuming current user is the owner

        # Fetch languages
        try:
            languages = _fetch_repository_languages(owner, repo_name)
            for lang, bytes_of_code in languages.items():
                aggregated_languages[lang] = aggregated_languages.get(lang, 0) + bytes_of_code
        except requests.exceptions.RequestException as e:
            print(f"Error fetching languages for {owner}/{repo_name}: {e}")
        
        # Fetch topics
        try:
            topics = _fetch_repository_topics(owner, repo_name)
            for topic in topics:
                aggregated_topics[topic] = aggregated_topics.get(topic, 0) + 1
        except requests.exceptions.RequestException as e:
            print(f"Error fetching topics for {owner}/{repo_name}: {e}")
            
    # Process aggregated data into categories (Frontend, Backend, Infrastructure)
    stack_data = _categorize_stack_data(aggregated_languages, aggregated_topics)
    cache.set(cache_key, stack_data) # Cache the result
    
    return stack_data

def _fetch_user_repositories(username):
    """Fetches public repositories for a given GitHub user."""
    url = f"{GITHUB_API_BASE_URL}/users/{username}/repos"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status() # Raise an exception for HTTP errors
    return response.json()

def _fetch_repository_languages(owner, repo):
    """Fetches languages for a specific GitHub repository."""
    url = f"{GITHUB_API_BASE_URL}/repos/{owner}/{repo}/languages"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def _fetch_repository_topics(owner, repo):
    """Fetches topics for a specific GitHub repository."""
    url = f"{GITHUB_API_BASE_URL}/repos/{owner}/{repo}/topics"
    # Note: topics API might require 'Accept: application/vnd.github.mercy-preview+json' header
    # Adding it for robustness
    topic_headers = HEADERS.copy()
    topic_headers["Accept"] = "application/vnd.github.mercy-preview+json"
    response = requests.get(url, headers=topic_headers)
    response.raise_for_status()
    return response.json()["names"] # topics API returns {"names": ["topic1", "topic2"]}

def _categorize_stack_data(languages, topics):
    """
    Categorizes languages and topics into Frontend, Backend, Infrastructure
    based on a hardcoded list provided by the user.
    """
    frontend_skills = {"HTML", "CSS", "JavaScript"}
    backend_skills = {"Python", "Django", "PHP", "Databases", "GraphQL"} # Adding GraphQL to Backend as it's often API-related
    infra_skills = {"Bash", "Cyber Security", "Docker"} # Bash for scripting and infrastructure tasks
    
    return {
        "frontend": sorted(list(frontend_skills)),
        "backend": sorted(list(backend_skills)),
        "infrastructure": sorted(list(infra_skills)),
    }
