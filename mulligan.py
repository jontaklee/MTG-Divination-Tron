#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 09:10:53 2019

@author: jonathan
"""
import numpy as np
from random import shuffle

def tron_list():
    
    # outputs a representative tron deck to an array
    # future implementation should allow import of own decklists, and card classes
    
    cantrips = ['star']*4 + ['sphere']*4 + ['stirrings']*4
    creatures = ['ballista']*2 + ['wurmcoil']*4 + ['ulamog']*2
    walkers = ['karn']*4 + ['ugin']*2
    search = ['map']*4 + ['scrying']*4
    other_artifacts = ['relic']*3 + ['o-stone']*4
    tron_lands = ['mine']*4 + ['tower']*4 + ['p-plant']*4
    other_lands = ['forest']*5 + ['g-quarter'] + ['sanctum']
    
    decklist = cantrips + creatures + walkers + search + other_artifacts + tron_lands + other_lands
    return decklist

def shuffle_deck(deck):

    # shuffles the deck five times to ensure randomness
    for i in range(0,5):
        shuffle(deck)
        
def draw_opener(handsize, deck):
    shuffle_deck(deck)
    return deck[:handsize]
    
def eval_tron_hand(opener, true_hand_size):
    
    # determines whether to mulligan an opening hand
    # only keeps hands with guaranteed turn 3 tron (without disruption)
    
    tron_set = set(['mine', 'tower', 'p-plant'])
    color_filters = set(['star', 'sphere'])
    
    unique_cards = set(opener)
    
    # keep if all three tron lands in opening hand
    if len(tron_set.intersection(unique_cards)) == 3:
        keep = True
    
    # keep if 2 tron lands + map, or 2 tron lands + sylvan scrying + color filtering
    elif len(tron_set.intersection(unique_cards)) == 2:
        if 'map' in unique_cards:
            keep = True
        elif len(color_filters.intersection(unique_cards)) >= 1 and 'scrying' in unique_cards:
            if true_hand_size > 3:
                keep = True
        
        # mulligan any other hand         
            else: 
                keep = False
        else:
            keep = False
    else:
        keep = False
    
    return keep

def paris_method(n):
    
    deck = tron_list()
    decisions = []

    for i in range(n):
        keep = False
        mull_count = 0
        while mull_count <= 4 and keep == False:
            start_size = 7 - mull_count
            opener = draw_opener(start_size, deck)
            keep = eval_tron_hand(opener, start_size)
            mull_count += 1
        
        decisions.append(keep)         
    
    return np.mean(decisions)
            

def london_method(n):
    
    deck = tron_list()
    decisions = []

    for i in range(n):
        keep = False
        mull_count = 0
        while mull_count <= 4 and keep == False:
            effective_size = 7 - mull_count
            opener = draw_opener(7, deck)
            keep = eval_tron_hand(opener, effective_size)
            mull_count += 1
        
        decisions.append(keep)         
    
    return np.mean(decisions)

    
def main():
    sample_size = 100
    n_samples = 100
    paris_success_rate = round(np.mean([paris_method(sample_size) for x in range(n_samples)]), 3)
    london_success_rate = round(np.mean([london_method(sample_size) for x in range(n_samples)]), 3)
    print('paris success:', paris_success_rate)
    print('london success:', london_success_rate)


if __name__ == '__main__':
    main()
    
    
    
    
    