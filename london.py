#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulate hands with the London mulligan rule
Predicts expected turns to achieve Tron using a Random Forest model rather 
than direct simulations
"""
from itertools import combinations 
import numpy as np
import pickle

import card_classes
from card_classes import TronDeck

import model_turns_vancouver as mtv

 # predicts the best possible hand from 7 cards and expected Tron turn
def eval_london_hand(handnames, handsize, on_draw, model):
    
    combs = list(combinations(handnames, handsize))
    
    # 0 is a placeholder for output (turns)
    inputs = [(sub_hand, 0) for sub_hand in combs]
    
    df_hands = mtv.assemble_table(inputs)
    df_hands['play_draw'] = [int(on_draw)] * len(inputs)    
    df_hands = mtv.new_features(df_hands)
    
    X = df_hands.drop('turns', axis = 1).iloc[:, :(df_hands.shape[1]+1)].values
    turn_pred = model.predict(X)

    best_hand = combs[turn_pred.argmin()]
    best_turn = round(min(turn_pred), 2)
    
    return (best_hand, best_turn)

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
            pred_turn = eval_london_hand(handnames, handsize, on_draw, model)[1]
            preds.append(pred_turn)
        avg_output = (handsize, round(np.mean(preds), 2))
        print(avg_output)
        avg_turns.append(avg_output)
    
    return avg_turns
        
# on_draw_avg = [(7, 4.15), (6, 4.19), (5, 4.3), (4, 4.48), (3, 4.64)]
# on_play_avg = [(7, 4.41), (6, 4.45), (5, 4.58), (4, 4.88), (3, 5.14)]

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

# on_draw_avg = [(7, 4.12), (6, 4.26), (5, 4.63), (4, 5.13), (3, 5.89)]
# on_play_avg = [(7, 4.39), (6, 4.63), (5, 5.08), (4, 5.78), (3, 6.48)]

            

