import random, sys
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup


            
class NCAABTeam:
    def __init__(self):
        self.rank=0
        self.name=""
        self.conf=""
        self.rec=""
        self.adjem= ""
        self.oeff=0
        self.deff=0
        self.tempo=0
    def filldata(self, choice, NCAAB_teams):
        df= pd.read_csv('NCAAB_stats.csv')
        for x in range(len(NCAAB_teams)):
            if choice == NCAAB_teams[x]:
              
              filler= df.Team_Name_name[x]
              self.name=filler
              
              filler= float(df.Team_Name_AdjO[x])
              self.oeff=(round((float(filler)/100),3))
              
              filler= float(df.Team_Name_AdjD[x])
              self.deff=(round((float(filler)/100),3))
              
              filler= float(df.Team_Name_AdjT[x])
              self.tempo=filler
              break
    def filldata2(self, team_data):
        df= pd.read_csv('NCAAB_stats.csv')
        for x in range(len(team_data)):
                if x==0:
                    self.rank= team_data[x].split('<')[0]
                elif x<3:
                    filler= team_data[x].split('>', 1)[1]
                    filler= filler.split('<', 1)[0]
                    if x == 1:
                        self.name= filler
                    else:
                        self.conf= filler
        


def RepresentsInt(s): # Function to make sure user sends an integer, to avoid errors
    try: 
        s=int(s)
        return s
    except ValueError:
        return 0

def NCAABSimMatchup( first_current_team, second_current_team, NCAAB_teams): #Simulates the matchup, nothing changed besides bringing the pace and efficiency in
  
  averages= NCAABLeagueAverages(NCAAB_teams)
  ncaa_average_efficiency= averages[0]
  ncaa_average_pace= averages[1]
  
  first_current_team_seasonpace = first_current_team.tempo
  second_current_team_seasonpace = second_current_team.tempo
  game_pace= ((first_current_team_seasonpace)*(second_current_team_seasonpace))/(ncaa_average_pace)
  
  first_current_team_seasonoffeff = first_current_team.oeff
  second_current_team_seasonoffeff = second_current_team.oeff
  first_current_team_seasondefeff = first_current_team.deff
  second_current_team_seasondefeff = second_current_team.deff
  
  first_current_team_projeff = ((first_current_team_seasonoffeff)*(second_current_team_seasondefeff))/(ncaa_average_efficiency)
  second_current_team_projeff = ((second_current_team_seasonoffeff)*(first_current_team_seasondefeff))/(ncaa_average_efficiency)
  
  first_current_team_score = (game_pace)*(first_current_team_projeff)
  second_current_team_score = (game_pace)*(second_current_team_projeff)
  
  first_current_team_standard_deviation = (4*(game_pace)*((first_current_team_projeff)/2)*(1-((first_current_team_projeff)/2)))**.5
  second_current_team_standard_deviation = (4*(game_pace)*((second_current_team_projeff)/2)*(1-((second_current_team_projeff)/2)))**.5
  
  first_current_team_sims_won=0 
  second_current_team_sims_won = 0
  
  for t in range(10000):
    
    first_current_team_final_score = random.gauss((first_current_team_score), (first_current_team_standard_deviation))
    second_current_team_final_score = random.gauss((second_current_team_score), (second_current_team_standard_deviation))
    
    
    
    
    if first_current_team_final_score > second_current_team_final_score:
      first_current_team_sims_won= (first_current_team_sims_won)+1
    elif first_current_team_final_score < second_current_team_final_score:
      second_current_team_sims_won= (second_current_team_sims_won)+1
    elif first_current_team_final_score == second_current_team_final_score:
      t= t-1
  if first_current_team_sims_won > second_current_team_sims_won:
    winning_team= first_current_team.name
    chance_of_victory= (first_current_team_sims_won)//100
    sim_winner= first_current_team
  elif first_current_team_sims_won < second_current_team_sims_won:
    winning_team= second_current_team.name
    chance_of_victory= (second_current_team_sims_won)//100
    sim_winner= second_current_team
  elif first_current_team_sims_won == second_current_team_sims_won:
    winning_team= "It's Basically a Tossup"
    chance_of_victory = 50
    
      
  return winning_team, chance_of_victory, (first_current_team_score//1), (second_current_team_score//1)

def NCAABLeagueAverages(NCAAB_teams): # Function to return the average values for league efficiency and league tempo
    df= pd.read_csv('ncaab_stats.csv')
    efficiencyAverage=0
    tempoAverage=0
    for s in range(len(NCAAB_teams)):
        try:
            filler= str(df.Team_Name_name[s])
            int(filler)
        except:                        
            filler= float(df.Team_Name_AdjO[s])
            efficiencyAverage+= (round((float(filler)/100),3)) #gets total of offensive efficiency
                                                      
            filler= float(df.Team_Name_AdjD[s])
            efficiencyAverage+= (round((float(filler)/100),3)) #gets total of defensive efficiency
                                                      
            filler= float(df.Team_Name_AdjT[s])
            tempoAverage+= float(filler) #gets total of tempo
        
    efficiencyAverage= (round((efficiencyAverage/702),3))
    tempoAverage= (round((tempoAverage/351),1))
    return efficiencyAverage, tempoAverage

def GetNCAABTeams():
    df= pd.read_csv('ncaab_stats.csv')
    NCAAB_teams=[]
    for x in range(353):
        filler= str(df.Team_Name_name[x])
        NCAAB_teams.append(filler)
    return NCAAB_teams


def scrapeData():
    page_url= "https://kenpom.com/"
    page= urllib.request.urlopen(page_url)
    soup= BeautifulSoup(page, 'html.parser')
    tables= soup.find("table")
    print("ready")
    for row in tables.findAll("tr"):
        empty= True
        team_data=[]
        for column in row.findAll("td"):
            if not column == "":
                empty= False
                moose= str(column)
                moose= moose.split('>', 1)
                moose= moose[1]
                print(moose)
                team_data.append(moose)
        if not empty:
            wait= input()
    print(tables)

