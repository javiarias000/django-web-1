import os # Added manually
import requests
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils import translation
import re # For parsing Link header
from datetime import datetime # Import datetime
import math # Import math module

from .utils import fetch_github_data # Import the utility function

def home(request):
    total_stars = 0
    total_forks = 0
    sga1_total_commits = "N/A" # New variable for SGA1 commits
    language_distribution = {} # Initialize language distribution

    # Fetch stack data
    stack_data = fetch_github_data()

    context = {
        'total_commits': '0', # Will be updated with SGA1 commits
        'oss_contributions': '0', # Will be updated with total_forks
        'years_exp': '10+',
        'system_uptime': '99.9%',
        'projects': [],
        'stack_data': stack_data, # Add this line
    }

    github_username = "javiarias000"
    
    # --- Fetch all repositories and aggregate stars/forks ---
    repos_api_url = f"https://api.github.com/users/{github_username}/repos"
    try:
        repos_response = requests.get(repos_api_url)
        repos_response.raise_for_status()
        repos_data = repos_response.json()

        for repo in repos_data:
            project_data = {
                'name': repo['name'],
                'description': repo['description'],
                'html_url': repo['html_url'],
                'stargazers_count': repo['stargazers_count'],
                'forks_count': repo['forks_count'],
                'updated_at': datetime.fromisoformat(repo['updated_at'].replace('Z', '+00:00')), # Convert to datetime object
                'languages': [repo['language']] if repo['language'] else [], # Ensure it's a list for iteration
                'image_url': f"https://picsum.photos/seed/{repo['name']}/600/338" # Placeholder image URL
            }
            context['projects'].append(project_data)
            total_stars += repo['stargazers_count']
            total_forks += repo['forks_count']
            
            # Aggregate language distribution
            if repo['language']:
                language_distribution[repo['language']] = language_distribution.get(repo['language'], 0) + 1
        
        context['oss_contributions'] = f"{total_forks}+"

        # Calculate percentages for language distribution
        total_projects_with_language = sum(language_distribution.values())
        if total_projects_with_language > 0:
            for lang, count in language_distribution.items():
                language_distribution[lang] = (count / total_projects_with_language) * 100 
        
        # Sort by percentage (descending) and store in context
        sorted_languages = sorted(language_distribution.items(), key=lambda item: item[1], reverse=True)
        
        # Prepare language data for radar chart with calculated positions
        radar_languages = []
        max_languages_on_radar = 5 # Limit to top N languages for visual clarity
        
        # Define the center and max radius of the radar (adjust as needed)
        center_x, center_y = 50, 50 # Percentage relative to parent
        max_radar_radius = 40 # Percentage relative to parent, max distance from center
        
        for i, (lang, percentage) in enumerate(sorted_languages[:max_languages_on_radar]):
            # Calculate angle for even distribution
            angle_degrees = (i / max_languages_on_radar) * 360
            angle_radians = math.radians(angle_degrees)
            
            # Scale radius based on percentage (e.g., 20% to 100% of max_radar_radius)
            # Min percentage on radar should result in a small radius, max in max_radar_radius
            scaled_radius = (percentage / 100) * max_radar_radius
            
            # Calculate top and left positions
            top_pos = center_y + scaled_radius * math.sin(angle_radians)
            left_pos = center_x + scaled_radius * math.cos(angle_radians)
            
            # Determine dot size based on percentage
            dot_size = int(2 + (percentage / 100) * 8) # Example: size from 2 to 10
            
            radar_languages.append({
                'lang': lang,
                'percentage': percentage,
                'top': f"{top_pos:.2f}%",
                'left': f"{left_pos:.2f}%",
                'size': f"size-{dot_size}"
            })
        
        context['radar_languages'] = radar_languages

    except requests.exceptions.RequestException as e:
        print(f"Error fetching GitHub repositories: {e}")
        context['github_error'] = "No se pudieron obtener los proyectos de GitHub."

    # --- Fetch commit count for SGA1 specifically ---
    sga1_commits_api_url = f"https://api.github.com/repos/{github_username}/SGA1/commits?per_page=1"
    try:
        sga1_commits_response = requests.get(sga1_commits_api_url)
        sga1_commits_response.raise_for_status()
        
        if 'Link' in sga1_commits_response.headers:
            link_header = sga1_commits_response.headers['Link']
            # Regex to find the 'last' page link and extract the page number
            match = re.search(r'page=(\d+)>; rel="last"', link_header)
            if match:
                sga1_total_commits = int(match.group(1))
            else:
                # If only one page, count items in current response (max 30)
                sga1_total_commits = len(sga1_commits_response.json())
        else:
            # No Link header, meaning all commits are on the first page (max 30)
            sga1_total_commits = len(sga1_commits_response.json())
        
        context['total_commits'] = f"{sga1_total_commits}+" if sga1_total_commits > 0 else "0" # Format as "X+"

    except requests.exceptions.RequestException as e:
        print(f"Error fetching SGA1 commit count: {e}")
        # context['github_error'] += " (Error fetching SGA1 commits)" # Append error if needed

    return render(request, 'home.html', context)

def education(request):
    """
    Renders the education page.
    """
    stack_data = fetch_github_data() # Fetch stack data for education page
    context = {
        'stack_data': stack_data,
    }
    return render(request, 'education.html', context)
