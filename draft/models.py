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
    nerd_position_rank = models.IntegerField()
    nerd_overall_rank = models.IntegerField()
    nerd_id = models.IntegerField()

    nerd_estimated_points = models.IntegerField(null=True)

    #QB specific fields
    completions = models.IntegerField(null=True)
    pass_attempts = models.IntegerField(null=True)
    pass_yards = models.IntegerField(null=True)
    pass_tds = models.IntegerField(null=True)
    pass_interceptions = models.IntegerField(null=True)


    # non-def fields
    rush_attempts = models.IntegerField(null=True)
    rush_yards = models.IntegerField(null=True)
    rush_tds = models.IntegerField(null=True)
    fumbles = models.IntegerField(null=True)
    receptions = models.IntegerField(null=True)
    receiving_yards = models.IntegerField(null=True)
    receiving_tds = models.IntegerField(null=True)

    # def fields
    sacks = models.IntegerField(null=True)
    interceptions = models.IntegerField(null=True)
    fumble_recoveries = models.IntegerField(null=True)
    def_tds = models.IntegerField(null=True)
    special_team_tds = models.IntegerField(null=True)

    def __unicode__(self):
        return u'{} {}'.format(self.first_name, self.last_name)


class DraftPick(models.Model):
    player = models.ForeignKey(Player)
    draft = models.ForeignKey(Draft)
    team = models.ForeignKey(Team)
    position = models.IntegerField()
