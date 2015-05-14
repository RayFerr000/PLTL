# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Assignment.models


class Migration(migrations.Migration):

    dependencies = [
        ('Class', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('assignment_id', models.AutoField(serialize=False, primary_key=True)),
                ('assignment_name', models.CharField(default=b'DEFAULT VALUE', max_length=50)),
                ('pub_date', models.DateField(verbose_name=b'Date Published')),
                ('due_date', models.DateField(verbose_name=b'Due Date')),
                ('total_grade', models.IntegerField(default=0)),
                ('assignmentfile', models.FileField(null=True, upload_to=Assignment.models.get_upload_file_name, blank=True)),
                ('class_id', models.ForeignKey(to='Class.Class', to_field=b'class_id')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
