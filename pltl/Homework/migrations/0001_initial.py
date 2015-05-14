# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Homework.models


class Migration(migrations.Migration):

    dependencies = [
        ('Assignment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('homework_id', models.AutoField(serialize=False, primary_key=True)),
                ('homework_soln', models.FileField(upload_to=Homework.models.get_upload_file_name)),
                ('submitted_by', models.EmailField(max_length=20)),
                ('submitted_timestamp', models.DateTimeField(auto_now_add=True)),
                ('grade', models.CharField(max_length=3, null=True, blank=True)),
                ('feedback', models.CharField(max_length=300, null=True, blank=True)),
                ('graded_by', models.CharField(max_length=50, null=True, blank=True)),
                ('assignment_id', models.ForeignKey(to='Assignment.Assignment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
