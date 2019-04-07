#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Train a Random Forest model to predict turns to achieve Tron, using data
from simulated games
"""

from collections import Counter
import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

import vancouver as vc

# simulates n*5 hands and saves to a list
def sim_hands(n, on_draw):
    '''
    n -- (int) number of simulations per starting handsize
    draw -- (boolean) on the draw
    '''

    output = []
    
    for handsize in range(3,8):
        for j in range(n):
            sim = vc.sim_magic(handsize, on_draw)
            output.append(sim)
    
    return output
            
# formats hand and output turn for dataframe
def format_hand(hand):
    
    # only considers cards relevant to assembling Tron as features
    relevant_cards = ['Urza\'s Tower', 'Urza\'s Mine', 'Urza\'s Power Plant',
                      'Forest', 'Ghost Quarter', 'Sanctum of Ugin',
                      'Chromatic Star', 'Chromatic Sphere', 
                      'Relic of Progenitus', 'Ancient Stirrings', 
                      'Sylvan Scrying', 'Expedition Map']
    
    counts = Counter(hand[0])
    
    # output of model - number of turns to achieve Tron
    hand_dict = {'handsize':len(hand[0]), 'turns':hand[1]}
    
    for card in relevant_cards: 
        if card in counts.keys():
            hand_dict[card] = counts[card]
        else:
            hand_dict[card] = 0
            
    return hand_dict
            
# joins simulated hands into a dataframe
def assemble_table(hands):

    hands_as_dicts = [format_hand(hand) for hand in hands]
    tron_df = pd.DataFrame(hands_as_dicts)
    return tron_df

def create_df(n, on_draw):
    '''
    n -- (int) number of simulations per starting hand
    on_draw -- (boolean)
    '''
    sim_data = sim_hands(n, on_draw)
    df_sim = assemble_table(sim_data)
    df_sim['play_draw'] = [int(on_draw)] * (n*5)
    
    return df_sim


# helper function to count presence of unique cards in hand
def unique_counts(arr):
    
    count = 0
    for num in arr:
        if num:
            count += 1
        else:
            continue
    
    return count


# count combinations of features as a new feature
def unique_total(df, cols):
    '''
    df -- input dataframe
    cols -- list of column names
    '''
    df_sub = df[cols]
    new_col = [unique_counts(row) for row in df_sub.itertuples(index = False)]
    return new_col


def unique_sum(df, cols):
    '''
    df -- input dataframe
    cols -- list of column names
    '''
    df_sub = df[cols]
    new_col = [sum(row) for row in df_sub.itertuples(index = False)]
    return new_col

def new_features(df):
    
    # combine counts for chromatic star and chromatic sphere
    df['Chromatic Total'] = df['Chromatic Star'] + df['Chromatic Sphere']
    # combine counts for non-Tron non-Forest lands
    df['Other Lands'] = df['Ghost Quarter'] + df['Sanctum of Ugin']
    # drop the original columns
    df.drop(['Chromatic Star', 'Chromatic Sphere', 
             'Ghost Quarter', 'Sanctum of Ugin'], 
            axis = 1, inplace = True)
   
    # number of unique Tron lands as a feature  
    df['tron_count'] = unique_total(
            df,
            [ "Urza's Mine", 
             "Urza's Power Plant", 
             "Urza's Tower"])
    # unique Tron lands + Map as a feature
    df['tron_map_count'] = unique_total(
            df, 
            ['Expedition Map', 
             "Urza's Mine", 
             "Urza's Power Plant", 
             "Urza's Tower"])
    # total number of lands as a feature
    df['total_lands'] = unique_sum(
            df, 
            ["Urza's Mine", 
             "Urza's Power Plant", 
             "Urza's Tower", 
             'Other Lands'])
    
    return df

# generate dataframe and engineer features
def prep_df(n):
    # n -- (int) number of simulations per starting hand 
    print('performing', n*10, 'simulations')
    
    df_draw = create_df(n, True)
    df_play = create_df(n, False)

    df = pd.concat([df_draw, df_play], sort = True)

    print('assembling table...')
    
    # remove outliers
    df = df[df['turns'] < 16]
    
    print('adding features...')

    df = new_features(df)
    
    return df


def train_random_forest(df):
    
    y = df.iloc[:, 10].values
    X = df.drop('turns', axis = 1).iloc[:, :(df.shape[1]+1)].values
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, 
                                                    random_state = 0)  
    
    # optimized using GridSearchCV
    regressor = RandomForestRegressor(n_estimators = 500,
                                  min_samples_split = 2,
                                  min_samples_leaf = 4,
                                  max_features = 'sqrt',
                                  max_depth = 10,
                                  bootstrap = True,
                                  random_state = 0)
    
    regressor.fit(X_train, y_train)
    
    '''    
    training_error = abs(regressor.predict(X_train) - y_train)
    round(np.mean(training_error), 2)
    # mae = 1.23
    
    y_pred = regressor.predict(X_test)
    errors = abs(y_pred - y_test)
    round(np.mean(errors), 2)
    # mae = 1.24
    '''
    return regressor


# helper function for base prediction
def predict_by_mean(df, means):
    
    preds = []
    
    handsize = df['handsize']
    for n in handsize:
        pred = means[n]
        preds.append(pred)
    
    return(preds)
      
    
# comparison to base case - average per handsize
def base_prediction(df):
    
    by_handsize = df.groupby('handsize')
    handsize_means = by_handsize.apply(lambda x: np.mean(x['turns']))
    naive_pred = predict_by_mean(df, handsize_means)
    naive_error = abs(naive_pred - df['turns'])
    print(round(np.mean(naive_error), 2))
    # base error of 1.6
   
    
def main():
    num_sims = 5000
    df = prep_df(num_sims)
    model = train_random_forest(df)
    #outfile = 'TronRandomForest.model'
    #pickle.dump(model, open(outfile, 'wb'))
    return model


if __name__ == '__main__':
    main()
