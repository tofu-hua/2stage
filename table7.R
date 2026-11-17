######################################################################################################################################
### check the number of appearences of "Barbora Hermannova", "Marketa Slukova", "Giulia Toti", "Laura Giombini" in train/test sets.  #
######################################################################################################################################

df = read.csv("volley.csv")

dTr <- df[df$year <= 2014, ]
dTe <- df[df$year > 2014, ]

giulia = which(dTr[,5]=="Giulia Toti" | dTr[,6]=="Giulia Toti" | dTr[,7]=="Giulia Toti" | dTr[,8]=="Giulia Toti")  
length(giulia)  # [1] 20 # i.e. Giulia has played 20 matches in train set 
G_win = length(which(dTr[,5]=="Giulia Toti" | dTr[,6]=="Giulia Toti"))   # [1] 2  # Of the 20 matches, 2 are on winning side  
G_lose = length(which(dTr[,7]=="Giulia Toti" | dTr[,8]=="Giulia Toti"))   # [1] 18  # Of the 20 matches, 18 are on the losing side

laura = which(dTr[,5]=="Laura Giombini" | dTr[,6]=="Laura Giombini" | dTr[,7]=="Laura Giombini" | dTr[,8]=="Laura Giombini") 
length(laura)  # [1] 110
L_win = length(which(dTr[,5]=="Laura Giombini" | dTr[,6]=="Laura Giombini"))
# [1] 41  # Of the 110 matches, 41 are on the winning side.
L_lose = length(which(dTr[,7]=="Laura Giombini" | dTr[,8]=="Laura Giombini")) 
# [1] 69   # Of the 110 matches, 69 are on the losing side.

Hermannova = which(dTr[,5]=="Barbora Hermannova" | dTr[,6]=="Barbora Hermannova" | dTr[,7]=="Barbora Hermannova" | dTr[,8]=="Barbora Hermannova") 
length(Hermannova)  # [1] 109
H_win = length(which(dTr[,5]=="Barbora Hermannova" | dTr[,6]=="Barbora Hermannova"))
# [1] 46  # Of the 109 matches, 46 are on the winning side.
H_lose = length(which(dTr[,7]=="Barbora Hermannova" | dTr[,8]=="Barbora Hermannova")) 
# [1] 63   # Of the 109 matches, 63 are on the losing side.

Marketa = which(dTr[,5]=="Marketa Slukova" | dTr[,6]=="Marketa Slukova" | dTr[,7]=="Marketa Slukova" | dTr[,8]=="Marketa Slukova") 
length(Marketa)  # [1] 255
M_win = length(which(dTr[,5]=="Marketa Slukova" | dTr[,6]=="Marketa Slukova"))
# [1] 158  # Of the 255 matches, 158 are on the winning side.
M_lose = length(which(dTr[,7]=="Marketa Slukova" | dTr[,8]=="Marketa Slukova")) 
# [1] 97   # Of the 255 matches, 97 are on the losing side.


table_seven = matrix(rep(NA, 3*4), 3, 4)
colnames(table_seven) = c('Hermannova', 'Slukova', 'Toti', 'Giombini')
rownames(table_seven) = c('win', 'lose', 'total')
table_seven[,1] = c(H_win, H_lose, length(Hermannova))
table_seven[,2] = c(M_win, M_lose, length(Marketa))
table_seven[,3] = c(G_win, G_lose, length(giulia))
table_seven[,4] = c(L_win, L_lose, length(laura))
table_seven
print(table_seven)