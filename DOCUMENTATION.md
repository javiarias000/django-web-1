# Comprehensive Project Documentation: Dynamic Django Portfolio

## Table of Contents
1.  [Introduction](#1-introduction)
2.  [Features](#2-features)
3.  [Project Structure](#3-project-structure)
4.  [Setup and Installation](#4-setup-and-installation)
    *   [Prerequisites](#prerequisites)
    *   [Cloning the Repository](#cloning-the-repository)
    *   [Virtual Environment](#virtual-environment)
    *   [Install Dependencies](#install-dependencies)
    *   [Database Migrations](#database-migrations)
5.  [Running the Application](#5-running-the-application)
6.  [Key Files Overview](#6-key-files-overview)
7.  [Internationalization (i18n)](#7-internationalization-i18n)
8.  [GitHub Integration](#8-github-integration)
9.  [Project Carousel Functionality](#9-project-carousel-functionality)
10. [Future Improvements](#10-future-improvements)

---

## 1. Introduction
This project is a dynamic portfolio website built using Django, a high-level Python web framework, and styled with Tailwind CSS. It's designed to showcase a developer's GitHub projects, technical expertise, and educational background in an interactive and visually appealing manner. The application integrates directly with the GitHub API to fetch and display repository data, provides an interactive language distribution radar chart, and features an auto-scrolling, infinite-looping project carousel.

## 2. Features
*   **Dynamic GitHub Project Display:** Fetches and displays public repositories from a specified GitHub user, including project name, description, stars, forks, languages, and last updated time.
*   **Language Distribution Radar Chart:** Visualizes the developer's language proficiency based on their GitHub projects, showing a dynamic radar-like graph.
*   **GitHub Statistics:** Displays key metrics such as total commits, OSS contributions, years of experience, and system uptime.
*   **Auto-scrolling Project Carousel:** Presents GitHub projects in an interactive, infinitely looping carousel with pause-on-hover functionality and smooth transitions.
*   **Internationalization (i18n):** Supports language switching (English and Spanish) using Django's built-in i18n features.
*   **Dedicated Education Section:** A separate page to detail educational background and technical stack.
*   **Modern UI with Tailwind CSS:** Clean, responsive, and modern user interface.

## 3. Project Structure
The project follows a standard Django project layout:

```
.
├── core/                     # Main Django project settings
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py           # Project settings, i18n configuration
│   ├── urls.py               # Main URL dispatcher, i18n patterns
│   └── wsgi.py
├── locale/                   # Directory for translation files
│   └── es/
│       └── LC_MESSAGES/
│           └── django.po
├── portafolio/               # Django app for portfolio content
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py               # App-specific URL patterns
│   ├── views.py              # View logic for pages, GitHub API interaction
│   └── templates/
│       ├── base.html         # Base template, includes nav and footer
│       ├── home.html         # Home page content (GitHub stats, radar, carousel)
│       └── education.html    # Education page content
├── manage.py                 # Django's command-line utility
├── requirements.txt          # Project dependencies
└── venv/                     # Python virtual environment (ignored by Git)
```

## 4. Setup and Installation

### Prerequisites
Before you begin, ensure you have the following installed:
*   Python 3.8+
*   pip (Python package installer)
*   git

### Cloning the Repository
First, clone the project repository to your local machine:

```bash
git clone https://github.com/javiarias000/your-portfolio-repo.git # Replace with actual repo URL
cd your-portfolio-repo
```

### Virtual Environment
It's highly recommended to use a Python virtual environment to manage project dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: `venv\Scripts\activate`
```

### Install Dependencies
Install all required Python packages using pip:

```bash
pip install -r requirements.txt
```

### Database Migrations
Apply the initial database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

## 5. Running the Application
To start the Django development server:

```bash
python manage.py runserver
```
The application will be accessible at `http://127.0.0.1:8000/` or `http://127.0.0.1:8000/en/` for the English version.

## 6. Key Files Overview

*   **`core/settings.py`**: Configures the Django project. Crucial for `i18n` setup (middleware, `LANGUAGES`, `LOCALE_PATHS`), and specifies the template directories (`DIRS`).
*   **`core/urls.py`**: The main URL configuration. It includes `i18n_patterns` to enable language prefixes in URLs and maps the `set_language` view for language switching, along with the `portafolio` app's URLs.
*   **`portafolio/views.py`**: Contains the logic for rendering the `home` and `education` pages. The `home` view handles fetching data from the GitHub API, calculating language distribution for the radar chart, and preparing the context for the template.
*   **`portafolio/templates/base.html`**: The foundational HTML structure for all pages. It includes the navigation bar, footer, and defines `{% block content %}` and `{% block title %}` for child templates to extend. It also contains the dynamic language selector.
*   **`portafolio/templates/home.html`**: Extends `base.html` and provides the main content for the landing page. This includes the hero section, dynamic GitHub statistics, the interactive language intelligence radar chart, and the auto-scrolling project carousel.
*   **`portafolio/templates/education.html`**: Extends `base.html` and displays the educational background and hardcoded technical stack (Frontend, Backend, Infrastructure).

## 7. Internationalization (i18n)
The project supports English (`en`) and Spanish (`es`).
*   **Middleware:** `django.middleware.locale.LocaleMiddleware` is enabled in `settings.py`.
*   **URL Patterns:** `i18n_patterns` wraps the main URL patterns in `core/urls.py`, allowing URL prefixes like `/en/home` or `/es/home`.
*   **Language Selector:** The navigation bar in `base.html` provides buttons to switch languages, utilizing Django's built-in `set_language` view.
*   **Translation Files:** Translation strings are managed in the `locale/` directory using `django.po` files. To create/update translation files, run:
    ```bash
    python manage.py makemessages -l es
    python manage.py compilemessages
    ```

## 8. GitHub Integration
The `portafolio/views.py` file connects to the GitHub API to:
*   Fetch a list of public repositories for a specified GitHub username (`javiarias000`).
*   Aggregate total stars and forks across these repositories.
*   Calculate the percentage distribution of programming languages used in these projects.
*   Fetch the total commit count for a specific repository (`SGA1` in this case).
All this data is passed to `home.html` for dynamic display.

## 9. Project Carousel Functionality
The project carousel in `home.html` is implemented using custom JavaScript and Tailwind CSS.
*   **Auto-scrolling:** The carousel automatically scrolls through projects with a configurable `scrollIntervalTime` (e.g., 5 seconds).
*   **Pause on Hover:** Auto-scrolling pauses when the mouse cursor is over the carousel and resumes when the cursor leaves.
*   **Continuous Loop:** Items are dynamically cloned and prepended/appended to the carousel. When the scroll position reaches a cloned section, it instantly jumps back to the corresponding "real" section, creating a seamless, infinite loop effect without abrupt jumps.
*   **Manual Navigation:** "Previous" and "Next" buttons allow users to manually scroll by one project card width, and auto-scrolling continues in the background.
*   **Smooth Transition:** CSS `scroll-smooth` property is used for fluid scrolling between items.

## 10. Future Improvements
*   **Dynamic Tech Stack for Education Page:** Implement a mechanism to dynamically populate the "Stack & Tools" section on the education page, possibly by manually tagging projects with specific frameworks/libraries or integrating with external APIs that provide deeper project analysis.
*   **Responsive Design Refinements:** Further optimize layout and element sizing for various screen sizes.
*   **Error Handling and Loading States:** Enhance user experience with more robust error handling and loading indicators for GitHub API calls.
*   **Backend for Project Details:** Implement a Django model to store more detailed project information (e.g., specific technical problems solved, implementation details) that are not directly available from the GitHub API.
*   **CI/CD Pipeline:** Set up continuous integration and deployment for automated testing and deployment.
*   **Accessibility (A11y):** Improve accessibility features for users with disabilities.
