# Project Portfolio - Django & Tailwind CSS

[![Python Version](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/Django-4.1-green.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Description
This is a dynamic and interactive personal portfolio website built with Django and styled using Tailwind CSS. It's designed to powerfully showcase a developer's work by integrating directly with the GitHub API to display projects, visualize language proficiency, and present key statistics. The site features internationalization support (English/Spanish) and a smooth, auto-scrolling project carousel.

## Features
*   **Dynamic GitHub Projects:** Fetches and displays public repositories from your GitHub profile.
*   **Interactive Language Radar Chart:** Visual representation of programming language distribution across your projects.
*   **Key GitHub Statistics:** Highlights total commits, open-source contributions, and more.
*   **Auto-Scrolling Project Carousel:** Seamlessly browse projects with an infinite loop, pause-on-hover, and smooth transitions.
*   **Internationalization (i18n):** Supports multiple languages (English and Spanish).
*   **Clean & Responsive UI:** Modern design built with Tailwind CSS.
*   **Dedicated Education Section:** Page detailing academic background and technical stack.

## Technologies Used
*   **Backend:** Python, Django
*   **Frontend:** HTML, CSS, JavaScript
*   **Other:** Bash, GraphQL, Databases

## Setup and Installation

### Prerequisites
*   Python 3.8+
*   pip (Python package installer)
*   git

### Steps
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/javiarias000/your-portfolio-repo.git # Replace with your actual repo URL
    cd your-portfolio-repo
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply database migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

## How to Run
To start the Django development server:

```bash
python manage.py runserver
```

Open your web browser and navigate to `http://127.0.0.1:8000/` (or `http://127.0.0.1:8000/en/` for English).

## Customization
*   **GitHub Username:** Update `github_username` in `portafolio/views.py` to display your own projects.
*   **Localization:** Add more languages by creating new translation files in the `locale/` directory.

## Contributing
Contributions are welcome! Please feel free to open issues or submit pull requests.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
