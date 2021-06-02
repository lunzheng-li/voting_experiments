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
Let me replicate Levine and Palfrey (2007)'s voting experiment in Otree,

29 - May: for all round_number>=2, I want a table to prresent the history. Since
for the length of the tables are different in different rounds, Javascript is 
needed. Let me spend some time on JS (or maybe I can figure a way that do not 
need JS)

31 - May: it seems that I made the "JS creating table" work, let me make things
look nicer. 

01 - June: next - make the instruction more readable and add practice rounds and
the second session.
"""


class Constants(BaseConstants):
    name_in_url = 'Levine_Palfrey_2007'
    players_per_group = 3
    num_rounds = 6
    end_s1_round = num_rounds // 2
    start_s2_round = end_s1_round + 1

    N_A = 1
    N_B = players_per_group - N_A
    labels = ['ALPHA'] * N_A + ['BETA'] * N_B

    # Here we set the N_A and N_B for session 2
    N_A_s2 = 2
    N_B_s2 = players_per_group - N_A_s2
    labels_s2 = ['ALPHA'] * N_A_s2 + ['BETA'] * N_B_s2

    H_payoff = 105
    L_payoff = 5

    c_max = 55

    instructions_template = 'Levine_Palfrey_2007/Instructions_temp.html'
    pass


class Subsession(BaseSubsession):
    def creating_session(self):
        # To avoid modification in the Constants class, make copy of it.
        labels_shuffled = Constants.labels.copy()
        labels_s2_shuffled = Constants.labels_s2.copy()
        # print(labels_shuffled)

        for g in self.get_groups():
            random.shuffle(labels_shuffled)
            random.shuffle(labels_s2_shuffled)
            for p in g.get_players():
                if self.round_number < Constants.start_s2_round:
                    p.label = labels_shuffled[0]
                    del labels_shuffled[0]
                else:
                    p.label = labels_s2_shuffled[0]
                    del labels_s2_shuffled[0]

                # # get y_bonus from a uniform distribution, the following can
                # # give us floating cost
                # p.y_bonus = round(np.random.uniform(0, 55), 1)
                # However, may be in the experiment, only integers is better
                # see Page 147, in the protocol section -'in integer increments'
                p.y_bonus = random.randint(0, Constants.c_max)

    pass


class Group(BaseGroup):
    vote_x_A = models.IntegerField()  # the num of X votes in group A
    vote_y_A = models.IntegerField()
    vote_x_B = models.IntegerField()
    vote_y_B = models.IntegerField()

    winner = models.StringField()

    def vote_results(self):
        # as we have duplicate keys, I made a list of tuples rather than dict
        label_vote_tups = [(p.label, p.vote) for p in self.get_players()]
        vote_A_lst = []
        vote_B_lst = []
        for tup in label_vote_tups:
            if tup[0] == 'ALPHA':
                vote_A_lst.append(tup[1])
                self.vote_x_A = vote_A_lst.count('X')
                self.vote_y_A = vote_A_lst.count('Y')
            else:
                vote_B_lst.append(tup[1])
                self.vote_x_B = vote_B_lst.count('X')
                self.vote_y_B = vote_B_lst.count('Y')

        if self.vote_x_A > self.vote_x_B:
            self.winner = 'ALPHA'
        elif self.vote_x_A < self.vote_x_B:
            self.winner = 'BETA'
        elif self.vote_x_A == self.vote_x_B:
            self.winner = 'Draw'

        # set payoff
        for p in self.get_players():
            # voting cost
            if p.vote == 'Y':
                real_bonus = p.y_bonus
            else:
                real_bonus = 0

            # vote payoff
            if self.winner == 'Draw':
                p.payoff = (Constants.H_payoff +
                            Constants.L_payoff) / 2 + real_bonus
            else:
                if p.label == self.winner:
                    p.payoff = Constants.H_payoff + real_bonus
                else:
                    p.payoff = Constants.L_payoff + real_bonus

            # # display history for voters
            # print([i.y_bonus for i in p.in_previous_rounds()])
    pass


class Player(BasePlayer):
    # I used 'type' to name the variable, but 'type' is a command of Python,
    # so I change it to 'label'.
    label = models.StringField()
    # vote
    vote = models.StringField(
        choices=['X', 'Y'],
        widget=widgets.RadioSelect,
        label='What is your choice?'
    )
    # cost - in this experiment, the cost is defined as an opportunity cost of
    # choosing X (to vote)
    y_bonus = models.IntegerField()
    pass
