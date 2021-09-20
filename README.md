# DFS_ML
Proposal
I will be creating a functional lineup optimizer for NBA daily fantasy sports. This optimizer will take in data from previous season varying from player data to opposing team stats to predict how many fantasy points a player will have per game. The lineup optimizer will have an end result of having the ability to view the lineups as well as export them to DraftKings where you can play them. The optimizer will be using TensorFlow neural networks predict the fantasy points a player will score in a game. I’ll scrap/download the available data from nba, basketball reference and bigdataball.
Tools/Libraries used:
-	The data will be downloaded as an excel file which then will be imported using Pandas to create a dataframe.
-	Tensorflow will be the library used for for creating the neural network and predicting the fantasy points.
-	Sklearn will be used to scale the data and prep for creating the model.
Data
-	www.nba.com/stats 
-	https://rotogrinders.com/resultsdb
-	BigDataBall for the historical DFS data
