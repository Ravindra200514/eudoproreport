# 🎓 EduPro — Learner Demographics & Course Enrollment Analysis

> A full-stack data analytics project that generates synthetic e-learning data and visualises it through a stunning interactive Streamlit dashboard.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-red?style=flat-square&logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-5.18%2B-3F4F75?style=flat-square&logo=plotly)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 🚀 Features

| Module | Highlights |
|--------|-----------|
| **Data Generator** | 2,000 users · 80 courses · 12,000 transactions |
| **Demographics Tab** | Age histogram, gender donut, subscription funnel, age×subscription heatmap |
| **Enrollment Trends** | Monthly area chart, category bars, completion pie, device trends |
| **Course Insights** | Top-15 courses, rating violin, category matrix, price-rating bubble |
| **Revenue** | Monthly bar, category breakdown, payment method split |
| **Geo Analysis** | Choropleth world map, country rankings |
| **Deep Dive** | Coupon impact, hours completed, learner ratings, raw data table |

---

## 📁 Project Structure

```
.
├── generate_data.py   # Synthetic data generator
├── app.py             # Streamlit dashboard
├── requirements.txt   # Python dependencies
├── data/              # Auto-created CSVs (gitignored)
│   ├── users.csv
│   ├── courses.csv
│   └── transactions.csv
└── README.md
```

---

## ⚡ Quick Start

```bash
# 1. Clone
git clone https://github.com/praja/edupro-analysis.git
cd edupro-analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate synthetic data
python generate_data.py

# 4. Launch dashboard
streamlit run app.py
```

Open **http://localhost:8501** in your browser. 🎉

---

## 📊 Dashboard Preview

The dashboard features a dark glassmorphism design with:
- 🌈 Gradient hero header
- 📦 5 KPI metric cards
- 🗂️ 6 interactive tabs
- 🔍 Sidebar filters (Country, Category, Level, Subscription)

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Streamlit** — Dashboard framework
- **Plotly** — Interactive charts
- **Pandas / NumPy** — Data manipulation
- **Faker** — Synthetic data generation

---

## 📄 License

MIT © 2024 EduPro Analytics
