# Generated by Django 2.2.6 on 2019-10-22 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grade', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportproblem',
            name='deadline',
            field=models.DateTimeField(null=True),
        ),
    ]
