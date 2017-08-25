from secrets import FANTASY_NERD_API_KEY as api_key
import requests
from draft.models import Player, DraftPick


class PlayerPopulator(object):
    BASE_URL = 'https://www.fantasyfootballnerd.com/service/'
    DRAFTABLE_URL = 'draft-rankings/json/{}/1/'
    STATS_URL = 'draft-projections/json/{}/{}/'

    def populate_player_db(self):
        self.populate_draftable_players()
        self.populate_quarterback_stats()
        self.populate_running_back_stats()
        self.populate_wide_receiver_stats()
        self.populate_tight_end_stats()
        self.populate_def_stats()

    def get_draftable_players(self):
        response = requests.get(self.BASE_URL + self.DRAFTABLE_URL.format(api_key))
        return response.json()

    def populate_draftable_players(self):
        players_json = self.get_draftable_players()['DraftRankings']

        for player in players_json:
            Player.objects.create(
                position=player.get('position'),
                first_name=player.get('fname'),
                last_name=player.get('lname'),
                nfl_team=player.get('team'),
                bye_week=int(player.get('byeWeek')),
                standard_dev=float(player.get('standDev')),
                nerd_rank=float(player.get('nerdRank')),
                nerd_position_rank=int(player.get('positionRank')),
                nerd_overall_rank=int(player.get('overallRank')),
                nerd_id=int(player.get('playerId'))
            )

    def get_quarterback_stats(self):
        response = requests.get(self.BASE_URL + self.STATS_URL.format(api_key, 'QB'))
        return response.json()

    def populate_quarterback_stats(self):
        qb_json = self.get_quarterback_stats()['DraftProjections']

        for qb_data in qb_json:
            player = Player.objects.filter(nerd_id=qb_data.get('playerId')).first()
            if player:
                player.completions = qb_data.get('completions')
                player.pass_attempts = qb_data.get('attempts')
                player.pass_yards = qb_data.get('passingYards')
                player.pass_tds = qb_data.get('passingTD')
                player.pass_interceptions = qb_data.get('passingInt')

                self.hydrate_common_stats(player, qb_data)
                self.hydrate_common_player_stats(player, qb_data)
                player.save()

    def hydrate_common_stats(self, player, data):
        player.nerd_estimated_points = data.get('fantasyPoints')

    def hydrate_common_player_stats(self, player, data):
        player.rush_yards = data.get('rushYards')
        player.rush_attempts = data.get('rushAtt')
        player.rush_tds = data.get('rushTD')
        player.fumbles = data.get('fumbles')

    def get_running_back_stats(self):
        response = requests.get(self.BASE_URL + self.STATS_URL.format(api_key, 'RB'))
        return response.json()

    def populate_running_back_stats(self):
        rb_json = self.get_running_back_stats()['DraftProjections']

        for data in rb_json:
            player = Player.objects.filter(nerd_id=data.get('playerId')).first()
            if player:
                self.hydrate_common_stats(player, data)
                self.hydrate_common_player_stats(player, data)
                self.hydrate_common_receiving_stats(player, data)
                player.save()

    def hydrate_common_receiving_stats(self, player, data):
        player.receptions = data.get('rec')
        player.receiving_yards = data.get('recYards')
        player.receiving_tds = data.get('recTD')

    def get_wide_receiver_stats(self):
        response = requests.get(self.BASE_URL + self.STATS_URL.format(api_key, 'WR'))
        return response.json()

    def populate_wide_receiver_stats(self):
        wr_json = self.get_wide_receiver_stats()['DraftProjections']

        for data in wr_json:
            player = Player.objects.filter(nerd_id=data.get('playerId')).first()
            if player:
                self.hydrate_common_stats(player, data)
                self.hydrate_common_player_stats(player, data)
                self.hydrate_common_receiving_stats(player, data)
                player.save()

    def get_tight_end_stats(self):
        response = requests.get(self.BASE_URL + self.STATS_URL.format(api_key, 'TE'))
        return response.json()

    def populate_tight_end_stats(self):
        te_json = self.get_tight_end_stats()['DraftProjections']

        for data in te_json:
            player = Player.objects.filter(nerd_id=data.get('playerId')).first()
            if player:
                self.hydrate_common_stats(player, data)
                self.hydrate_common_player_stats(player, data)
                self.hydrate_common_receiving_stats(player, data)
                player.save()

    def get_def_stats(self):
        response = requests.get(self.BASE_URL + self.STATS_URL.format(api_key, 'DEF'))
        return response.json()

    def populate_def_stats(self):
        def_json = self.get_def_stats()['DraftProjections']

        for data in def_json:
            player = Player.objects.filter(nerd_id=data.get('playerId')).first()
            if player:
                self.hydrate_common_stats(player, data)
                player.sacks = data.get('sacks')
                player.interceptions = data.get('interceptions')
                player.def_tds = data.get('TD')
                player.fumble_recoveries = data.get('fumbleRec')
                player.special_teams_tds = data.get('specialTeamTD')
                player.save()


class CustomProjectionCalculator(object):

    def __init__(self, draft):
        self.draft = draft
        self.scoring = draft.scoring

    def calculate_all_stats(self):
        s = self.scoring
        for p in Player.objects.all():

            points = 0
            if p.pass_yards:
                points += (s.passing_yard * p.pass_yards)
            if p.pass_tds:
                points += (s.pass_td * p.pass_tds)
            if p.pass_interceptions:
                points += (s.interception * p.pass_interceptions)
            if p.rush_yards:
                points += (s.rushing_yard * p.rush_yards)
            if p.rush_tds:
                points += (s.rush_td * p.rush_tds)
            if p.receptions:
                points += (s.reception * p.receptions)
            if p.receiving_yards:
                points += (s.receiving_yard * p.receiving_yards)
            if p.receiving_tds:
                points += (s.receiving_td * p.receiving_tds)
            if p.fumbles:
                points += (s.fumble * p.fumbles)

            if p.sacks:
                points += (s.def_sack * p.sacks)
            if p.interceptions:
                points += (s.def_interception * p.interceptions)
            if p.fumble_recoveries:
                points += (s.def_fumble_recovery * p.fumble_recoveries)
            if p.def_tds:
                points += (s.def_td * p.def_tds)
            if p.special_team_tds:
                points += (s.special_team_td * p.special_team_tds)

            print(p)
            print(points)

            DraftPick.objects.create(
                player=p,
                draft=self.draft,
                estimated_points=points
            )


class AnalysisTools(object):

    def print_rankings(self):
        position = 1
        for dp in DraftPick.objects.filter(player__position__in=['RB', 'WR', 'TE']).order_by('-estimated_points')[:150]:
            print('{} vs nerd {} ({})// {} // {} {} // {} vs nerd: {} // diff: {}'.format(position,
                                                                                          dp.player.nerd_overall_rank, (
                                                                                          position - dp.player.nerd_overall_rank),
                                                                                          dp.player.position,
                                                                                          dp.player.first_name,
                                                                                          dp.player.last_name,
                                                                                          dp.estimated_points,
                                                                                          dp.player.nerd_estimated_points,
                                                                                          (
                                                                                          dp.estimated_points - dp.player.nerd_estimated_points)))
            position = position + 1