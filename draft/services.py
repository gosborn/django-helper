from secrets import FANTASY_NERD_API_KEY as api_key
import requests
from draft.models import Player


class PlayerPopulator(object):
    BASE_URL = 'https://www.fantasyfootballnerd.com/service/'
    DRAFTABLE_URL = 'draft-rankings/json/{}/1/'
    STATS_URL = 'draft-projections/json/{}/{}/'

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
