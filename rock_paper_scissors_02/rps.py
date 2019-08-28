#!/usr/bin/env python
# Author: Jørgen Bele Reinfjell
# Date: 28.08.2019 [dd.mm.yyyy]
# File: rps.py
# Description:
#   Python code for assignment 2 of Plab2 2019

from random import randint
from enum import Enum
from collections import defaultdict
from functools import total_ordering, reduce

import matplotlib.pyplot as plt


def subsequences(r, v):
    rlen = len(r)
    j = 0
    for i in range(0, len(v)-1):
        if r[j] == v[i]:
            j += 1
            if j == rlen:
                yield i-j+1, i
                j = 0
        else:
            j = 0


def max_val(d):
    keys = list(d.keys())
    return reduce(lambda acc, n: n if d[n] > d[acc] else acc, keys[1:], keys[0])


def rand_action():
    return Action.from_ord(randint(0, 2))


def avg(l):
    return sum(l)/len(l)


@total_ordering
class Action(Enum):
    ROCK = 0
    PAPER = 1
    SCISSOR = 2

    @staticmethod
    def from_ord(ordinal):
        return [Action.ROCK, Action.PAPER, Action.SCISSOR][ordinal]

    def __eq__(self, otr):
        return self.value == otr.value

    def __lt__(self, otr):
        return self + 1 == otr

    def __add__(self, n):
        return Action.from_ord((self.value + n) % 3)


def verify_action():
    r, p, s = list(Action.__members__.values())
    assert(r < p)
    assert(p < s)
    assert(s < r)

    assert(p > r)
    assert(r > s)
    assert(s > p)

    assert(p == p)
    assert(r == r)
    assert(s == s)


class Player:
    def next_action(self):
        pass

    def register_result(self, result):
        pass


class SeqPlayer(Player):
    def __init__(self):
        self.prev = Action.PAPER

    def next_action(self):
        return self.prev + 1

    def register_result(self, result):
        pass

    def __str__(self):
        return f'SeqPlayer'


class RandPlayer(Player):
    def next_action(self):
        return rand_action()

    def register_result(self, result):
        pass

    def __str__(self):
        return f'RandPlayer'


class MostUsedPlayer(Player):
    def __init__(self):
        self._history = [0 for k in Action.__members__.values()]

    def next_action(self):
        a = list(Action.__members__.values())
        action = reduce(lambda acc, n: n if self._history[n.value] > self._history[acc.value] else acc,
                        a[1:], a[0])
        if self._history[action.value] == 0:
            return rand_action()
        return action

    def register_result(self, action):
        # store the winning move, makes next_action() simpler
        self._history[(action+1).value] += 1

    def __str__(self):
        return f'MostUsedPlayer'


class HistoricPlayer(Player):
    def __init__(self, n=1):
        self._history = []
        self.n = n

    def next_action(self):
        a = list(Action.__members__.values())
        recent = self._history[len(self._history)-self.n:]

        def inc_(d, k):
            d[k] += 1
            return d

        s = list(subsequences(recent, self._history))
        move_history = reduce(lambda acc, x: inc_(acc, x),
                              map(lambda x: self._history[x[1]+1],
                                  subsequences(recent, self._history[:-self.n])), defaultdict(int))
        if move_history:
            return Action.from_ord(max_val(move_history))
        return rand_action()

    def register_result(self, action):
        self._history.append((action+1).value)  # stores the winning move

    def __str__(self):
        return f'Historic({self.n})'


class SimpleGame:
    def __init__(self, p1, p2):
        self.players = (p1, p2)
        self.actions = [0, 0]
        self.points = [0, 0]

    def play(self):
        actions = [p.next_action() for p in self.players]
        round_points = [0, 0]
        for i, player in enumerate(self.players):
            j = (i+1) % 2
            player.register_result(actions[j])
            if actions[i] == actions[j]:
                round_points[i] = 0.5
            else:
                round_points[i] = 1 if actions[i] > actions[j] else 0
            self.points[i] += round_points[i]
        self.actions = actions
        return self.actions, round_points, self.points

    def __str__(self):
        return f'actions: {self.actions}, points: {self.points}'


class MultiplePlays:
    def __init__(self, p1, p2, n):
        self.players = (p1, p2)
        self.actions = [0, 0]
        self.points = [0, 0]
        self.simple_game = SimpleGame(self.players[0], self.players[1])
        self.n = n

    def play_simplegame(self):
        action, points, total_points = self.simple_game.play()
        results = [self.players[0], 'nobody', self.players[1]]
        result = results[int(points[0]*0.5 + points[1]*2)]
        return result, action, points, total_points, f'{self.players[0]}: {action[0]}. {self.players[1]}: {action[1]} -> {result.__str__()} wins'

    def play_tournament(self, fig, ax):
        # Total score
        th1, th2 = reduce(lambda acc, x: (acc[0] + [x[0]], acc[1] + [x[1]]),
                          map(lambda x: self.play_simplegame()[3],
                              range(0, self.n)), [[], []])

        # Total average points per round
        # ah1, ah2 = reduce(lambda acc, x: (acc[0] + [avg(acc[0] + [x[0]])], acc[1] + [avg(acc[1] + [x[1]])]),
        #                  map(lambda x: self.play_simplegame()[2], range(0, self.n)),
        #                  [[], []])
        ah1, ah2 = reduce(
            lambda acc, x: [[acc[0][0] + [avg(acc[1][0] + [x[0]])], acc[0][1] + [avg(acc[1][1] + [x[1]])]],
                            [acc[1][0] + [x[0]], acc[1][1] + [x[1]]]],
            map(lambda x: self.play_simplegame()[2], range(0, self.n)),
            [[[], []], [[], []]])[0]

        if not fig:
            fig, axs = plt.subplots(2, 1)
            ax = axs
        ax[0].plot(th1, label=self.players[0])
        ax[0].plot(th2, label=self.players[1])
        ax[0].set_xlabel('round')
        ax[0].set_ylabel('points')
        ax[0].grid(True)
        ax[0].legend()

        ax[1].plot(ah1, label=self.players[0])
        ax[1].plot(ah2, label=self.players[1])
        ax[1].set_xlabel('round')
        ax[1].set_ylabel('avg points per round')
        ax[1].grid(True)
        ax[1].legend()

        fig.tight_layout()
        # plt.show()


TOURNAMENTS = [
    (MostUsedPlayer(), MostUsedPlayer(),       1000),
    (MostUsedPlayer(), MostUsedPlayer(),       1000),
    (MostUsedPlayer(), MostUsedPlayer(),       1000),

    (MostUsedPlayer(), HistoricPlayer(n=4),    1000),
    (MostUsedPlayer(), HistoricPlayer(n=20),   1000),

    (HistoricPlayer(n=2), HistoricPlayer(n=2), 1000),
    (HistoricPlayer(n=4), HistoricPlayer(n=2), 1000),

    (SeqPlayer(),      RandPlayer(), 1000),
    (HistoricPlayer(), RandPlayer(), 1000),
    (HistoricPlayer(), SeqPlayer(), 1000),
]

CHUNK_SIZE = 3
for c in range(0, len(TOURNAMENTS), CHUNK_SIZE):
    fig, axs = plt.subplots(CHUNK_SIZE, 2)
    for i, (p1, p2, n) in enumerate(TOURNAMENTS[c:c+CHUNK_SIZE]):
        mp = MultiplePlays(p1, p2, n)
        mp.play_tournament(fig, axs[i])
plt.show()
