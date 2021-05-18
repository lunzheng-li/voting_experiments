from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Instruction(Page):
    timeout_seconds = 1200

    def is_displayed(self):
        return self.player.round_number == 1
    pass


class Type(Page):
    pass


class Poll(Page):
    form_model = 'player'
    form_fields = ['poll']
    pass


class Poll_WaitPage(WaitPage):
    after_all_players_arrive = 'poll_results'


class Poll_results(Page):
    pass


class Guess(Page):
    form_model = 'player'
    form_fields = ['guess_red', 'guess_blue',
                   'guess_vote_red', 'guess_vote_blue']

    def error_message(self, values):
        print('values is', values)
        if values['guess_red'] + values['guess_blue'] != (
                Constants.players_per_group):
            return 'The numbers must add up to ' + str(
                Constants.players_per_group)
        elif values['guess_vote_red'] + values['guess_vote_blue'] > (
                Constants.players_per_group):
            return 'The sum of the numbers must small than ' + str(
                Constants.players_per_group)
    pass


class Vote(Page):
    form_model = 'player'
    form_fields = ['vote']
    pass


class Results_WaitPage(WaitPage):
    after_all_players_arrive = 'vote_results'


class Results(Page):
    def vars_for_template(self):
        player = self.player
        if player.guess_payoff == c(0):
            a = 'Wrong'
        else:
            a = 'Right'
        return dict(
            a=a,
        )
    pass


page_sequence = [
    Instruction,
    Poll,
    Poll_WaitPage,
    Poll_results,
    Guess,
    Vote,
    Results_WaitPage,
    Results,
]
