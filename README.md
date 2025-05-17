
# 💰 Budget & Expense Visualization Web App

A **Flask-based web application** that lets users upload their **bank statements**, automatically **categorizes expenses**, and displays **interactive visual dashboards** for better financial tracking and budgeting.

---

## 📌 Features

- 📄 Upload bank statements (CSV/XLSX)
- 🧠 Automatically categorize expenses (e.g., Food, Travel, Bills)
- 📊 Visualize spending via Pie Charts, Bar Graphs, Line Charts
- 📅 Filter by date range and category
- 💾 Store and manage data securely in MySQL
- ⚡ Built for speed and usability

---

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS, JavaScript, Chart.js
- **Backend**: Python, Flask
- **Database**: MySQL (with SQLAlchemy ORM)
- **Parsing & Logic**: Pandas, Regex, NumPy

---

## 📂 Folder Structure

```
budget-visualization/
│
├── static/                  # CSS, JS files
│   ├── css/
│   └── js/
├── templates/               # HTML templates
│   ├── index.html
│   ├── upload.html
│   └── dashboard.html
├── uploads/                 # Uploaded statements
├── app.py                   # Flask app entry point
├── models.py                # Database models
├── utils.py                 # Parsing & categorization functions
├── config.py                # DB config
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/budget-visualization.git
cd budget-visualization
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up MySQL

- Create a database:

```sql
CREATE DATABASE budget_app;
```

- Update `config.py` with your DB credentials:

```python
DB_USERNAME = 'root'
DB_PASSWORD = 'your_password'
DB_HOST = 'localhost'
DB_NAME = 'budget_app'
```

### 5. Initialize the Database

```bash
python
>>> from app import db
>>> db.create_all()
>>> exit()
```

### 6. Run the App

```bash
python app.py
```

Then visit `http://127.0.0.1:5000` in your browser.

---

## 🧭 Workflow

```
1. Upload bank statement (.csv/.xlsx)
2. Parse transactions using Pandas
3. Auto-categorize using keywords
4. Store data in MySQL
5. Render interactive charts (Chart.js)
6. Filter and track expense patterns
```

---



## 📦 Example Statement Format (CSV)

| Date       | Description         | Amount  | Type    |
|------------|---------------------|---------|---------|
| 2025-01-01 | Starbucks Coffee    | -150.00 | Debit   |
| 2025-01-03 | Salary              | +30000  | Credit  |
| 2025-01-05 | Uber Ride           | -300.00 | Debit   |

---

## 🔮 Future Scope

- Login/Signup Authentication
- AI-based Smart Categorization
- Email Monthly Reports
- Export PDFs of expenses

---

## 🤝 Contributing

Pull requests and feature suggestions are welcome! Open an issue for discussions.

---

## 📜 License

MIT License. See the [LICENSE](LICENSE) file for details.

---

