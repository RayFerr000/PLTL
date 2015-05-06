# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djangoyearlessdate.models


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('class_id', models.CharField(default=b'DEFAULT VALUE', unique=True, max_length=20, db_index=True)),
                ('semester', models.CharField(default=b'DEFAULT VALUE', max_length=20)),
                ('year', djangoyearlessdate.models.YearField()),
                ('class_description', models.CharField(default=b'Enter 500 characters at max', max_length=500, blank=True)),
                ('course_id', models.ForeignKey(to='Course.Course', to_field=b'course_id')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
