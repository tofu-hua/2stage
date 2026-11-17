# -*- coding: utf-8 -*-
#  Usage:  python3 elo_simu2.py 
#  need "simu_data2.csv" in the same folder
#  It is a simulation study for two-team match with 5 players in each team, using eloD with unequal weights.

import numpy as np
import pandas as pd
from collections import defaultdict
from sklearn.preprocessing import LabelEncoder
import copy
import os
from sys import argv
import sys
import math
from locale import atof, atoi


#####################
# probability model #
#####################

def sigmoid(cur_mu_w, cur_mu_l, c_wl):
  x = (cur_mu_w-cur_mu_l)/c_wl
  return 1/(1+np.exp(-x))

#####################
# Data Preparation ##
#####################

names = ['game_id','winner1', 'winner2', 'winner3','winner4','winner5', 'loser1', 'loser2', 'loser3', 'loser4', 'loser5']
data = pd.read_csv("simu.csv", header=0, names = names)
cutpoint = math.ceil(max(data['game_id'])*0.4)
Train = data[data['game_id'] <= cutpoint]
Test = data[data['game_id'] > cutpoint]


col_name =  ['winner1','winner2','winner3','winner4','winner5','loser1','loser2', 'loser3', 'loser4', 'loser5']
winners_all,losers_all = data[col_name[:len(col_name)//2]], data[col_name[len(col_name)//2:]]
Train, Test = Train[col_name], Test[col_name]
winners,losers = Train[col_name[:len(col_name)//2]], Train[col_name[len(col_name)//2:]]
winners_val,losers_val = Test[col_name[:len(col_name)//2]], Test[col_name[len(col_name)//2:]]

###############################
## EloD with unequal weights ##
###############################

def eloD_weight(winners, losers, K, weight, start_mean = 1500, 
         mode = 'train', prior_ratings=None):
    file_name = 'eloD_weight_' + mode + '.txt'
    if K == 0:
      print('Error: K should not be 0')
      sys.exit(0)
    if mode.lower() =='train':
      prior_ratings = defaultdict(lambda: start_mean) 
    elif mode.lower() not in ['test','train']:
      print(f'WARNING: Ur input of mode is {mode} and the current mode is "Train" ')

    with open(file_name,'w', encoding="utf-8") as f:
      str2 = 'game, winner_mean_old, loser_mean_old, winner_mean, loser_mean, phat'
      f.write(str2+'\n')
      player_double = list(zip(winners['winner1'],winners['winner2'],winners['winner3'],winners['winner4'],winners['winner5'],losers['loser1'],losers['loser2'],losers['loser3'],losers['loser4'],losers['loser5']))
      
      count,tie,total,total_discrepancy = 0,0,0,0
      b = np.log(10)/400
      for game in np.arange(winners.shape[0]):
        current_players = player_double[game]
        current_winner1, current_winner2, current_winner3, current_winner4, current_winner5 = current_players[0],current_players[1],current_players[2],current_players[3], current_players[4]
        current_loser1, current_loser2, current_loser3, current_loser4, current_loser5 = current_players[5],current_players[6],current_players[7], current_players[8], current_players[9]

        # collect prior rating in player_rating        
        new_rating = prior_ratings.copy()

        # each player mean & variance
        winner1_mean, winner2_mean, winner3_mean, winner4_mean, winner5_mean = new_rating[current_winner1], new_rating[current_winner2], new_rating[current_winner3], new_rating[current_winner4], new_rating[current_winner5]
        loser1_mean, loser2_mean, loser3_mean, loser4_mean, loser5_mean = new_rating[current_loser1], new_rating[current_loser2], new_rating[current_loser3], new_rating[current_loser4], new_rating[current_loser5] 
        # calculate team meam & variance
        winner_mean = sum([winner1_mean,winner2_mean,winner3_mean,winner4_mean,winner5_mean])
        loser_mean = sum([loser1_mean,loser2_mean,loser3_mean,loser4_mean,loser5_mean])
        # compare and count the correct prediction
        if winner_mean > loser_mean:
          count +=1
        if winner_mean == loser_mean:
          tie +=1
        total +=1

        # calculate p_iq ,p_qi   
        p_iq = sigmoid(winner_mean, loser_mean, 1/b)
        p_qi = 1-p_iq
        # define s: game outcome
        winner_s, loser_s = 1, 0
        # Ki
        K_i = K*(winner_s-p_iq)
        K_q = K*(loser_s-p_qi)
        
        # sum discrepancy
        discrepancy = -np.log(p_iq)
        total_discrepancy += discrepancy
        # update winner
        keys = [current_winner1, current_winner2, current_winner3, current_winner4, current_winner5]
        for j in range(0,5):
          new_rating[keys[j]] = new_rating[keys[j]] + K_i*weight[j]

        # update loser
        keys = [current_loser1, current_loser2, current_loser3, current_loser4, current_loser5]
        for j in range(0,5):
          new_rating[keys[j]] = new_rating[keys[j]] + K_q*weight[j]

       # save record
        str2 ='%2d, %4.3f, %4.3f, %4.3f, %4.3f, %.4f\n'%(game+1, winner_mean,loser_mean,winner_mean + K_i,loser_mean + K_q, p_iq)
        f.write(str2) # save
        # update prior rating
        prior_ratings = new_rating  
    f.close()
    error = total-count-tie
    misclassified_rate = error/(total-tie)
    return prior_ratings, misclassified_rate, (total,count,tie), total_discrepancy/winners.shape[0]
    # total(n) - (accurate(a) + ties(t)) = error (e)


########
# Main #
########

weight0 = [0.2, 0.2, 0.2, 0.2, 0.2]
weight1 = [0.3, 0.175, 0.175, 0.175, 0.175]
weight2 = [0.4, 0.15, 0.15, 0.15, 0.15] # true weights are here
weight3 = [0.5, 0.125, 0.125, 0.125, 0.125]
weight4 = [0.6, 0.1, 0.1, 0.1, 0.1]
weights = [weight0, weight1, weight2, weight3, weight4]

accVal = []
accAll = []
errVal = []
errAll = []


for weight in weights:
  #estimate, errtrain,_,_ = eloD_weight(winners,losers, K=18, weight = weight, start_mean = 1500)
  #_, err,num,_ = eloD_weight(winners_val,losers_val, K=18, weight = weight, start_mean = 1500,prior_ratings=estimate,mode='test')
  _, err,num,_ = eloD_weight(winners_all,losers_all, K=18, weight = weight, start_mean = 1500)
  _, err_all,num_all,_ = eloD_weight(winners_all,losers_all, K=25, weight = weight, start_mean = 1500)
  
  errVal.append(err)
  errAll.append(err_all)
  accVal.append(1-err)
  accAll.append(1-err_all)

# Write the header and rows matching the target paper table format
print('alpha_1 (for updating) & %.2f & %.2f & %.2f & %.2f & %.2f  \n' % (weight0[0], weight1[0], weight2[0], weight3[0], weight4[0]))
print('K = 18 & %.4f & %.4f & %.4f & %.4f & %.4f  \n' % (errVal[0], errVal[1], errVal[2], errVal[3], errVal[4]))
print('K = 25 & %.4f & %.4f & %.4f & %.4f & %.4f  \n' % (errAll[0], errAll[1], errAll[2], errAll[3], errAll[4]))

