#!/usr/bin/env python3 v1.1
# -*- coding: utf-8 -*-
"""
Classes for the Tron deck, and cards within the deck.
"""

from random import shuffle


# generic Magic Card class
class MagicCard:
    
   def __init__(self, name, cmc, card_type, colorless, gmc):
       self.name = name
       self.cmc = cmc
       self.card_type = card_type
       self.colorless = colorless
       self.gmc = gmc
       
# class to specify Land cards
class Land(MagicCard):
    
    def __init__(self, name, basic):
        self.name = name
        self.basic = basic
        MagicCard.__init__(self, name, 0, 'land', True, 0)

# dictionary of Tron lands, with keys as card names, for other functions       
def tron_dict():
    tower = Land('Urza\'s Tower', False)
    mine = Land('Urza\'s Mine', False)
    pplant = Land('Urza\'s Power Plant', False)
    return {tower.name:tower, mine.name:mine, pplant.name:pplant}


# stored as a global variable to match object location across functions
Tron_dic = tron_dict()

        
# class to simulate casting Ancient Stirrings
class AncientStirrings(MagicCard):
    
    def __init__(self):
        MagicCard.__init__(self, 'Ancient Stirrings', 1, 'sorcery', False, 1)

    def cast(self, hand, deck, bfield):
        
        global manapool, g_mana
        tron_set = set(Tron_dic.keys())
        
        # determine which lands are still needed for Tron
        tron_needed = tron_set.difference(set(bfield))
        
        # look at the top five cards of the deck
        temp = deck.deck[:5]
        
        # selects a Tron land to add to hand, if available
        for card in temp:
            if card.name in tron_needed and card not in hand:
                hand.append(card)
                temp.pop(temp.index(card))
                break

        # selecting another card if no new Tron lands in top 5 cards
        temp_names = [card.name for card in temp]

        # coded to prioritize achieving Tron over all else
        priority = ['Expedition Map', 'Chromatic Star', 'Chromatic Sphere', 
                    'Forest', 'Urza\'s Tower', 'Urza\'s Mine', 'Urza\'s Power Plant',
                    'Sanctum of Ugin', 'Ghost Quarter']
        
        if len(temp) == 5:
            for name in priority:
                if name in temp_names:
                    hand.append(temp[temp_names.index(name)])
                    temp.pop(temp_names.index(name))
                    break
                
        # remove the top five cards of the deck
        del deck.deck[:5]
        
        # put the remaining 4 cards on the bottom of the deck
        deck.deck.extend(temp) 
        
        manapool -= 1
        g_mana -= 1
        
        
# class to simulate casting and activating Chromatic Star/Sphere
class Chromatic(MagicCard):
    
    def __init__(self, name):
        self.name = name
        self.amc = 1
        MagicCard.__init__(self, name, 1, 'artifact', True, 0)
        
    def cast(self, hand, deck, bfield):
        global manapool
        bfield.append(self)
        manapool -= 1
    
    def ability(self, hand, deck, bfield):
        global manapool, g_mana
        deck.draw(hand)
        bfield.pop(bfield.index(self))
        g_mana += 1
        

# class to simulate casting and activating Relic of Progenitus
class Relic(MagicCard):
    
    def __init__(self):
        self.amc = 1
        MagicCard.__init__(self, 'Relic of Progenitus', 1, 'artifact', True, 0)
        
    def cast(self, hand, deck, bfield):
        global manapool
        bfield.append(self)
        manapool -= self.amc
        
    def ability(self, hand, deck, bfield):
        global manapool
        deck.draw(hand)
        bfield.pop(bfield.index(self))
        manapool -= 1

   
    
# helper function for Sylvan Scrying and Expedition Map
def tron_tutor(hand, deck, bfield):
    
    tron_set = set(Tron_dic.keys())
    
    # determine which Tron lands are still needed
    tron_needed = list(tron_set.difference(set(bfield)))
    hand_names = [card.name for card in hand]
    
    # move a Tron land from deck to hand (only tutors Tron lands)
    for name in tron_needed:
        if name not in hand_names:
            hand.append(Tron_dic.get(name))
            deck.deck.pop(deck.deck.index(Tron_dic.get(name)))
            break
          
    deck.shuffle()


# class to simulate casting Sylvan Scrying    
class SylvanScrying(MagicCard):
    
    def __init__(self):
        MagicCard.__init__(self, 'Sylvan Scrying', 2, 'sorcery', False, 1)
        
    def cast(self, hand, deck, bfield):
        
        global manapool, g_mana
        tron_tutor(hand, deck, bfield)
        manapool -= self.cmc
        g_mana -= 1
        
        
# class to simulate casting and activating Expedition Map  
class ExpMap(MagicCard):
    
    def __init__(self):
        self.amc = 2
        MagicCard.__init__(self, 'Expedition Map', 1, 'artifact', False, 0)
        
    def cast(self, bfield):
        
        global manapool
        bfield.append(self)
        manapool -= self.amc
    
    def ability(self, hand, deck, bfield):
        
        global manapool
        tron_tutor(hand, deck, bfield)
        bfield.pop(bfield.index(self))
        manapool -= 2



# generates a Tron decklist
def decklist(tron_dict):
    
    sanctum = Land('Sanctum of Ugin', False)
    gq = Land('Ghost Quarter', False)
    forest = Land('Forest', True)
    
    # haymakers are treated as generic cards with no function
    karn = MagicCard('Karn Liberated', 7, 'planeswalker', True, 0)
    ugin = MagicCard('Ugin, the Spirit Dragon', 8, 'planeswalker', True, 0)
    ulamog = MagicCard('Ulamog, the Ceaseless Hunger', 10, 'creature', True, 0)
    wurmcoil = MagicCard('Wurmcoil Engine', 6, 'creature', True, 0)
    ballista = MagicCard('Walking Balista', 0, 'creature', True, 0)
    ostone = MagicCard('Oblivion Stone', 3, 'artifact', True, 0)
    
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


# class to simulate the library as a stack
class TronDeck:
    
    def __init__(self, Tron_dic):
        self.deck = decklist(Tron_dic)
    
    def shuffle(self):
        for i in range(0,5):
            shuffle(self.deck)
    
    # draw opening hand
    def draw_opener(self, handsize):
        self.shuffle()
        hand = self.deck[:handsize]
        del self.deck[:handsize]
        return hand
    
    def draw(self, hand):
        hand.append(self.deck[0])
        self.deck.pop(0)
    
    def scry_bottom(self):
        self.deck.append(self.deck[0])
        del self.deck[0]

'''
def main():
    d = TronDeck()
'''





