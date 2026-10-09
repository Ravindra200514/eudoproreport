"""
EduPro - Synthetic Data Generator
Generates synthetic datasets for Users, Courses, and Transactions
"""

import pandas as pd
import numpy as np
import random
from faker import Faker
import os

fake = Faker()
np.random.seed(42)
random.seed(42)

# ─── Config ───────────────────────────────────────────────────────────────────
N_USERS       = 2000
N_COURSES     = 80
N_TRANSACTIONS = 12000
OUTPUT_DIR    = "data"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─── Reference Data ───────────────────────────────────────────────────────────
COUNTRIES = [
    "India", "United States", "United Kingdom", "Canada", "Australia",
    "Germany", "France", "Brazil", "Mexico", "Singapore",
]
COUNTRY_WEIGHTS = [0.30, 0.22, 0.10, 0.07, 0.06, 0.05, 0.05, 0.07, 0.04, 0.04]

CATEGORIES = [
    "Data Science", "Web Development", "Mobile Development",
    "AI & Machine Learning", "Cloud Computing", "Cybersecurity",
    "UI/UX Design", "Business & Management", "Digital Marketing", "DevOps",
]

LEVELS      = ["Beginner", "Intermediate", "Advanced"]
LEVEL_WEIGHTS = [0.40, 0.40, 0.20]

GENDERS     = ["Male", "Female", "Non-binary", "Prefer not to say"]
GENDER_WEIGHTS = [0.48, 0.46, 0.04, 0.02]

AGE_BINS    = [(18, 24), (25, 34), (35, 44), (45, 54), (55, 65)]
AGE_WEIGHTS = [0.20, 0.35, 0.25, 0.13, 0.07]

PAYMENT_METHODS = ["Credit Card", "Debit Card", "PayPal", "UPI", "Net Banking", "Crypto"]

COMPLETION_STATUS = ["Completed", "In Progress", "Dropped", "Not Started"]
STATUS_WEIGHTS    = [0.45, 0.30, 0.15, 0.10]


def rand_age() -> int:
    bin_ = random.choices(AGE_BINS, weights=AGE_WEIGHTS)[0]
    return random.randint(*bin_)


# ─── Generate Users ───────────────────────────────────────────────────────────
def generate_users(n: int) -> pd.DataFrame:
    records = []
    for i in range(1, n + 1):
        country = random.choices(COUNTRIES, weights=COUNTRY_WEIGHTS)[0]
        join_date = fake.date_between(start_date="-4y", end_date="today")
        records.append({
            "user_id":         f"U{i:05d}",
            "name":            fake.name(),
            "email":           fake.unique.email(),
            "gender":          random.choices(GENDERS, weights=GENDER_WEIGHTS)[0],
            "age":             rand_age(),
            "country":         country,
            "join_date":       join_date,
            "subscription":    random.choices(
                                   ["Free", "Basic", "Premium"],
                                   weights=[0.45, 0.30, 0.25]
                               )[0],
            "is_active":       random.choices([True, False], weights=[0.80, 0.20])[0],
            "referral_source": random.choices(
                                   ["Organic", "Social Media", "Email", "Word of Mouth", "Ad"],
                                   weights=[0.30, 0.25, 0.20, 0.15, 0.10]
                               )[0],
        })
    df = pd.DataFrame(records)
    df.to_csv(f"{OUTPUT_DIR}/users.csv", index=False)
    print(f"✅  Users generated     → {OUTPUT_DIR}/users.csv  ({len(df):,} rows)")
    return df


# ─── Generate Courses ─────────────────────────────────────────────────────────
def generate_courses(n: int) -> pd.DataFrame:
    records = []
    for i in range(1, n + 1):
        category = random.choice(CATEGORIES)
        level    = random.choices(LEVELS, weights=LEVEL_WEIGHTS)[0]
        duration = random.randint(4, 80)          # hours
        base_price = round(random.uniform(9.99, 299.99), 2)
        rating   = round(random.uniform(3.0, 5.0), 1)
        records.append({
            "course_id":         f"C{i:04d}",
            "title":             f"{category}: {fake.bs().title()} ({level})",
            "category":          category,
            "level":             level,
            "instructor":        fake.name(),
            "duration_hours":    duration,
            "price_usd":         base_price,
            "discounted_price":  round(base_price * random.uniform(0.5, 1.0), 2),
            "rating":            rating,
            "num_reviews":       random.randint(10, 8000),
            "language":          random.choices(
                                     ["English", "Hindi", "Spanish", "French", "German"],
                                     weights=[0.60, 0.15, 0.10, 0.08, 0.07]
                                 )[0],
            "certificate":       random.choice([True, False]),
            "launch_date":       fake.date_between(start_date="-5y", end_date="-1m"),
        })
    df = pd.DataFrame(records)
    df.to_csv(f"{OUTPUT_DIR}/courses.csv", index=False)
    print(f"✅  Courses generated    → {OUTPUT_DIR}/courses.csv  ({len(df):,} rows)")
    return df


# ─── Generate Transactions ────────────────────────────────────────────────────
def generate_transactions(users: pd.DataFrame, courses: pd.DataFrame, n: int) -> pd.DataFrame:
    user_ids   = users["user_id"].tolist()
    course_ids = courses["course_id"].tolist()

    course_price_map     = courses.set_index("course_id")["discounted_price"].to_dict()
    course_duration_map  = courses.set_index("course_id")["duration_hours"].to_dict()

    records = []
    for i in range(1, n + 1):
        user_id   = random.choice(user_ids)
        course_id = random.choice(course_ids)
        price     = course_price_map[course_id]
        duration  = course_duration_map[course_id]
        status    = random.choices(COMPLETION_STATUS, weights=STATUS_WEIGHTS)[0]

        completed_hours = 0
        if status == "Completed":
            completed_hours = duration
        elif status == "In Progress":
            completed_hours = round(random.uniform(0.05, 0.95) * duration, 1)
        elif status == "Dropped":
            completed_hours = round(random.uniform(0.01, 0.30) * duration, 1)

        enroll_date  = fake.date_between(start_date="-3y", end_date="today")
        rating_given = None
        if status == "Completed":
            rating_given = round(random.uniform(2.5, 5.0), 1)

        records.append({
            "transaction_id":    f"T{i:07d}",
            "user_id":           user_id,
            "course_id":         course_id,
            "enroll_date":       enroll_date,
            "price_paid_usd":    round(price * random.uniform(0.80, 1.00), 2),
            "payment_method":    random.choice(PAYMENT_METHODS),
            "completion_status": status,
            "completed_hours":   completed_hours,
            "rating_given":      rating_given,
            "device":            random.choices(
                                     ["Desktop", "Mobile", "Tablet"],
                                     weights=[0.50, 0.38, 0.12]
                                 )[0],
            "coupon_used":       random.choices([True, False], weights=[0.35, 0.65])[0],
        })

    df = pd.DataFrame(records)
    df.to_csv(f"{OUTPUT_DIR}/transactions.csv", index=False)
    print(f"✅  Transactions generated → {OUTPUT_DIR}/transactions.csv  ({len(df):,} rows)")
    return df


# ─── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n🚀  EduPro Data Generator\n" + "─" * 40)
    users        = generate_users(N_USERS)
    courses      = generate_courses(N_COURSES)
    transactions = generate_transactions(users, courses, N_TRANSACTIONS)
    print("\n✨  All datasets ready in ./data/")
