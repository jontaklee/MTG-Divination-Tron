#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulate hands with the London mulligan rule
Predicts expected turns to achieve Tron using a Random Forest model rather 
than direct simulations
"""
from itertools import combinations 
import numpy as np
import pandas as pd
import pickle

import card_classes
from card_classes import TronDeck

import model_turns as mtv

 # predicts the best possible hand from 7 cards and expected Tron turn
def best_hand(handnames, handsize, on_draw, model):
    
    combs = list(combinations(handnames, handsize))
    
    # 0 is a placeholder for output (turns)
    inputs = [(sub_hand, 0) for sub_hand in combs]
    
    df_hands = mtv.assemble_table(inputs)
    df_hands['play_draw'] = [int(on_draw)] * len(inputs)    
    df_hands = mtv.new_features(df_hands)
    
    X = df_hands.drop('turns', axis = 1).iloc[:, :(df_hands.shape[1]+1)].values
    turn_pred = model.predict(X)

    best_cards = combs[turn_pred.argmin()]
    best_turn = round(min(turn_pred), 2)
    
    return (best_cards, best_turn)


# estimate average turns to achieve tron using 1000 simulations
def expected_turns(on_draw):
    
    # this model is trained on hands that don't scry on mulligans
    model = pickle.load(open('TronRandomForest_noscry.model', 'rb'))
    avg_turns = []
    
    for handsize in range(7, 2, -1):
        preds = []
        for i in range(1000):
            library = TronDeck()
            hand = library.draw_opener(7)
            handnames = [card.name for card in hand]
            pred_turn = best_hand(handnames, handsize, on_draw, model)[1]
            preds.append(pred_turn)
        avg_output = (handsize, round(np.mean(preds), 2))
        print(avg_output)
        avg_turns.append(avg_output)
    
    return avg_turns
        

# expected number of turns using vancouver rule:
def expected_vancouver(on_draw):
    
    # this model is trained on hands with the Vancouver scry
    model = pickle.load(open('TronRandomForest.model', 'rb'))
    avg_turns = []
    
    for handsize in range(7, 2, -1):
        preds = []
        for i in range(1000):
            library = TronDeck()
            hand = library.draw_opener(handsize)
            hand_in = ([card.name for card in hand],0)
            df_hands = mtv.assemble_table([hand_in])
            df_hands['play_draw'] = [int(on_draw)]    
            df_hands = mtv.new_features(df_hands)
            
            X = df_hands.drop('turns', axis = 1).iloc[:, :(df_hands.shape[1]+1)].values
            turn_pred = model.predict(X)
            preds.append(turn_pred)
        
        avg_output = (handsize, round(np.mean(preds), 2))
        print(avg_output)
        avg_turns.append(avg_output)
    
    return avg_turns

# helper function to run and save simulations
def sim_london(on_draw):
    
    # this model is trained on hands that don't scry on mulligans
    model = pickle.load(open('TronRandomForest_noscry.model', 'rb'))
    output = []
    
    for handsize in range(7, 2, -1):
        print('simulating {0} card hands'.format(handsize))
        for i in range(5000):
            library = TronDeck()
            hand = library.draw_opener(7)
            handnames = [card.name for card in hand]
            pred_turn = best_hand(handnames, handsize, on_draw, model)[1]
            result = (handsize, int(on_draw), round(pred_turn, 2))
            output.append(result)
    
    return output

# create a table of simulated results
def create_sims_table():
    
    sims_draw = sim_london(True)
    sims_play = sim_london(False)
    sims_tot = sims_draw + sims_play
    
    dfs = pd.Dataframe(sims_tot, columns = ['handsize', 'play_draw', 'pred'])
    dfs.to_csv('london_sims_RandomForest.csv', index = False)

# helper function to process a user inputted hand
def input_hand():
    
    library = TronDeck()
    valid_cards = set([card.name for card in library.deck])
    
    names = input('Input your 7 cards (Full names, capitalized, separated by ;): ')
    names = names.split(';')
    if len(names) != 7:
        raise ValueError('your opener must contain 7 cards')
    # remove whitespace if present between card names
    names = [name.lstrip() for name in names]
    num_valid = len(set(names).intersection(valid_cards))
    if num_valid == len(set(names)):
        return(names)
    else:
        raise ValueError('invalid card name in hand')

# helper function to process a user input for play/draw
def input_play_draw():
    
    draw = input('Are you on the draw (y/n)? ')
    if draw == 'y':
        return True
    elif draw == 'n':
        return False
    else:
        raise ValueError('input must be y/n')

# evaluate an input hand and compare it to the next round of mulligans
def main():
    
    handnames = input_hand()
    on_draw = input_play_draw()
    num_mull = int(input('How many times did you mulligan (0-4)? '))
    handsize = 7 - num_mull
    
    model = pickle.load(open('TronRandomForest_noscry.model', 'rb'))
    
    best = best_hand(handnames, handsize, on_draw, model)
    
    df = pd.read_csv('london_sims_RandomForest.csv')
    df_sub = df[df['play_draw'] == int(on_draw)]
    df_sub = df_sub[df_sub['handsize'] == handsize-1]
    
    percentile = round((sum(df_sub['pred'] >= best[1])/len(df_sub['pred']) * 100))
    
    print('Your best {0} card hand is:\n{1}'.format(handsize, best[0]))
    print('It is predicted to achieve Tron on turn', round(best[1], 2))
    print('This is better than {0}% of {1} card hands'.format(percentile, handsize-1))
    

if __name__ == '__main__':
    main()
            

