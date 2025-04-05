# EduConnectNigeria

EduConnect Nigeria is an innovative digital learning platform designed to bridge the educational gap in rural Nigeria. It provides offline access to digital resources, interactive lessons, virtual classrooms, and online tutoring, ensuring quality education for all, regardless of internet availability.

## Features

- **User Authentication**: Custom user model with roles (Student, Teacher, Admin).
- **Course Management**: Create and manage courses with descriptions and instructors.
- **Learning Materials**: Upload and manage learning resources (PDFs, videos, etc.).
- **Quizzes and Questions**: Interactive quizzes with multiple-choice questions.
- **Forums**: Discussion boards for collaborative learning.
- **Tutoring Sessions**: One-on-one tutoring with scheduled sessions.
- **Progress Tracking**: Monitor student progress in courses.
- **AI-Powered Solver**: Instantly solve academic questions with step-by-step explanations using AI.

## Project Structure

educonnectnigeria/
│── manage.py
│── db.sqlite3
│── requirements.txt
│
├── educonnectnigeria/  # Main Django project folder
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│
├── ai_solver/  # AI-powered question solver
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│
├── assessments/  # Quizzes and tests
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│
├── courses/  # Course management
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│
├── forums/  # Discussion forums
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│
├── progress_tracking/  # Student progress tracking
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│
├── tutoring/  # Tutoring sessions
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
├── users/  # User authentication & management
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py




## Installation

### Prerequisites
- Python 3.x
- Django
- Virtual environment (optional but recommended)

### Setup
```sh
# Clone the repository
git clone https://github.com/lohochris/EduConnectNigeria.git
cd EduConnectNigeria

# Create a virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Create a superuser for the admin panel
python manage.py createsuperuser

# Run the development server
python manage.py runserver


Usage
Navigate to http://127.0.0.1:8000/ in your browser.

Log in with your superuser credentials.

Start adding courses, materials, quizzes, and explore AI-powered solving and tutoring sessions!

Contributing
Contributions are welcome! To contribute:

Fork the repository.

Create a new branch (git checkout -b feature-branch).

Commit your changes (git commit -m 'Add feature').

Push to the branch (git push origin feature-branch).

Open a Pull Request.

License
This project is licensed under the MIT License.

Contact
For inquiries, contact Loho Christopher at lohochris@gmail.com.