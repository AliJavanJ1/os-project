from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class AIModel(models.Model):
    model_name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    code_file = models.FileField(upload_to='code_files')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.model_name


class Project(models.Model):
    data_name = models.CharField(max_length=100, blank=False, null=False)
    model = models.ForeignKey(AIModel, on_delete=models.CASCADE)
    data_file = models.FileField(upload_to='data_files')

    class Meta:
        unique_together = ('data_name', 'model')

    def __str__(self):
        return self.data_name


class Run(models.Model):
    class RunType(models.TextChoices):
        TRAIN = 'T', 'Train'
        PREDICT = 'TAP', 'Train and Predict'

    start_time = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    result_timeseries = models.FileField(upload_to='result_timeseries', default='result_timeseries/result_file.csv')
    type = models.CharField(max_length=10, choices=RunType.choices, blank=False, null=False)
    split_ratio = models.FloatField(default=0.8,
                                    blank=False,
                                    null=False,
                                    help_text='ratio of train data to all data witch should be from 0 and 1')

    def __str__(self):
        return f'{self.start_time.strftime("%Y-%m-%d %H:%M:%S")}: {self.get_type_display()} ration: {self.split_ratio}'
