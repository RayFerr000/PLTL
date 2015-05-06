# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Class', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Enrolled_Class',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(default=b'DEFAULT VALUE', max_length=20)),
                ('status', models.CharField(default=b'DEFAULT VALUE', max_length=50)),
                ('class_id', models.ForeignKey(to='Class.Class', to_field=b'class_id')),
                ('email', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('peer_leader', models.ForeignKey(related_name='peer_leader', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('students_led', models.ManyToManyField(related_name='students_led', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
