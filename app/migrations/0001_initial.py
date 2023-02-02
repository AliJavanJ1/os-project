# Generated by Django 4.1.6 on 2023-02-02 14:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AIModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=100, unique=True)),
                ('code_file', models.FileField(upload_to='code_files')),
                ('type', models.CharField(choices=[('T', 'TensorFlow'), ('P', 'PyTorch'), ('S', 'Scikit-learn'), ('O', 'OpenCV')], max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_name', models.CharField(max_length=100)),
                ('data_file', models.FileField(upload_to='data_files')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.aimodel')),
            ],
            options={
                'unique_together': {('data_name', 'model')},
            },
        ),
        migrations.CreateModel(
            name='Run',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('result_timeseries', models.FileField(default='result_timeseries/result_file.csv', upload_to='result_timeseries')),
                ('type', models.CharField(choices=[('T', 'Train'), ('TAP', 'Train and Predict')], max_length=10)),
                ('split_ratio', models.FloatField(default=0.8, help_text='ratio of train data to all data witch should be from 0 and 1')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.project')),
            ],
        ),
    ]