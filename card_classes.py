#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 19:21:06 2019

@author: jonathan
"""
from random import shuffle
from mulligan import shuffle_deck

def draw(hand, deck):
    hand.append(deck[0])
    deck.pop(0)

def draw_opener(handsize, deck):
    shuffle_deck(deck)
    hand = deck[:handsize]
    del deck[:handsize]
    return hand
    
class MagicCard:
    
   def __init__(self, name, cmc, card_type, colorless):
       self.name = name
       self.cmc = cmc
       self.card_type = card_type
       self.colorless = colorless
       
       
class Land(MagicCard):
    
    def __init__(self, name, basic):
        self.name = name
        self.basic = basic
        MagicCard.__init__(self, name, 1, 'land', True)
        

class AncientStirrings(MagicCard):
    
    def __init__(self):
        MagicCard.__init__(self, 'Ancient Stirrings', 1, 'sorcery', False)

    def cast(self, hand, deck, bfield, manapool, g_mana):
        tron_set = set(['Urza\'s Mine', 'Urza\'s Tower', 'Urza\'s Power Plant'])
        
        tron_needed = tron_set.difference(set(bfield))
        
        temp = deck[:5]
        
        for card in temp:
            if card.name in tron_needed and card not in hand:
                hand.append(card)
                temp.pop(temp.index(card))
                break

        # coded to prioritize achieving tron asap
        priority = ['Expedition Map', 'Chromatic Star', 'Chromatic Sphere', 
                    'Forest', 'Sanctum of Ugin', 'Ghost Quarter']
        temp_names = [x.name for x in temp]
        
        # ignores haymakers 
        if len(temp) == 5:
            for name in priority:
                if name in temp_names:
                    hand.append(temp[temp_names.index(name)])
                    temp.pop(temp_names.index(name))
                    break
                        
        del deck[:5]
        deck.extend(temp)
        manapool -= 1
        g_mana -= 1
        
        

class Chromatic(MagicCard):
    
    def __init__(self, name):
        self.name = name
        MagicCard.__init__(self, name, 1, 'artifact', True)
        
    def cast(self, manapool):
        manapool -= 1
    
    def ability(self, hand, deck, g_mana):
        g_mana += 1
        draw(hand, deck)


class Relic(MagicCard):
    
    def __init__(self):
        MagicCard.__init__(self, 'Relic of Progenitus', 1, 'artifact', True)
        
    def cast(self, manapool):
        manapool -= 1
    
    def ability(self, hand, deck, manapool):
        draw(hand, deck)
        manapool -= 1
    

def tron_tutor(hand, deck, bfield, tron_dict):
    
    # Helper function for Sylvan Scrying and Expedition Map
    
    tron_set = set(tron_dict.keys())
    tron_needed = list(tron_set.difference(set(bfield)))
    hand_names = [card.name for card in hand]
    
    # Only tutors for tron lands
    for name in tron_needed:
        if name not in hand_names:
            hand.append(tron_dict.get(name))
            deck.pop(deck.index(tron_dict.get(name)))
            break
                  
    shuffle_deck(deck) 
    
    
class SylvanScrying(MagicCard):
    
    def __init__(self):
        MagicCard.__init__(self, 'Sylvan Scrying', 2, 'sorcery', False)
        
    def cast(self, hand, deck, bfield, manapool, g_mana):
        tron_tutor(hand, deck, bfield, tron_dict)
        manapool -= 2
        g_mana -= 1

    
class ExpMap(MagicCard):
    
    def __init__(self):
        MagicCard.__init__(self, 'Expedition Map', 1, 'artifact', False)
        
    def cast(self, manapool):
        manapool -= 1
    
    def ability(self, hand, deck, bfield, manapool):        
        tron_tutor(hand, deck, bfield, tron_dict)
        manapool -= 2
        

def tron_dict():
    tower = Land('Urza\'s Tower', False)
    mine = Land('Urza\'s Mine', False)
    pplant = Land('Urza\'s Power Plant', False)
    return {tower.name:tower, mine.name:mine, pplant.name:pplant}

def tron_deck(tron_dict):
    
    sanctum = Land('Sanctum of Ugin', False)
    gq = Land('Ghost Quarter', False)
    forest = Land('Forest', True)
    
    # haymakers are treated as generic cards with no function
    karn = MagicCard('Karn Liberated', 7, 'planeswalker', True)
    ugin = MagicCard('Ugin, the Spirit Dragon', 8, 'planeswalker', True)
    ulamog = MagicCard('Ulamog, the Ceaseless Hunger', 10, 'creature', True)
    wurmcoil = MagicCard('Wurmcoil Engine', 6, 'creature', True)
    ballista = MagicCard('Walking Balista', 0, 'creature', True)
    ostone = MagicCard('Oblivion Stone', 3, 'artifact', True)
    
    emap = ExpMap()
    stirrings = AncientStirrings()
    scrying = SylvanScrying()
    star = Chromatic('Chromatic Star')
    sphere = Chromatic('Chromatic Sphere')
    relic = Relic()
    
    tron_lands = list(tron_dict.values())*4
    
    quads = [karn, wurmcoil, ostone, emap, stirrings, scrying, star, sphere]*4
    trips = [relic]*3
    dups = [ulamog, ballista, ugin]*2
    singles = [sanctum, gq]
    forests = [forest]*5
    return tron_lands + quads + trips + dups + singles + forests





bfield = []
manapool = 1
g_mana = 1





