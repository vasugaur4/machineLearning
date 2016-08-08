import os
import sys
from abc import ABCMeta, abstractmethod

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class AddFootballDataInterface:
    """
    Adds/Updates football related tables in db.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def add_football_leagues():
        """Subclasses must implement this as a @staticmethod"""
        pass

    @abstractmethod
    def todays_fixtures():
        """Subclasses must implement this as a @staticmethod"""
        pass

    @abstractmethod
    def add_upcoming_fixtures(date):
        """Subclasses must implement this as a @staticmethod"""
        pass

    @abstractmethod
    def match_commentary(match_id,events):
        """Subclasses must implement this as a @staticmethod"""
        pass

    @abstractmethod
    def add_league_standings(league_id):
        """Subclasses must implement this as a @staticmethod"""
        pass

    @abstractmethod
    def upcoming_fixtures(date = None):
        """Subclasses must implement this as a @staticmethod"""
        pass

    @abstractmethod
    def add_team_squads(team_id):
        """Subclasses must implement this as a @staticmethod"""
        pass

    @abstractmethod
    def update_player_stats(player_id):
        """Subclasses must implement this as a @staticmethod"""
        pass


class GetFootballDataInterface:
    """
    Returns football related data from db.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_leagues():
        """Subclasses must implement this as a @staticmethod"""
        pass

    @abstractmethod
    def get_league_teams(league_id):
        """Subclasses must implement this as a @staticmethod"""
        pass

    @abstractmethod
    def get_team_squad(team_id):
        """Subclasses must implement this as a @staticmethod"""
        pass

    @abstractmethod
    def get_team_squads(team_1, team_2):
        """Subclasses must implement this as a @staticmethod"""
        pass

    # @abstractmethod
    # def get_team_players(team_id):
    #     """Subclasses must implement this as a @staticmethod"""
    #     pass


    @abstractmethod
    def get_player_stats(player_name):
        """Subclasses must implement this as a @staticmethod"""
        pass

    @abstractmethod
    def get_fixtures_new(date, league_id):
        """Subclasses must implement this as a @staticmethod"""
        pass

    @abstractmethod
    def get_league_specific_fixtures(league_id,fixture_type=None):
        """Subclasses must implement this as a @staticmethod"""
        pass

    @abstractmethod
    def get_team_upcoming_fixtures(team_id):
        """Subclasses must implement this as a @staticmethod"""
        pass

    @abstractmethod
    def get_team_completed_fixtures(team_id):
        """Subclasses must implement this as a @staticmethod"""
        pass

    @abstractmethod
    def get_match_scores(match_id):
        """Subclasses must implement this as a @staticmethod"""
        pass

    @abstractmethod
    def get_todays_fixtures():
        """Subclasses must implement this as a @staticmethod"""
        pass

    @abstractmethod
    def get_league_standings(league_id):
        """Subclasses must implement this as a @staticmethod"""
        pass

    @abstractmethod
    def get_team_form(team_1, team_2, league_id):
        """Subclasses must implement this as a @staticmethod"""
        pass

    @abstractmethod
    def get_match_stats(match_id):
        """Subclasses must implement this as a @staticmethod"""
        pass

    @abstractmethod
    def get_match_teams(match_id):
        """Subclasses must implement this as a @staticmethod"""
        pass

    @abstractmethod
    def get_match_squads(match_id):
        """Subclasses must implement this as a @staticmethod"""
        pass

    @abstractmethod
    def get_player_match_stats(match_id):
        """Subclasses must implement this as a @staticmethod"""
        pass

    @abstractmethod
    def get_match_substitutions(match_id):
        """Subclasses must implement this as a @staticmethod"""
        pass

    @abstractmethod
    def get_match_subs(match_id):
        """Subclasses must implement this as a @staticmethod"""
        pass

    @abstractmethod
    def get_match_summary(match_id):
        """Subclasses must implement this as a @staticmethod"""
        pass

    @abstractmethod
    def get_match_timeline(match_id):
        """Subclasses must implement this as a @staticmethod"""
        pass

    @abstractmethod
    def get_upcoming_fixtures(max_limit=None):
        """Subclasses must implement this as a @staticmethod"""
        pass

    @abstractmethod
    def get_completed_fixtures():
        """Subclasses must implement this as a @staticmethod"""
        pass

    @abstractmethod
    def get_commentary(match_id,comment_id=None,direction=None):
        """Subclasses must implement this as a @staticmethod"""
        pass

    @abstractmethod
    def get_squads(soup, team, league_id, team_id):
        """Subclasses must implement this as a @staticmethod"""
        pass

    @abstractmethod
    def get_player_stats(player_id):
        """Subclasses must implement this as a @staticmethod"""
        pass


class BaseFlagImageHandler:
    """
    Returns flag image(s) of team(s).
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def flag_single(team):
        """Subclasses must implement this as a @staticmethod"""
        pass

    @abstractmethod
    def flag_double(team_1, team_2):
        """Subclasses must implement this as a @staticmethod"""
        pass


class BaseStadiumHandler:
    """
    Returns stadium for team(s).
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def stadium(team_name):
        """Subclasses must implement this as a @staticmethod"""
        pass
