Hospital Management System
Overview
The Hospital Management System is a Python-based desktop application designed to streamline hospital operations, including patient management, appointment scheduling, and consultation tracking. It uses SQLite for data storage, Tkinter for the GUI, and implements data structures like linked lists and priority queues for efficient data handling. The system supports two user roles: Receptionist and Doctor, each with specific functionalities.
Features

Receptionist Panel:
Add new patients with validation for patient ID and phone number.
Schedule appointments with priority levels (Critical, Urgent, Normal).
View the appointment schedule.
Search patients by ID or phone number.
View consultation records.


Doctor Panel:
Complete the next scheduled appointment by recording consultation details (diagnosis, cost, notes).


Data Management:
SQLite database for storing patients, appointments, and consultations.
Linked list for in-memory patient data management.
Priority queue for scheduling appointments based on priority and time.


Security:
Role-based login system with the following credentials:
Receptionist: Username: reception, Password: reception123
Doctor: Username: doctor, Password: doctor123





Prerequisites

Python 3.6 or higher
Required Python libraries: sqlite3, tkinter (usually included with Python), datetime, heapq, dataclasses, re

Installation

Clone the repository:git clone https://github.com/username/hospital-management-system.git


Navigate to the project directory:cd hospital-management-system


Run the application:python hospital_management.py



Usage

Launch the application using the command above.
Select a role (Receptionist or Doctor) and log in with the provided credentials:
Receptionist: reception / reception123
Doctor: doctor / doctor123


Use the respective panels to manage patients, appointments, or consultations.
Log out to return to the login screen.

Database Schema

patients: Stores patient details (patient_id, name, age, gender, contact, medical_history).
appointments: Stores appointment details (appointment_id, patient_id, appointment_time, priority, status).
consultations: Stores consultation details (consultation_id, appointment_id, diagnosis, cost, blood_type, other_questions).

Project Structure

hospital_management.py: Main application code containing all classes and logic.
hospital.db: SQLite database file (created automatically on first run).

Future Improvements

Add support for multiple doctors and scheduling conflicts.
Implement patient record editing and deletion.
Enhance security with proper user authentication and password hashing.
Add reporting features for consultations and appointments.
Improve the UI with a more modern design.

Contributing
Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request with your changes.
License
This project is licensed under the MIT License. See the LICENSE file for details.
Contact
For questions or suggestions, please open an issue on the GitHub repository or contact the maintainer at yonasleykun27@gmail.com.
