#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulate hands using the Vancouver mulligan

Returns turn on which Tron is achieved
"""

import card_classes
from card_classes import tron_dict, TronDeck

def vancouver_scry(library, hand):
    
    if len(hand) == 7:
        return
    
    temp = library[0]
    names = [card.name for card in hand]
    
    # determine which Tron lands aren't in the starting hand
    tron_set = set(Tron_dic.keys())
    tron_needed = tron_set.difference(set(names))
    
    num_lands = [card.card_type for card in hand].count('land')
    g_sources = set(['Forest', 'Chromatic Star', 'Chromatic Sphere'])
    
    # code below doesn't care what to do if you already have Tron in hand

    # keep on top if card is a Tron land
    if temp.name in tron_needed:
        top = True
        
    # bottom anything that's not a Tron land if hand is a 1-lander
    elif num_lands < 2:
        top = False
        
    # always top Expedition map if hand can cast and activate it
    elif temp.name == 'Expedition Map':
        top = True
        
    # keep Sylvan Scrying if hand can cast it
    elif temp.name == 'Sylvan Scrying' or temp.name == 'Ancient Stirrings':
        if len(g_sources.intersection(set(names))) > 0:
            top = True
        
    # only keep Star/Sphere if hand contains Scrying/Stirrings but no green source
    elif temp.name == 'Chromatic Star' or temp.name == 'Chromatic Sphere':
        if 'Sylvan Scrying' in names or 'Ancient Stirrings' in names \
        and len(g_sources.intersection(set(names))) == 0:
            top = True
                
    # bottom everything else
    else: 
        top = False
    
    if top is False:
        library.scry_bottom()


def play_land(card, hand, bfield):
    
    global manapool, g_mana, land_drop
    
    bfield.append(card)
    hand.pop(hand.index(card))
    manapool += 1
    
    if card.name == 'Forest':
        g_mana += 1
    
    land_drop = True
    

def sim_turn(hand, deck, bfield, tron_set):
        
    manapool = [card.card_type for card in bfield].count('land')
    g_mana = [card.name for card in bfield].count('Forest')
    
    hand_names = [card.name for card in hand]
    
    bfield_names = [card.name for card in bfield]
        
    tron_needed = tron_set.difference(set(bfield))
    land_drop = False
    
    plays = True
    while plays:
        plays = False
        
        priority = [('Expedition Map', 'ability'), ('Sylvan Scrying', 'cast'), 
                    ('Expedition Map', 'cast'), ('Ancient Stirrings', 'cast'),
                    ('Chromatic Star', 'ability'), ('Chromatic Sphere', 'ability'),
                    ('Chromatic Star', 'cast'), ('Chromatic Sphere', 'cast'),
                    ('Relic of Progenitus', 'ability'), ('Relic of Progenitus', 'cast'),
                    ('Forest', 'play'), ('Ghost Quarter', 'play'), ('Sanctum of Ugin', 'play')]
        
        # play a tron land from hand if already available
        for card_name in list(tron_needed):
            if card_name in hand_names and land_drop is False:
                card = hand[hand_names.index(card_name)]
                play_land(card, hand, bfield)
                break
        
        # play a card and return to the top of the loop 
        for card_name in priority:
            field = card_name[1]
            
            if field == 'ability' and card_name[0] in bfield:
                card = bfield[bfield_names.index(card_name)]
                if manapool >= card.amc:
                    card.ability(hand, deck, bfield)
                    plays = True
                    break
            
            if field == 'cast' and card_name[0] in hand:
                card = hand[hand_names.index(card_name)]
                if manapool >= card.cmc and g_mana >= card.gmc:
                    card.cast(hand, deck, bfield)
                    plays = True
                    break
            
            if field == 'play' and card_name[0] in hand and land_drop is False:
                card = hand[hand_names.index(card_name)]
                play_land(card, hand, bfield)
                plays = True
                break
                         
            
def sim_magic():
    
    on_draw = True
    handsize = 7
    
    Tron_dic = tron_dict()
    library = TronDeck(Tron_dic)
    bfield = []
    
    hand = library.draw_opener(handsize)
    starting_hand = hand
    
    if handsize < 7:
        vancouver_scry(library, hand)
    
    tron_set = set(Tron_dic.keys())
    tron_achieved = False
    
    turn = 0

    while tron_achieved is False:
        
        if on_draw or turn != 0:
            library.draw(hand)
        sim_turn(hand, library, bfield, tron_set)
        
        if len(tron_set.difference(set(bfield))) == 0:
            tron_achieved = True
            
        turn += 1
    
    return (starting_hand, turn)
    
    
        
                