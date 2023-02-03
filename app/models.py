from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class AIModel(models.Model):
    class ModelType(models.TextChoices):
        TENSORFLOW = 'T', 'TensorFlow'
        PYTORCH = 'P', 'PyTorch'
        SCIKIT = 'S', 'Scikit-learn'
        OPENCV = 'O', 'OpenCV'
    model_name = models.CharField(max_length=100, blank=False, null=False)
    code_file = models.FileField(upload_to='code_files')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=ModelType.choices, blank=False, null=False)

    class Meta:
        unique_together = ('model_name', 'user')

    def __str__(self):
        return self.model_name + '_' + self.user.__str__


class Project(models.Model):
    data_name = models.CharField(max_length=100, blank=False, null=False)
    model = models.ForeignKey(AIModel, on_delete=models.CASCADE)
    data_file = models.FileField(upload_to='data_files')
    target_data_file = models.FileField(upload_to='data_files')

    class Meta:
        unique_together = ('data_name', 'model')

    def __str__(self):
        return self.data_name + '_' + self.model.__str__ 


class Run(models.Model):
    class RunType(models.TextChoices):
        TRAIN = 'T', 'Train'
        PREDICT = 'TAP', 'Train and Predict'

    start_time = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    iostat_cpu_data = models.FileField(upload_to='result_timeseries', default='result_timeseries/temp.csv')
    iostat_disk_data = models.FileField(upload_to='result_timeseries', default='result_timeseries/temp.csv')
    iostat_cpu_chart = models.FileField(upload_to='result_timeseries', default='result_timeseries/temp.jpeg')
    iostat_disk_chart = models.FileField(upload_to='result_timeseries', default='result_timeseries/temp.jpeg')
    blktrace_data = models.FileField(upload_to='result_timeseries', default='result_timeseries/temp.csv')
    blktrace_chart = models.FileField(upload_to='result_timeseries', default='result_timeseries/temp.jpeg')
    is_running = models.BooleanField(default=False)
    type = models.CharField(max_length=10, choices=RunType.choices, blank=False, null=False)
    split_ratio = models.FloatField(default=0.8,
                                    blank=False,
                                    null=False,
                                    help_text='ratio of train data to all data witch should be from 0 and 1')

    def __str__(self):
        return f'{self.start_time.strftime("%Y-%m-%d %H:%M:%S")}: {self.get_type_display()} ration: {self.split_ratio}'

    def save(self, *args, **kwargs):
        directory = 'result_timeseries/' + self.project.__str__ + '/'
        self.iostat_cpu_data= directory + 'iostat_cpu_data.csv'
        self.iostat_disk_data = directory + 'iostat_disk_data.csv'
        self.iostat_cpu_chart = directory + 'iostat_cpu_chart.jpeg'
        self.iostat_disk_chart = directory + 'iostat_disk_chart.jpeg'
        self.blktrace_data = directory + 'blktrace_data.csv'
        self.blktrace_chart = directory + 'blktrace_chart.jpeg'
        super(Run, self).save(*args, **kwargs)
