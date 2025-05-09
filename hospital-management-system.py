import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
import datetime
import heapq
from dataclasses import dataclass
import re

# Database Manager
class DatabaseManager:
    def __init__(self, db_file='hospital.db'):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER,
                gender TEXT,
                contact TEXT,
                medical_history TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER,
                appointment_time TEXT,
                priority INTEGER,
                status TEXT,
                FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS consultations (
                consultation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                appointment_id INTEGER,
                diagnosis TEXT,
                cost REAL,
                blood_type TEXT,
                other_questions TEXT,
                FOREIGN KEY (appointment_id) REFERENCES appointments (appointment_id)
            )
        ''')
        self.conn.commit()

    def add_patient(self, patient_id, name, age, gender, contact, medical_history):
        try:
            self.cursor.execute('''
                INSERT INTO patients (patient_id, name, age, gender, contact, medical_history)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (patient_id, name, age, gender, contact, medical_history))
            self.conn.commit()
            return patient_id
        except sqlite3.IntegrityError:
            raise ValueError("Patient ID already exists")

    def add_appointment(self, patient_id, appointment_time, priority, status='scheduled'):
        self.cursor.execute('''
            INSERT INTO appointments (patient_id, appointment_time, priority, status)
            VALUES (?, ?, ?, ?)
        ''', (patient_id, appointment_time, priority, status))
        self.conn.commit()
        return self.cursor.lastrowid

    def add_consultation(self, appointment_id, diagnosis, cost, blood_type, other_questions):
        self.cursor.execute('''
            INSERT INTO consultations (appointment_id, diagnosis, cost, blood_type, other_questions)
            VALUES (?, ?, ?, ?, ?)
        ''', (appointment_id, diagnosis, cost, blood_type, other_questions))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_patient(self, patient_id):
        self.cursor.execute('SELECT * FROM patients WHERE patient_id = ?', (patient_id,))
        return self.cursor.fetchone()

    def get_all_patients(self):
        self.cursor.execute('SELECT * FROM patients')
        return self.cursor.fetchall()

    def get_scheduled_appointments(self):
        self.cursor.execute('SELECT * FROM appointments WHERE status = "scheduled" ORDER BY priority ASC, appointment_time ASC')
        return self.cursor.fetchall()

    def update_appointment_status(self, appointment_id, status):
        self.cursor.execute('UPDATE appointments SET status = ? WHERE appointment_id = ?', (status, appointment_id))
        self.conn.commit()

    def delete_patient(self, patient_id):
        self.cursor.execute('DELETE FROM patients WHERE patient_id = ?', (patient_id,))
        self.cursor.execute('DELETE FROM appointments WHERE patient_id = ?', (patient_id,))
        self.conn.commit()

    def get_consultations(self):
        self.cursor.execute('SELECT c.*, a.patient_id, p.name FROM consultations c JOIN appointments a ON c.appointment_id = a.appointment_id JOIN patients p ON a.patient_id = p.patient_id')
        return self.cursor.fetchall()

# Patient Class
@dataclass
class Patient:
    patient_id: int
    name: str
    age: int
    gender: str
    contact: str
    medical_history: str

# Appointment Class
@dataclass
class Appointment:
    appointment_id: int
    patient_id: int
    appointment_time: datetime.datetime
    priority: int
    status: str = 'scheduled'

    def __lt__(self, other):
        return (self.priority, self.appointment_time, self.appointment_id) < (other.priority, other.appointment_time, other.appointment_id)

    def __eq__(self, other):
        return (self.priority, self.appointment_time, self.appointment_id) == (other.priority, other.appointment_time, other.appointment_id)

# Linked List for Patients
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def delete(self, patient_id):
        current = self.head
        previous = None
        while current:
            if current.data.patient_id == patient_id:
                if previous:
                    previous.next = current.next
                else:
                    self.head = current.next
                return True
            previous = current
            current = current.next
        return False

    def search(self, patient_id):
        current = self.head
        while current:
            if current.data.patient_id == patient_id:
                return current.data
            current = current.next
        return None

    def get_all_patients(self):
        patients = []
        current = self.head
        while current:
            patients.append(current.data)
            current = current.next
        return patients

# Priority Queue for Appointments
class PriorityQueue:
    def __init__(self):
        self._heap = []

    def push(self, item):
        heapq.heappush(self._heap, (item.priority, item.appointment_time, item.appointment_id, item))

    def pop(self):
        while self._heap:
            priority, appointment_time, appointment_id, item = heapq.heappop(self._heap)
            if item.status == 'scheduled':
                return item
        return None

    def peek(self):
        while self._heap:
            priority, appointment_time, appointment_id, item = self._heap[0]
            if item.status == 'scheduled':
                return item
            else:
                heapq.heappop(self._heap)
        return None

# Main Application
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)

        self.db = DatabaseManager()
        self.patients_list = LinkedList()
        self.appointments_queue = PriorityQueue()
        self.load_data()

        self.show_login()

    def load_data(self):
        patients = self.db.get_all_patients()
        for p in patients:
            patient = Patient(*p)
            self.patients_list.insert(patient)
        appointments = self.db.get_scheduled_appointments()
        for a in appointments:
            appointment_time = datetime.datetime.fromisoformat(a[2])
            appointment = Appointment(a[0], a[1], appointment_time, a[3], a[4])
            self.appointments_queue.push(appointment)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_main_frame()

        tk.Label(self.main_frame, text="Select Role:", font=("Arial", 12)).pack(pady=10)
        self.role_var = tk.StringVar()
        roles = ["Receptionist", "Doctor"]
        self.role_dropdown = ttk.Combobox(self.main_frame, textvariable=self.role_var, values=roles)
        self.role_dropdown.pack(pady=10)

        tk.Label(self.main_frame, text="Username:", font=("Arial", 12)).pack(pady=10)
        self.username_entry = tk.Entry(self.main_frame)
        self.username_entry.pack(pady=10)

        tk.Label(self.main_frame, text="Password:", font=("Arial", 12)).pack(pady=10)
        self.password_entry = tk.Entry(self.main_frame, show="*")
        self.password_entry.pack(pady=10)

        tk.Button(self.main_frame, text="Login", command=self.login, font=("Arial", 12)).pack(pady=20)

    def login(self):
        role = self.role_var.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if role == "Receptionist" and username == "reception" and password == "reception123":
            self.show_receptionist_panel()
        elif role == "Doctor" and username == "doctor" and password == "doctor123":
            self.show_doctor_panel()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def show_receptionist_panel(self):
        self.clear_main_frame()

        tk.Label(self.main_frame, text="Receptionist Panel", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.main_frame, text="Add Patient", command=self.show_add_patient, font=("Arial", 12)).pack(pady=10)
        tk.Button(self.main_frame, text="Schedule Appointment", command=self.show_schedule_appointment, font=("Arial", 12)).pack(pady=10)
        tk.Button(self.main_frame, text="View Schedule", command=self.show_view_schedule, font=("Arial", 12)).pack(pady=10)
        tk.Button(self.main_frame, text="Search Patient", command=self.show_search_patient, font=("Arial", 12)).pack(pady=10)
        tk.Button(self.main_frame, text="View Consultations", command=self.show_view_consultations, font=("Arial", 12)).pack(pady=10)
        tk.Button(self.main_frame, text="Logout", command=self.show_login, font=("Arial", 12)).pack(pady=10)

    def show_add_patient(self):
        self.clear_main_frame()

        tk.Label(self.main_frame, text="Add Patient", font=("Arial", 16)).pack(pady=20)
        fields = ["Patient ID", "Name", "Age", "Gender", "Contact", "Medical History"]
        entries = {}
        for i, field in enumerate(fields):
            tk.Label(self.main_frame, text=f"{field}:", font=("Arial", 12)).pack(pady=5)
            entry = tk.Entry(self.main_frame)
            entry.pack(pady=5)
            entries[field.lower().replace(" ", "_")] = entry

        def submit():
            patient_id_str = entries["patient_id"].get()
            if not (patient_id_str.isdigit() and len(patient_id_str) in [4, 5]):
                messagebox.showerror("Error", "Patient ID must be a 4 or 5 digit number")
                return

            contact = entries["contact"].get()
            if not re.match(r'^(09|07)\d{8}$', contact):
                messagebox.showerror("Error", "Phone number must start with 09 or 07 followed by 8 digits")
                return

            try:
                patient_id = int(patient_id_str)
                name = entries["name"].get()
                age = int(entries["age"].get())
                gender = entries["gender"].get()
                medical_history = entries["medical_history"].get()
                self.db.add_patient(patient_id, name, age, gender, contact, medical_history)
                patient = Patient(patient_id, name, age, gender, contact, medical_history)
                self.patients_list.insert(patient)
                messagebox.showinfo("Success", "Patient added successfully")
                self.show_receptionist_panel()
            except ValueError as e:
                messagebox.showerror("Error", "Invalid input: Ensure Age is a number")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Patient ID already exists")

        tk.Button(self.main_frame, text="Submit", command=submit, font=("Arial", 12)).pack(pady=20)
        tk.Button(self.main_frame, text="Back", command=self.show_receptionist_panel, font=("Arial", 12)).pack(pady=10)

    def show_schedule_appointment(self):
        self.clear_main_frame()

        tk.Label(self.main_frame, text="Schedule Appointment", font=("Arial", 16)).pack(pady=20)
        patients = self.patients_list.get_all_patients()
        patient_options = [f"{p.patient_id}: {p.name}" for p in patients] if patients else ["No patients"]
        patient_var = tk.StringVar(self.main_frame)
        patient_var.set(patient_options[0])

        tk.Label(self.main_frame, text="Patient:", font=("Arial", 12)).pack(pady=5)
        patient_dropdown = ttk.Combobox(self.main_frame, textvariable=patient_var, values=patient_options)
        patient_dropdown.pack(pady=5)

        tk.Label(self.main_frame, text="Time (YYYY-MM-DD HH:MM):", font=("Arial", 12)).pack(pady=5)
        time_entry = tk.Entry(self.main_frame)
        time_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Priority (1-Critical, 2-Urgent, 3-Normal):", font=("Arial", 12)).pack(pady=5)
        priority_entry = tk.Entry(self.main_frame)
        priority_entry.pack(pady=5)

        def submit():
            if not patients:
                messagebox.showerror("Error", "No patients available")
                return
            patient_selection = patient_var.get()
            patient_id = int(patient_selection.split(":")[0])
            try:
                appointment_time = datetime.datetime.strptime(time_entry.get(), "%Y-%m-%d %H:%M")
                priority = int(priority_entry.get())
                appointment_id = self.db.add_appointment(patient_id, appointment_time.isoformat(), priority)
                appointment = Appointment(appointment_id, patient_id, appointment_time, priority)
                self.appointments_queue.push(appointment)
                messagebox.showinfo("Success", "Appointment scheduled")
                self.show_receptionist_panel()
            except ValueError:
                messagebox.showerror("Error", "Invalid time format or priority")

        tk.Button(self.main_frame, text="Submit", command=submit, font=("Arial", 12)).pack(pady=20)
        tk.Button(self.main_frame, text="Back", command=self.show_receptionist_panel, font=("Arial", 12)).pack(pady=10)

    def show_view_schedule(self):
        self.clear_main_frame()

        tk.Label(self.main_frame, text="View Schedule", font=("Arial", 16)).pack(pady=20)
        appointments = self.db.get_scheduled_appointments()
        if not appointments:
            tk.Label(self.main_frame, text="No scheduled appointments", font=("Arial", 12)).pack(pady=10)
        else:
            tree = ttk.Treeview(self.main_frame, columns=("Appointment ID", "Patient ID", "Patient Name", "Time", "Priority"), show="headings")
            tree.heading("Appointment ID", text="Appointment ID")
            tree.heading("Patient ID", text="Patient ID")
            tree.heading("Patient Name", text="Patient Name")
            tree.heading("Time", text="Time")
            tree.heading("Priority", text="Priority")
            tree.pack(fill=tk.BOTH, expand=True, pady=10)
            for a in appointments:
                patient = self.db.get_patient(a[1])
                tree.insert("", tk.END, values=(a[0], a[1], patient[1], a[2], a[3]))

        tk.Button(self.main_frame, text="Back", command=self.show_receptionist_panel, font=("Arial", 12)).pack(pady=20)

    def show_search_patient(self):
        self.clear_main_frame()

        tk.Label(self.main_frame, text="Search Patient", font=("Arial", 16)).pack(pady=20)
        tk.Label(self.main_frame, text="Search by:", font=("Arial", 12)).pack(pady=5)
        search_var = tk.StringVar()
        search_options = ["ID", "Phone Number"]
        search_dropdown = ttk.Combobox(self.main_frame, textvariable=search_var, values=search_options)
        search_dropdown.pack(pady=5)

        tk.Label(self.main_frame, text="Value:", font=("Arial", 12)).pack(pady=5)
        value_entry = tk.Entry(self.main_frame)
        value_entry.pack(pady=5)

        def search():
            search_type = search_var.get()
            value = value_entry.get()
            if search_type == "ID":
                try:
                    patient_id = int(value)
                    patient = self.patients_list.search(patient_id)
                    if patient:
                        details = f"Name: {patient.name}\nAge: {patient.age}\nGender: {patient.gender}\nContact: {patient.contact}\nMedical History: {patient.medical_history}"
                        messagebox.showinfo("Patient Details", details)
                    else:
                        messagebox.showerror("Error", "Patient not found")
                except ValueError:
                    messagebox.showerror("Error", "Invalid Patient ID")
            elif search_type == "Phone Number":
                patients = self.patients_list.get_all_patients()
                for patient in patients:
                    if patient.contact == value:
                        details = f"ID: {patient.patient_id}\nName: {patient.name}\nAge: {patient.age}\nGender: {patient.gender}\nContact: {patient.contact}\nMedical History: {patient.medical_history}"
                        messagebox.showinfo("Patient Details", details)
                        return
                messagebox.showerror("Error", "Patient not found")

        tk.Button(self.main_frame, text="Search", command=search, font=("Arial", 12)).pack(pady=20)
        tk.Button(self.main_frame, text="Back", command=self.show_receptionist_panel, font=("Arial", 12)).pack(pady=10)

    def show_view_consultations(self):
        self.clear_main_frame()

        tk.Label(self.main_frame, text="View Consultations", font=("Arial", 16)).pack(pady=20)
        consultations = self.db.get_consultations()
        if not consultations:
            tk.Label(self.main_frame, text="No consultations", font=("Arial", 12)).pack(pady=10)
        else:
            tree = ttk.Treeview(self.main_frame, columns=("Consultation ID", "Appointment ID", "Patient ID", "Patient Name", "Diagnosis", "Cost", "Other Questions"), show="headings")
            tree.heading("Consultation ID", text="Consultation ID")
            tree.heading("Appointment ID", text="Appointment ID")
            tree.heading("Patient ID", text="Patient ID")
            tree.heading("Patient Name", text="Patient Name")
            tree.heading("Diagnosis", text="Diagnosis")
            tree.heading("Cost", text="Cost")
            tree.heading("Other Questions", text="Other Questions")
            tree.pack(fill=tk.BOTH, expand=True, pady=10)
            for c in consultations:
                tree.insert("", tk.END, values=(c[0], c[1], c[6], c[7], c[2], c[3], c[5]))

        tk.Button(self.main_frame, text="Back", command=self.show_receptionist_panel, font=("Arial", 12)).pack(pady=20)

    def show_doctor_panel(self):
        self.clear_main_frame()

        tk.Label(self.main_frame, text="Doctor Panel", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.main_frame, text="Complete Next Appointment", command=self.complete_next_appointment, font=("Arial", 12)).pack(pady=10)
        tk.Button(self.main_frame, text="Logout", command=self.show_login, font=("Arial", 12)).pack(pady=10)

    def complete_next_appointment(self):
        next_appointment = self.appointments_queue.pop()
        if next_appointment:
            self.show_consultation(next_appointment)
        else:
            messagebox.showinfo("Info", "No scheduled appointments")
            self.show_doctor_panel()

    def show_consultation(self, appointment):
        self.clear_main_frame()

        tk.Label(self.main_frame, text="Consultation", font=("Arial", 16)).pack(pady=20)
        tk.Label(self.main_frame, text=f"Patient: {self.db.get_patient(appointment.patient_id)[1]}", font=("Arial", 12)).pack(pady=10)
        tk.Label(self.main_frame, text="Diagnosis:", font=("Arial", 12)).pack(pady=5)
        diagnosis_entry = tk.Entry(self.main_frame)
        diagnosis_entry.pack(pady=5)
        tk.Label(self.main_frame, text="Cost:", font=("Arial", 12)).pack(pady=5)
        cost_entry = tk.Entry(self.main_frame)
        cost_entry.pack(pady=5)
        tk.Label(self.main_frame, text="Other Questions/Notes:", font=("Arial", 12)).pack(pady=5)
        other_questions_text = tk.Text(self.main_frame, height=5, width=50)
        other_questions_text.pack(pady=5)

        def submit():
            diagnosis = diagnosis_entry.get()
            cost_str = cost_entry.get()
            other_questions = other_questions_text.get("1.0", tk.END).strip()
            if not diagnosis:
                messagebox.showerror("Error", "Please enter a diagnosis")
                return
            try:
                cost = float(cost_str)
            except ValueError:
                messagebox.showerror("Error", "Cost must be a number")
                return
            self.db.add_consultation(appointment.appointment_id, diagnosis, cost, '', other_questions)
            self.db.update_appointment_status(appointment.appointment_id, 'completed')
            appointment.status = 'completed'
            messagebox.showinfo("Success", "Consultation completed")
            self.show_doctor_panel()

        tk.Button(self.main_frame, text="Submit", command=submit, font=("Arial", 12)).pack(pady=20)
        tk.Button(self.main_frame, text="Back", command=self.show_doctor_panel, font=("Arial", 12)).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()