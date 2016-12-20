#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Advent of Code, Day 11
======================

Author: hbldh <henrik.blidh@nedomkull.com>

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import re
import time
from collections import namedtuple
from itertools import combinations
try:
    from queue import PriorityQueue
    _range = range
except ImportError:
    from Queue import PriorityQueue
    _range = xrange

state_tuple = namedtuple('state', ['d', 'e', 'F1', 'F2', 'F3', 'F4'])


data_1 = """
The first floor contains a thulium generator, a thulium-compatible microchip, a plutonium generator, and a strontium generator.
The second floor contains a plutonium-compatible microchip and a strontium-compatible microchip.
The third floor contains a promethium generator, a promethium-compatible microchip, a ruthenium generator, and a ruthenium-compatible microchip.
The fourth floor contains nothing relevant.
"""
initial_state_1 = state_tuple(d=0, e='F1', F1=['thG', 'thM', 'plG', 'stG'], F2=['plM', 'stM'], F3=['prG', 'prM', 'ruG', 'ruM'], F4=[])

data_2 = """
The first floor contains a thulium generator, a thulium-compatible microchip, a plutonium generator, a strontium generator, an elerium generator, an elerium-compatible microchip, a dilithium generator, and a dilithium-compatible microchip.
The second floor contains a plutonium-compatible microchip and a strontium-compatible microchip.
The third floor contains a promethium generator, a promethium-compatible microchip, a ruthenium generator, and a ruthenium-compatible microchip.
The fourth floor contains nothing relevant.
"""
initial_state_2 = state_tuple(d=0, e='F1', F1=['thG', 'thM', 'plG', 'stG', 'elG', 'elM', 'diG', 'diM'], F2=['plM', 'stM'], F3=['prG', 'prM', 'ruG', 'ruM'], F4=[])


def solver(input_data):
    all_elements = re.findall('([\w]*) generator', input_data, re.M)
    mapping = {}
    mchips = []
    gens = []
    valid_dict = {}

    # Create bitmask for object.
    for i, element in enumerate(all_elements):
        mapping["{0} generator".format(element)] = 2 ** (i * 2)
        mapping["{0}-compatible microchip".format(element)] = 2 ** ((i * 2) + 1)
        gens.append(2 ** (i * 2))
        mchips.append(2 ** ((i * 2) + 1))
    G = sum(gens)
    for i in _range(2 ** ((len(mapping) + 1) * 2)):
        for g in gens:

    def isvalid(v):

        for m, g in zip(mchips, gens):
            (v & m) & (v & g)
    isvalid(int('1011',2))
    # For each microchip, register invalid configurations
    invalid_states = {}
    #for i, element in enumerate(all_elements):
    #    for j, element in enumerate(all_elements)

    floors = [1, 0, 0, 0, 0]
    for i, floor_start in enumerate(input_data.strip().splitlines()):
        generators = re.findall('([\w]* generator)', floor_start)
        for g in generators:
            floors[i + 1] += mapping[g]
        microchip = re.findall('(\w*-compatible microchip)', floor_start)
        for m in microchip:
            floors[i + 1] += mapping[m]

solver(data_2)



def is_valid(s):
    for floor in [getattr(s, 'F1'), getattr(s, 'F2'), getattr(s, 'F3'), getattr(s, 'F4')]:
        generators = [x for x in floor if x.endswith('G')]
        if len(generators):
            for e in floor:
                if e[-1] == 'M':
                    if e[:2] + 'G' not in generators:
                        return False
    return True


def hash_state(s):
    return hash((s.e, tuple(sorted(s.F1)), tuple(sorted(s.F2)),
                tuple(sorted(s.F3)), tuple(sorted(s.F4))))


def get_possible_moves(s):
    possible_moves = []
    current_floor_contents = getattr(s, s.e)
    for components_to_move in list(combinations(current_floor_contents, 1)) + list(combinations(current_floor_contents, 2)):
        for new_floor in [int(s.e[1]) - 1, int(s.e[1]) + 1]:
            if new_floor < 1 or new_floor > 4:
                continue
            s_move = state_tuple(**{
                'd': s.d + 1,
                'e': "F{0}".format(new_floor),
                'F1': s.F1[:],
                'F2': s.F2[:],
                'F3': s.F3[:],
                'F4': s.F4[:]
            })
            for c in components_to_move:
                getattr(s_move, s.e).remove(c)
                getattr(s_move, s_move.e).append(c)
            if is_valid(s_move):
                possible_moves.append(s_move)
    return possible_moves


def solve(data, initial_state):
    q = PriorityQueue()
    q.put(initial_state)
    elements = re.findall('(\w*) generator', data, re.M)
    visited = {}

    while q.qsize() > 0:
        state = q.get()
        if len(state.F4) == len(elements) * 2 and state.e == 'F4':
            break
        else:
            for changed_state in get_possible_moves(state):
                h = hash_state(changed_state)
                if h not in visited:
                    q.put(changed_state)
                    visited[h] = 1
    return state

t = time.time()
solution_1 = solve(data_1, initial_state_1)
print("[Part 1] Minimum number of steps: {0} (Runtime: {1:.2f} s)".format(solution_1.d, time.time() - t))

#t = time.time()
#print("N.B. Runtime of part 2 is at least 15 minutes...")
#solution_2 = solve(data_2, initial_state_2)
#print("[Part 2] Minimum number of steps: {0} (Runtime: {1:.2f} s)".format(solution_2.d, time.time() - t))



