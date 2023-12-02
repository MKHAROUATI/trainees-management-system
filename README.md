# django
 
# Stagiaire Management System

The Stagiaire Management System is a Django web application designed to manage information related to stagiaires, their permissions, reservations, and other associated details within different groups.

## Features

- **User Authentication**: Utilizes Django's built-in `AbstractUser` model for user authentication.
- **Groupe Management**: Allows the creation of groups with specific names and owners.
- **Stagiaire Information**: Manages information about stagiaires including their names, grades, units, countries, and group associations.
- **Permissions Tracking**: Tracks permissions granted to stagiaires including reasons, destinations, and durations.
- **Renseignement and Consultation**: Manages additional details such as files and medical consultations for stagiaires.
- **Reservation Management**: Tracks reservations made by stagiaires including destination, duration, dates, and accompanying details.

## Models

### CustomUser

Extends Django's `AbstractUser` for custom user functionality, including an additional `grade` field.

### Groupe

Represents a group with a specific name, an owner (linked to `CustomUser`), and creation/update timestamps.

### Stagiaire

Manages information about stagiaires, including their association with a group, name, grade, unit, country, and creation/update timestamps.

### Permission

Tracks permissions granted to stagiaires, including the stagiaire associated, motif, destination, duration, dates, and creation/update timestamps.

### Renseignement

Manages additional information about stagiaires, including files and creation/update timestamps.

### Consultation

Tracks medical consultations for stagiaires, including the stagiaire associated, medical decision, and creation/update timestamps.

### Reservation

Tracks reservations made by stagiaires, including the stagiaire associated, destination, duration, dates, accompanying details, and creation/update timestamps.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/stagiaire-management-system.git
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Apply database migrations:

bash
Copy code
python manage.py migrate
Create a superuser for administrative access:

bash
Copy code
python manage.py createsuperuser
Run the development server:

bash
Copy code
python manage.py runserver
Visit http://localhost:8000/admin/ to access the Django admin and manage your Stagiaire Management System.

Usage
Log in with the superuser credentials created during installation.
Use the Django admin interface to manage Groupe, Stagiaire, Permission, Renseignement, Consultation, and Reservation records.
Contributing
Feel free to contribute to the project by opening issues or submitting pull requests. Follow the contributing guidelines for more details.

License
This project is licensed under the MIT License.

vbnet
Copy code

This README file provides a brief overview of the project, its features, mod