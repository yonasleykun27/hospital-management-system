# 🏥 Hospital Management System

[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

*A desktop application built with Python, SQLite, and Tkinter for efficient hospital/clinic management.*

---

## 📑 Table of Contents

1. [✨ Features](#✨-features)
2. [🛠️ Technologies](#🛠️-technologies)
3. [🚀 Quick Start](#🚀-quick-start)
4. [📂 Project Structure](#📂-project-structure)
5. [📋 Usage](#📋-usage)
6. [🛡️ Contributing](#🛡️-contributing)
7. [⚖️ License](#⚖️-license)

---

## ✨ Features

* **Role-Based Access**: Separate panels for Receptionist and Doctor.
* **Patient Management**: Add, search, and remove patients with validation.
* **Appointment Scheduling**: Prioritize (Critical, Urgent, Normal) and sort by time.
* **Consultation Logging**: Record diagnosis, cost, and notes; track completed visits.
* **Persistent Storage**: SQLite database (`hospital.db`) auto-creates tables on first run.
* **User-Friendly UI**: Built on Tkinter with clear forms and tables.

---

## 🛠️ Technologies

* **Python 3.x**
* **SQLite** (via `sqlite3` module)
* **Tkinter** (GUI toolkit)
* **Dataclasses** & **heapq** (in-memory data handling)

---

## 🚀 Quick Start

1. **Clone repository**

   ```bash
   git clone https://github.com/your-username/hospital-management-system.git
   cd hospital-management-system
   ```

2. **(Optional) Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   > *No external dependencies; uses standard library*
   > If you add extras, list them in `requirements.txt` and run:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run application**

   ```bash
   python app.py
   ```

   * **Receptionist**: `reception` / `reception123`
   * **Doctor**:       `doctor`    / `doctor123`

---

## 📂 Project Structure

```text
hospital-management-system/
├── app.py                # Main application script
├── hospital.db           # SQLite database (auto-generated)
├── requirements.txt      # (Optional) Python dependencies
├── LICENSE               # MIT License
└── README.md             # Project documentation
```

---

## 📋 Usage

### Receptionist Panel

1. **Add Patient**: Enter ID (4–5 digits), Name, Age, Gender, Contact (09xx or 07xx), Medical History.
2. **Schedule Appointment**: Select patient, choose date/time (`YYYY-MM-DD HH:MM`), set priority (1–3).
3. **View Schedule**: See upcoming appointments sorted by priority & time.
4. **Search Patient**: Lookup by ID or phone number.
5. **View Consultations**: Review completed consultations.

### Doctor Panel

1. **Complete Next Appointment**: Pops next scheduled appointment.
2. **Consultation Form**: Enter diagnosis, cost, notes; marks appointment as completed.

---

## 🛡️ Contributing

1. **Fork** the repo
2. **Branch**: `git checkout -b feature/YourFeature`
3. **Commit**: `git commit -m "Add awesome feature"`
4. **Push**: `git push origin feature/YourFeature`
5. **PR**: Open a Pull Request

*Please follow [Contributor Guidelines](CONTRIBUTING.md) if available.*

---

## ⚖️ License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.
