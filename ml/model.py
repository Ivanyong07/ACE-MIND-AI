import joblib
import os
import pandas as pd

# Load the "Brain" that train.py built earlier
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE_DIR, 'student_model.pkl'))


def prediction(daily_study_hours, sleep_hours, attendance_percentage, screen_time):

    study_attendance = daily_study_hours * attendance_percentage
    new_data = [[daily_study_hours, sleep_hours,
                 attendance_percentage, screen_time, study_attendance]]
    pre = pd.DataFrame(new_data, columns=[
        "daily_study_hours",
        "sleep_hours",
        "attendance_percentage",
        "screen_time",
        "study_attendance"])

    result = model.predict(pre).item()  # convert numpy into standard number

    if sleep_hours < 5.0:
        result -= 10

    if attendance_percentage < 50.0:
        result -= 5

    result = max(0, min(100, result))  # set range

    # round up and set result as 2 decimal point and maintain float point
    return round(float(result), 2)


# Test
# print(prediction(3, 5, 70))
# print(prediction(1, 1, 45))
# print(prediction(4, 4, 50, 4))
