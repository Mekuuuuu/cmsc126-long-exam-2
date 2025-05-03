# 💰 SimpliFi - Budget Tracker Web App

SimpliFi is a lightweight and user-friendly budget tracking web application designed to help users manage their income and expenses effectively. With a simple interface and core features like real-time data entry, categorized reports, and responsive design, SimpliFi allows users to take control of their finances effortlessly.

---

## 🚀 Features

- 📊 **Dashboard Overview** – See your total income, expenses, and remaining balance at a glance.
- ➕ **Add/Edit/Delete Entries** – Quickly manage your financial records.
- 🗂️ **Category-Based Tracking** – Organize expenses by category (e.g., food, transport, utilities).
- 📅 **Date Filtering** – Generate reports based on date range.
- 🧾 **Report Generation** – Download financial summaries.
- 📱 **Responsive Design** – Works on desktop, tablet, and mobile.

---

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Django (Python)
- **Database**: MySQL
- **Styling**: Vanilla CSS
- **Version Control**: Git & GitHub

---

## 👨‍👩‍👧‍👦 Team & Responsibilities

| Member                   | Role                                  | Responsibilities                                                  |
|--------------------------|---------------------------------------|-------------------------------------------------------------------|
| Abadia, Miko Tristan     | Backend Developer                     | Database setup, income/expense logic, and report generation       |
| Gucor, Lovely Shane      | Frontend Developer & Designer         | UI design, dashboard, and responsiveness, visual design           |
| Peladas, Zayne Bridget   | Frontend Developer & Designer         | UI design, dashboard, and responsiveness, visual design, README   |

All team members contributed meaningfully using Git with regular commits and branch-based development.

---

## ⚙️ Setup Instructions

To run SimpliFi locally, follow these steps:

### 1. Clone the repository
First, clone the project to your local machine using Git:
```bash
git clone https://github.com/Mekuuuuu/cmsc126-long-exam-2.git
cd cmsc126-long-exam-2
```


### 2. Set Python Version

Make sure you have [pyenv](https://github.com/pyenv/pyenv) installed. Set the local Python version to `3.10.13`:

```bash
pyenv local 3.10.13/n
```

If you don’t have that version installed, run:
```bash
pyenv install 3.10.13
```

### 3. Create and Activate a Virtual Environment
Install `virtualenv` if you haven't already:
```bash
python -m pip install virtualenv
```

Then create a virtual environment in the project folder:
```bash
python -m virtualenv venv
```

Activate the virtual environment:
```bash
source venv/bin/activate
```

You can verify it's active by checking the Python path:
```bash
which python
```
If the output ends with venv/bin/python, you're good.

### 4. Install Dependencies
Install the required packages:
```bash
pip install -r requirements.txt
```

If you are adding new modules, don't forget to update the file:
```bash
pip freeze > requirements.txt
```

### 5. Go to budget_tracker
Access manage.py for migration and runserver
```bash
cd budget_tracker
```

### 6. Apply Migration
Set up the database:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Run the Server
Start the development server:
```bash
python manage.py runserver
```

Open your browser and go to `http://127.0.0.1:8000/` to use SimpliFi.

To deactivate your virtual environment anytime:
```bash
deactivate
```

## 🖼️ Feature Walkthrough
Get a visual overview of SimpliFi’s core features:

### 📊 Dashboard Overview  
Displays total **Income**, **Expenses**, and **Remaining Balance** at a glance.

![Dashboard Screenshot](/path/to/dashboard.png)

---

### ➕ Add Income/Expense Entry  
Easily input financial records with category and amount fields.

![Add Entry Screenshot](/path/to/add-entry.png)

---

### 🗂️ Categorized Records  
View transactions grouped by categories like **Food**, **Transport**, and **Utilities**.

![Category Screenshot](/path/to/categories.png)

---

### 📅 Filter by Date  
Use the date filter to generate reports within a specific time range.

![Date Filter Screenshot](/path/to/date-filter.png)

---

### 🧾 Generate Report  
Download a summary of your transactions in a readable format.

![Report Screenshot](/path/to/report.png)

---

### 📱 Responsive Design  
SimpliFi is mobile-friendly and adapts to all screen sizes.

![Mobile View Screenshot](/path/to/mobile.png)

