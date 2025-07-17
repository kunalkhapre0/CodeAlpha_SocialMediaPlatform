# FeedFlip - Social Media Platform (Task 2)

FeedFlip is a mini social media platform built with Python and Django as part of the CodeAlpha Full Stack Development Internship.

## Features

*   User Registration and Login
*   User Profiles with Bio and Profile Pictures
*   Create, View, Edit, and Delete Posts (with optional image uploads)
*   Commenting on Posts
*   Liking/Unliking Posts
*   Following/Unfollowing Users
*   User Search Functionality
*   Responsive Design for Desktop and Mobile

  ## Live Demo

*   **Live URL:** - [DEMO LINK](https://feedflip.pythonanywhere.com/)

## Technologies Used

*   **Backend:** Python, Django
*   **Frontend:** HTML, CSS, JavaScript
*   **Database:** SQLite (for development)
*   **Key Django Packages:**
    *   `Pillow` (for image handling)
    *   `python-decouple` (for environment variable management)
*   **Frontend Libraries/Frameworks (if any):**
    *   Font Awesome (for icons)

## Setup and Run Locally

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/CodeAlpha_SocialMediaPlatform.git
    cd CodeAlpha_SocialMediaPlatform
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv_social
    # On Windows:
    # venv_social\Scripts\activate
    # On macOS/Linux:
    # source venv_social/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Create a `.env` file** in the project root and add your settings:
    ```env
    SECRET_KEY=your_very_secret_random_key_here
    DEBUG=True
    # Add other necessary environment variables if any
    ```
5.  **Apply migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
6.  **Create a superuser (for admin access):**
    ```bash
    python manage.py createsuperuser
    ```
7.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The application will be available at `http://127.0.0.1:8000/`.

## Screenshots 

![1](https://github.com/user-attachments/assets/f326fa81-e3fd-44d7-9362-d367ad735920)

![2](https://github.com/user-attachments/assets/d2214147-33d8-4d8c-8e96-93f447bab571)

![3](https://github.com/user-attachments/assets/4aafb2c7-f807-40b7-869e-87f3ca8834e5)

![4](https://github.com/user-attachments/assets/c00449e1-f057-4ade-9447-fa68325787a5)

![5](https://github.com/user-attachments/assets/f81fc21a-15f1-488b-b9c6-0bae65c780c6)

![6](https://github.com/user-attachments/assets/73c9d65b-355a-444b-9013-6767ae5ec8d2)

## Author

*   Muhammed Basil
*   [LinkedIn profile](https://www.linkedin.com/in/muhammed-basil-a83443317/)
*   [GitHub profile](https://github.com/diceflip)
