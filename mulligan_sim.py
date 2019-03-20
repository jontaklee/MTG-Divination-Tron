#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulates mulligans using the Paris and London mulligan rules

Returns the probability of an opening hand with turn 3 Tron
when willing to mulligan to 3 card hands
"""
import numpy as np

import card_classes
from card_classes import TronDeck
    
def eval_tron_hand(opener, true_hand_size):
    
    # determines whether to mulligan an opening hand
    # only keeps hands with guaranteed turn 3 tron (without disruption)
    
    tron_set = set(['Urza\'s Tower', 'Urza\'s Mine', 'Urza\'s Power Plant'])
    color_filters = set(['Chromatic Star', 'Chromatic Sphere'])
    
    hand_names = [card.name for card in opener]
    unique_cards = set(hand_names)
    
    # keep if all three tron lands in opening hand
    if len(tron_set.intersection(unique_cards)) == 3:
        keep = True
    
    # keep if 2 tron lands + map, or 2 tron lands + sylvan scrying + color filtering
    elif len(tron_set.intersection(unique_cards)) == 2:
        if 'Expedition Map' in unique_cards:
            keep = True
        elif len(color_filters.intersection(unique_cards)) >= 1 \
        and 'Sylvan Scrying' in unique_cards \
        and true_hand_size > 3:
            keep = True
        
        else: keep = False
        
    else:
        keep = False
    
    return keep

def paris_method(n):
    '''
    n: number of simulations to perform
    '''
    decisions = []

    for i in range(n):
        keep = False
        mull_count = 0
        while mull_count <= 4 and keep == False:
            library = TronDeck()
            start_size = 7 - mull_count
            opener = library.draw_opener(start_size)
            keep = eval_tron_hand(opener, start_size)
            mull_count += 1
        
        decisions.append(keep)         
    
    return np.mean(decisions)
            

def london_method(n):
    
    decisions = []

    for i in range(n):
        keep = False
        mull_count = 0
        while mull_count <= 4 and keep == False:
            library = TronDeck()
            effective_size = 7 - mull_count
            opener = library.draw_opener(7)
            keep = eval_tron_hand(opener, effective_size)
            mull_count += 1
        
        decisions.append(keep)         
    
    return np.mean(decisions)

    
def main():
    sample_size = 10000
    paris_success_rate = round(paris_method(sample_size), 3)
    london_success_rate = round(london_method(sample_size), 3)
    print('paris success:', paris_success_rate)
    print('london success:', london_success_rate)

if __name__ == '__main__':
    main()
    
