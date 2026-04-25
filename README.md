# Project Name

ACE MIND AI

## 🧠 Description

Ace Mind AI is an intelligent, AI-native academic orchestrator designed to transform how students manage their educational journey. Moving beyond simple static calendars, Ace Mind AI utilizes a Generative Language Model (GLM) to act as a personal academic strategist.

The technical scope involves a multi-step agentic workflow that processes student behavioral data to autonomously generate optimized study schedules and provide predictive grade analytics. Our design decision focuses on proactive intervention—shifting the student's role from a manual planner to an informed curator of their own academic success.

## ⚙️ Tech Stack

- Django (Backend framework)
- Python (Core logic)
- NumPy / Pandas (Data processing)
- Scikit-learn (Machine Learning)
- Jazzmin (Admin UI theme)
- Tailwind CSS
- CSS
- HTML
- Java Script

# 📦 Installation

git clone https://github.com/Ivanyong07/ACE-MIND-AI.git
cd ACE-MIND-AI
pip install -r requirements.txt

# 🔑 Genrate A Secret Key

python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 🤖 ML Model Setup

Before running the server, train the model:
cd project/ml
python train.py

## 📊 Dataset

This project uses a publicly available dataset from Kaggle:

- Source: https://www.kaggle.com/datasets/borovai0/student-performance-analytics-dataset

The dataset is used for training the machine learning model for academic performance prediction.
After downloaded drag the dataset to the folder (example: project/ml/student_performance)

⚠️ Note: The dataset is not included in this repository due to size and licensing. Please download it from the link above.

## 🧠 Model Training

The machine learning model is trained using a Kaggle dataset.

To train the model:
cd project/ml
python train.py

## Run server

python manage.py runserver

# To create superuser

python manage.py createsuperuser

# Features

Django backend system
ML-powered academic prediction
Intelligent study schedule generation
Admin dashboard (Jazzmin UI)
Data-driven student analytics

my-project/
│── manage.py
│── requirements.txt
│── README.md
│── project/
│ ├── ml/
│ ├── settings.py
│── app/
