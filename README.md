# Home Tuition Service Website

A professional website for managing home tuition services, built with Flask and MySQL.

## Features

- Modern and responsive design using Tailwind CSS
- User authentication for tutors and admin
- Booking system for tuition sessions
- Tutor registration and profile management
- Testimonials management
- Contact form with database integration

## Tech Stack

- Python 3.10
- Flask 3.0.0
- MySQL (via XAMPP/phpMyAdmin)
- Tailwind CSS
- JavaScript

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Home-tuition
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up MySQL database:
- Install XAMPP
- Start Apache and MySQL services
- Create a new database named 'home_tuition'
- Import the provided SQL schema

5. Create .env file:
```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=mysql://username:password@localhost/home_tuition
```

6. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

7. Run the application:
```bash
python run.py
```

Visit `http://localhost:5000` in your browser.

## Project Structure

```
Home-tuition/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── templates/
│   └── utils/
├── migrations/
├── .env
├── .gitignore
├── README.md
├── requirements.txt
└── run.py
```

## Database Schema

The application uses the following main tables:

1. Users (Admin/Parents)
2. Tutors
3. Subjects
4. Bookings
5. Testimonials
6. Contact Messages

Detailed schema information can be found in the database documentation.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License. 