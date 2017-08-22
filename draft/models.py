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


class DraftPick(models.Model):
    player = models.ForeignKey(Player)
    draft = models.ForeignKey(Draft)
    team = models.ForeignKey(Team)
    position = models.IntegerField()
