from django.db import models
from django.contrib.auth.models import User


class History(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    course = models.CharField(max_length=50)
    study_hours = models.FloatField()
    sleep_hours = models.FloatField()
    attendance_percentage = models.FloatField()
    screen_time = models.FloatField()

    prediction = models.FloatField()
    grade = models.CharField(max_length=5)
    pass_or_fail = models.CharField(max_length=50)
    risk = models.CharField(max_length=50)
    risk_class = models.CharField(max_length=50)

    zai_output = models.JSONField()

    def __str__(self):
        return (f'{self.user.username} - {self.prediction} - {self.pass_or_fail}')
