# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Draft(models.Model):
    name = models.CharField(max_length=256)


class Team(models.Model):
    draft = models.ForeignKey(Draft)
    name = models.CharField(max_length=256)


class Positions(object):
    QUARTERBACK = 'QB'
    WIDE_RECEIVER = 'WR'
    RUNNING_BACK = 'RB'
    TIGHT_END = 'TE'
    DEFENSE = 'DEF'

    OPTIONS = (
        (QUARTERBACK, 'QB'),
        (WIDE_RECEIVER, 'WR'),
        (RUNNING_BACK, 'RB'),
        (TIGHT_END, 'TE'),
        (DEFENSE, 'DEF')
    )


class Player(models.Model):
    position = models.CharField(max_length=8, choices=Positions.OPTIONS)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    nfl_team = models.CharField(max_length=8)  # this should be a model
    bye_week = models.IntegerField()
    standard_dev = models.FloatField()
    nerd_rank = models.FloatField()
    nerd_position_rank = models.FloatField()
    nerd_overall_rank = models.FloatField()
    nerd_id = models.IntegerField()

    nerd_estimated_points = models.IntegerField()

    #QB specific fields
    completions = models.IntegerField()
    passing_attempts = models.IntegerField()
    passing_yards = models.IntegerField()
    passing_tds = models.IntegerField()

    # non-def fields
    rush_attempts = models.IntegerField()
    rush_yards = models.IntegerField()
    rush_tds = models.IntegerField()
    fumbles = models.IntegerField()
    receptions = models.IntegerField()
    receiving_yards = models.IntegerField()
    receiving_tds = models.IntegerField()

    # def fields
    sacks = models.IntegerField()
    interceptions = models.IntegerField()
    fumble_recoveries = models.IntegerField()
    def_tds = models.IntegerField()
    special_team_tds = models.IntegerField()


class DraftPick(models.Model):
    player = models.ForeignKey(Player)
    draft = models.ForeignKey(Draft)
    team = models.ForeignKey(Team)
    position = models.IntegerField()
