from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import pandas as pd


class Welcome(Page):
    # timeout_seconds = 300

    def is_displayed(self):
        return self.player.round_number == 1
    pass


class Instruction(Page):
    timeout_seconds = 1200

    def is_displayed(self):
        return self.player.round_number == 1
    pass


class Vote(Page):
    form_model = 'player'
    form_fields = ['vote']

    def js_vars(self):
        currentRound = self.round_number
        prev = self.player.in_previous_rounds()
        prev_g = self.group.in_previous_rounds()
        return dict(
            currentRound=currentRound,
            labels_prev=[i.label for i in prev],
            votes_prev=[i.vote for i in prev],
            y_bonuss_prev=[i.y_bonus for i in prev],
            winner_prev=[i.winner for i in prev_g]
        )
    pass


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'vote_results'
    pass


class Results(Page):
    pass


page_sequence = [
    Welcome,
    Instruction,
    Vote,
    ResultsWaitPage,
    Results,
]
