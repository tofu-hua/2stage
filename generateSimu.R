##################################################
### generate two datasets for simulation study ###
##################################################

set.seed(0322)
mu_0 = 1500
sigma_0 = mu_0/5
n_player = 100
n_match = 10000

# generate players dictionary
gen_player <- function(n_player){
  player_matrix = matrix(rep(NA, n_player*2), n_player, 2)
  player_matrix = as.data.frame(player_matrix)
  colnames(player_matrix) = c('id', 'true_mu')
  player_matrix[,1] = 1:n_player
  player_matrix[,2] = rnorm(n_player, mean = mu_0, sd = sigma_0)
  
  return(player_matrix)
}

player_matrix = gen_player(n_player)

#####################################
## I. 2 teams, each with 2 players ##
#####################################
player1_weight = 0.75
player2_weight = 1-player1_weight

# generate matches
gen_match_two <- function(n_match){
  b=log(10)/400
  gen_dat <- matrix(rep(NA, n_match*5), n_match, 5)
  gen_dat <- as.data.frame(gen_dat)
  colnames(gen_dat) <- c('game_id', 'winner1', 'winner2', 'loser1', 'loser2')
  gen_dat[,1] <- c(1:n_match)
  for(i in 1:n_match){
    player_pick <- sample(1:n_player, 4, replace = FALSE)
    player_1 = player_pick[1]
    player_2 = player_pick[2]
    player_3 = player_pick[3]
    player_4 = player_pick[4]
    player_list = c(player_1, player_2, player_3, player_4)
    team_1_mu = player_matrix[player_1, 2]*player1_weight + player_matrix[player_2, 2]*player2_weight
    team_2_mu = player_matrix[player_3, 2]*player1_weight + player_matrix[player_4, 2]*player2_weight
    
    player_array = array(player_list, dim = c(1, 2, 2), dimnames = list(c('team_member'), c('player_1', 'player_2'), c('team1', 'team2')))
    s = rbinom(1, 1, prob = exp(b*team_1_mu)/(exp(b*team_1_mu)+exp(b*team_2_mu))) #r = 1 <- team_1 win
    if(s%%2 == 1){
      winner_team = player_array[,,1]
      loser_team = player_array[,,2]
    }else{
      winner_team = player_array[,,2]
      loser_team = player_array[,,1]
    }
    
    gen_dat[i,2:5] = c(winner_team, loser_team)
  }
  return(gen_dat)
}
#
game_dat <- gen_match_two(n_match)
#write.csv(game_dat, 'simu_data1.csv', row.names = FALSE)

######################################
## II. 2 teams, each with 5 players ##
######################################
player_weight = c(0.4, rep(0.15, 4))

#generate matches
gen_match_five <- function(n_match){
  b=log(10)/400
  gen_dat <- matrix(rep(NA, n_match*11), n_match, 11)
  gen_dat <- as.data.frame(gen_dat)
  colnames(gen_dat) <- c('game_id', 'winner1', 'winner2', 'winner3', 'winner4', 'winner5', 'loser1', 'loser2', 'loser3', 'loser4', 'loser5')
  gen_dat[,1] <- c(1:n_match)
  for(i in 1:n_match){
    player_pick <- sample(1:n_player, 10, replace = FALSE)
    team_1_mu = sum(player_matrix[player_pick[1:5], 2]*player_weight)
    team_2_mu = sum(player_matrix[player_pick[6:10], 2]*player_weight)
    player_array = array(player_pick, dim = c(1, 5, 2), dimnames = list(c('team_member'), c('player_1', 'player_2','player_3','player_4','player_5'), c('team1', 'team2')))
    s = rbinom(1, 1, prob = exp(b*team_1_mu)/(exp(b*team_1_mu)+exp(b*team_2_mu))) #r = 1 <- team_1 win
    if(s%%2 == 1){
      winner_team = player_array[,,1]
      loser_team = player_array[,,2]
    }else{
      winner_team = player_array[,,2]
      loser_team = player_array[,,1]
    }
    gen_dat[i,2:11] = c(winner_team, loser_team)
  }
  return(gen_dat)
}
game_dat <- gen_match_five(n_match)
write.csv(game_dat, 'simu.csv', row.names = FALSE)