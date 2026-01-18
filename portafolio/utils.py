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
    Categorizes languages and topics into Frontend, Backend, Infrastructure.
    This is a preliminary categorization and can be refined.
    """
    frontend_skills = set()
    backend_skills = set()
    infra_skills = set()
    
    # User-provided specific technologies to look for (from previous turn)
    user_technologies_map = {
        "django": "backend",
        "html": "frontend",
        "php": "backend",
        "css": "frontend",
        "bash": "infra",
        "python": "backend",
        "data science": "backend" # Categorizing data science as backend as it's typically server-side
    }

    # Process languages
    for lang, bytes_of_code in languages.items():
        lower_lang = lang.lower()
        if lower_lang == "html" or lower_lang == "css" or lower_lang == "javascript" or lower_lang == "typescript":
            frontend_skills.add(lang)
        elif lower_lang == "python" and bytes_of_code > 0: # Consider Python for backend if it's actually used
            backend_skills.add(lang)
        elif lower_lang == "php" and bytes_of_code > 0:
            backend_skills.add(lang)
        elif lower_lang in ["shell", "bash"] and bytes_of_code > 0:
            infra_skills.add(lang)
        
    # Process topics
    for topic in topics:
        lower_topic = topic.lower()
        if lower_topic in ["react", "nextjs", "tailwind", "framer-motion", "redux"]:
            frontend_skills.add(topic)
        elif lower_topic in ["graphql", "postgresql", "prisma", "redis", "fastify", "django", "python"]:
            backend_skills.add(topic)
        elif lower_topic in ["aws", "vercel", "docker", "kubernetes", "ci-cd", "terraform"]:
            infra_skills.add(topic)
        # Handle "data science" related topics
        if lower_topic in ["data-science", "machine-learning"]:
            backend_skills.add("Data Science") # Add "Data Science" directly
    
    # Add user-specified technologies explicitly if not already added by languages/topics
    for tech, category in user_technologies_map.items():
        tech_found = False
        if category == "frontend":
            if tech.lower() in [s.lower() for s in frontend_skills]:
                tech_found = True
            else:
                frontend_skills.add(tech.replace("_", " ").title()) # Add it if not already present
        elif category == "backend":
            if tech.lower() in [s.lower() for s in backend_skills]:
                tech_found = True
            else:
                backend_skills.add(tech.replace("_", " ").title())
        elif category == "infra":
            if tech.lower() in [s.lower() for s in infra_skills]:
                tech_found = True
            else:
                infra_skills.add(tech.replace("_", " ").title())

    # Filter out empty strings that might have been added
    frontend_skills = {s for s in frontend_skills if s}
    backend_skills = {s for s in backend_skills if s}
    infra_skills = {s for s in infra_skills if s}

    return {
        "frontend": sorted(list(frontend_skills)),
        "backend": sorted(list(backend_skills)),
        "infrastructure": sorted(list(infra_skills)),
    }
