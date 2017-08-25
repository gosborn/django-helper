# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Scoring(models.Model):
    label = models.CharField(max_length=256)
    passing_yard = models.FloatField(null=True)
    pass_td = models.FloatField(null=True)
    interception = models.FloatField(null=True)
    rushing_yard = models.FloatField(null=True)
    rush_td = models.FloatField(null=True)
    reception = models.FloatField(null=True)
    receiving_yard = models.FloatField(null=True)
    receiving_td = models.FloatField(null=True)
    fumble = models.FloatField(null=True)

    def_sack = models.FloatField(null=True)
    def_interception = models.FloatField(null=True)
    def_fumble_recovery = models.FloatField(null=True)
    def_td = models.FloatField(null=True)
    special_team_td = models.FloatField(null=True)


class Draft(models.Model):
    name = models.CharField(max_length=256)
    scoring = models.ForeignKey(Scoring, null=True)


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
    team = models.ForeignKey(Team, null=True)
    estimated_points = models.FloatField(null=True)

    def __unicode__(self):
        return u'{} {}: {}'.format(self.player.first_name, self.player.last_name, self.estimated_points)
