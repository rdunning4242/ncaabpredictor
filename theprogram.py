import kivy
import pandas as pd
kivy.require("1.9.0")
import theProgramAppFunctions as tpf
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton

"""
The Program App
Ryan Dunning
Version 0.1.0
"""


class TeamListButton(ListItemButton):
    pass

class TeamDB(BoxLayout):
    first_team_text_input = ObjectProperty()
    second_team_text_input = ObjectProperty()
    win_team= ObjectProperty()
    win_chance= ObjectProperty()
    first_score= ObjectProperty()
    second_score= ObjectProperty()
    team_search= ObjectProperty()
    team_list= ObjectProperty()
            
        #Make sure team is selected
        #Put Team Name in Text Box

    def choose_first_team(self):
        if self.team_list.adapter.selection:
            selection = self.team_list.adapter.selection[0].text
            self.first_team_text_input.text= selection
            #self.first_team_scores.text= selection + " Score: "
            
        
    def choose_second_team(self):
        if self.team_list.adapter.selection:
            selection = self.team_list.adapter.selection[0].text
            self.second_team_text_input.text= selection
            #self.second_team_scores.text= selection + " Score: "
    
    def run_program(self):
        all_teams= tpf.GetNCAABTeams()
        first_current_team= tpf.NCAABTeam()
        second_current_team= tpf.NCAABTeam()

        first_current_team.filldata(self.first_team_text_input.text, all_teams)
        second_current_team.filldata(self.second_team_text_input.text, all_teams)
        results= tpf.NCAABSimMatchup(first_current_team, second_current_team, all_teams)
        self.win_team.text= results[0]
        self.win_chance.text= str(results[1]) + "%"
        self.first_score.text= str(results[2])
        self.second_score.text= str(results[3])
        
    def search_for_teams(self):
        for x in range(len(self.team_list.adapter.data)):
            self.team_list.adapter.data.remove(self.team_list.adapter.data[0])
        all_teams= tpf.GetNCAABTeams()
        for x in range(len(all_teams)):
            team_name= all_teams[x]
            if self.team_search.text.lower() in team_name.lower():
                self.team_list.adapter.data.extend([team_name])
        self.team_search.text = ""
        self.team_list._trigger_reset_populate()
    
class ProgramApp(App):
    def build(self):
        return TeamDB()

dbApp = ProgramApp()
dbApp.run()
