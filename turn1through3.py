#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 10:34:10 2019

@author: jonathan
"""

'''
turn 1 optimal plays:
    1. play a tron land
        a. play a map
        b. play an egg
    2. play a forest
        a. play ancient stirrings
        b. play a map
        c. play an egg
        b. play nothing
    3. play any gq/sanctum
        a. play a map
        b. play an egg

turn 2 optimal plays:
    1. play 2nd tron land
        a. crack map if in play
        b. crack egg if in play and cast scrying
        c. crack egg if in play and cast stirrings
        c. cast map
        d. cast egg and stirrings
        e. cast egg
    
    2. play first tron land
        a. crack map
        b. crack egg if in play and cast scrying
        c. cast scrying
        d. crack egg if in play and cast stirrings
        e. cast stirrings
        f. cast map
        g. cast egg
    
    3. play first non-tron land
        ...find tron pieces
        
    4. play 2nd non-tron land
        ..end loop as t4 tron can't be achieved
'''
import numpy as np

from mulligan import tron_list, shuffle_deck
from random import shuffle


class MagicCard:
    
   def __init__(self, name, cmc, card_type):
       self.name = name
       self.cmc = cmc
       self.card_type = card_type
       




def draw_opener(handsize, deck):
    shuffle_deck(deck)
    hand = deck[:handsize]
    del deck[:handsize]
    return hand
    
def draw(hand, deck):
    hand.append(deck[0])
    deck.pop(0)

def play_card(card, hand, bfield, manapool):
    permanents = ['land', 'artifact', 'creature', 'planeswalker', 'enchantment']
    manapool -= card.cmc
    hand.pop(hand.index(card))
    card.effect()
    if card.type in permanents:
        bfield.append(card)
        


    
def turn(hand, deck, bfield):
    manapool = len(bfield)
    draw(hand, deck)
    land_drop = False
    
    # play a tron land if possible
    
    for card in hand:
        if card in list(tron_set.difference(set(bfield))):
            play_card(card, hand, bfield)
            land_drop = True
            manapool += 1
            break
    
    
    
def play_magic():
    
    tron_set = set(['mine', 'tower', 'p-plant'])
    
    deck = tron_list()
    hand = draw_opener(7, deck)
    bfield = []

    tron = False
    turncount = 0
    while turncount <= 4 and tron == False:
        turncount += 1
        turn(hand, deck, bfield)
        if tron_set.intersection(set(bfield)) == 3:
            tron = True
            
    return turncount
    
    













    