import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import os
import joblib
import random

data = pd.read_csv("https://link-to-dataset.csv")
df = pd.DataFrame(data)

# Drop the useless data
data = df.drop(
    columns=['student_id', 'class_participation'])
# print(data.describe())

# Add noise for more accurate
noise = np.random.normal(0, 0.5, size=len(data))
data['daily_study_hours'] = data['weekly_self_study_hours'] / 7
data['screen_time'] = (8 - data['daily_study_hours']).clip(1, 8)
data['sleep_hours'] = (
    6 + (data['attendance_percentage'] / 50) -
    (data['screen_time'] / 5) + noise
).clip(1, 9)
data['study_attendance'] = data['daily_study_hours'] * \
    data['attendance_percentage']

# Train
X = data[['daily_study_hours', 'sleep_hours',
          'attendance_percentage', 'screen_time', 'study_attendance']]
y = data['total_score']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)  # read 10000 data


re_score = model.score(X_test, y_test)  # the final grade R square
y_pred = model.predict(X_test)
print(
    "Coefficients [daily_study_hours, sleep_hours, attendance_percentage]:")
print(model.feature_importances_)
print(f"Feature importance:: {re_score:.4f}")

result = pd.DataFrame({
    'Actual': y_test,
    'Predicted': y_pred
})

# sample_data = result.sample(50)
# plt.figure(figsize=(9, 7))

# plt.scatter(sample_data['Actual'], sample_data['Predicted'],
#             color='blue', s=80, alpha=0.6, edgecolor='white', label='Student Data (Sample)')

# plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()],
#          'r--', lw=2, label='Perfect Prediction')

# plt.grid(True, linestyle='-', alpha=0.7)

# plt.title(f"Visualizing 50 Random Students\nModel Accuracy: {re_score:.2f}")
# plt.xlabel("Actual Score")
# plt.ylabel("Predicted Score")
# plt.legend()
# plt.show()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 'model' is your trained Ridge model, 'scaler' is your StandardScaler
joblib.dump(model, os.path.join(BASE_DIR, 'student_model.pkl'))

print("Success!!")
