# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-23 01:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('draft', '0002_auto_20170823_0148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='completions',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='def_tds',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='fumble_recoveries',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='fumbles',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='interceptions',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='nerd_estimated_points',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='passing_attempts',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='passing_tds',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='passing_yards',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='receiving_tds',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='receiving_yards',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='receptions',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='rush_attempts',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='rush_tds',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='rush_yards',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='sacks',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='special_team_tds',
            field=models.IntegerField(null=True),
        ),
    ]
