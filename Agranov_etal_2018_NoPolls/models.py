from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

import random

author = 'Lunzheng Li'

doc = """
Let me replicate Agranov et al(2018)'s voting experiment in Otree,
20/04/2021 - Next - figure out "formfields"
21/04/2021 - Next - set winner and determine payoff
22/04/2021 - Next - It seems the logic is working now, work on the display now.
                    Also, need to select one random round to pay the subject.
25/04/2021 - after a careful look at the paper, the payment is all the cumulative
             payoff of all rounds, and one guess is picked to paid in the end.
           - it seems that everything is working, let me double check and add
             other treatments.
           - use bots to test program.
"""


class Constants(BaseConstants):
    name_in_url = 'Agranov_etal_2018_NoPolls'
    players_per_group = 3
    num_rounds = 2

    states = ['Red', 'Blue']
    guesses = ['real_types', 'real_votes']
    # In 10 periods the voting cost = 25
    # In 10 periods the voting cost = 50
    costs = [c(25), c(50)]
    winner_prize = c(200)
    guess_prize = c(1000)

    instructions_template = 'Agranov_etal_2018_NoPolls/Instructions_temp.html'


class Subsession(BaseSubsession):
    def creating_session(self):
        for g in self.get_groups():
            if self.round_number < Constants.num_rounds / 2 + 1:
                g.cost = Constants.costs[0]
            else:
                g.cost = Constants.costs[1]
            print('cost', g.cost)

            g.state = random.choice(Constants.states)
            print('true state:', g.state)
            if g.state == 'red':
                p_red = 2 / 3
            else:
                p_red = 1 / 3
            p_blue = 1 - p_red

            for p in g.get_players():
                p.type = random.choices(Constants.states, weights=[
                    p_red, p_blue], k=1)[0]
                # create the random rounds and guesses type for bonus here
                if self.round_number == 1:
                    p.guess_paid_round = random.randint(
                        1, Constants.num_rounds)
                    p.guess_paid_question = random.choice(Constants.guesses)
                else:
                    p.guess_paid_round = p.in_previous_rounds(
                    )[0].guess_paid_round
                    p.guess_paid_question = p.in_previous_rounds(
                    )[0].guess_paid_question

    pass


class Group(BaseGroup):
    state = models.StringField()
    cost = models.CurrencyField()

    vote_red = models.IntegerField()
    vote_blue = models.IntegerField()
    vote_abstain = models.IntegerField()

    winner = models.StringField()

    def vote_results(self):
        votes = [p.vote for p in self.get_players()]
        types = [p.type for p in self.get_players()]

        type_red = types.count('Red')
        type_blue = types.count('Blue')

        self.vote_red = votes.count('Vote Red')
        self.vote_blue = votes.count('Vote Blue')
        self.vote_abstain = votes.count('Abstain')
        if self.vote_red > self.vote_blue:
            self.winner = 'Red'
        elif self.vote_blue > self.vote_red:
            self.winner = 'Blue'
        else:
            self.winner = random.choice(Constants.states)

        # set payoff
        for p in self.get_players():
            # vote payoff
            if p.type == self.winner:
                p.vote_payoff = Constants.winner_prize
            else:
                p.vote_payoff = c(0)
            # net payoff
            if p.vote != 'Abstain':
                p.payoff = p.vote_payoff - self.cost
            else:
                p.payoff = p.vote_payoff

            # get the bonus payoff coming from guesses
            if self.round_number == p.guess_paid_round:
                if p.guess_paid_question == 'real_types':
                    if p.guess_red == type_red and p.guess_blue == type_blue:
                        p.guess_payoff = Constants.guess_prize
                    else:
                        p.guess_payoff = c(0)
                else:
                    if (p.guess_vote_red == self.vote_red) and (
                            p.guess_vote_blue == self.vote_blue):
                        p.guess_payoff = Constants.guess_prize
                    else:
                        p.guess_payoff = c(0)
                print(p.guess_payoff)

            if self.round_number == Constants.num_rounds:
                p.guess_payoff = p.in_round(p.guess_paid_round).guess_payoff
                # print(p.participant.payoff)
                p.total_payoff = p.participant.payoff + p.guess_payoff

            # print('''{} guess is chosen, the real type - red: {} blue: {},
            #   your guesses are - red: {} blue {}; the real votes - red: {}
            #   blue: {} your guesses are - red: {} blue {}'''.format(
            #     str(p.guess_paid_question), str(type_red), str(type_blue),
            #     str(p.guess_red), str(p.guess_blue), str(self.vote_red),
            #     str(self.vote_blue), str(p.guess_vote_red),
            #     str(p.guess_vote_blue)))
    pass


class Player(BasePlayer):
    type = models.StringField()

    # guesses
    # guess on real types
    guess_red = models.IntegerField(min=0, max=Constants.players_per_group,
                                    label='red')
    guess_blue = models.IntegerField(min=0, max=Constants.players_per_group,
                                     label='blue')

    # guess on actual votes
    guess_vote_red = models.IntegerField(
        min=0, max=Constants.players_per_group, label='red')
    guess_vote_blue = models.IntegerField(
        min=0, max=Constants.players_per_group, label='blue')

    # pick one guess to send a prize
    guess_paid_round = models.IntegerField()
    guess_paid_question = models.StringField()
    guess_payoff = models.CurrencyField()

    # vote
    vote = models.StringField(
        choices=['Vote Red', 'Vote Blue', 'Abstain'],
        widget=widgets.RadioSelect,
        label='What is your ultimate choice?'
    )

    # all level of payoffs
    vote_payoff = models.CurrencyField()
    total_payoff = models.CurrencyField()

    pass
