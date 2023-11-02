from databases import SinglesDB
import pandas as pd
import plotly.express as px


class CountingCharts:

    def __init__(self, singles_db: SinglesDB):
        self.singles_db = singles_db

    def get_counter_player(self):
        active_players = self.singles_db.get_active_players()
        counter = count_visited_stands(active_players)
        data = pd.DataFrame(counter).T
        data["name"] = data.index
        fig = px.bar(data, x="visited_stands", y="name", color="team", orientation='h',
                     title="<b>Stand visitati")
        fig.update_layout(height=1500, title_x=0.5)
        return fig

    def get_counter_stands(self):
        active_players = self.singles_db.get_active_players()
        data = count_stands(active_players)
        data = pd.DataFrame(data)
        data = data.sort_values(by="stand")
        fig = px.bar(data, x="count", y="stand", color="team", orientation='h', title="<b>Stand visitati")
        fig.update_layout(height=500, title_x=0.5)
        return fig


def count_visited_stands(players):
    result = {}
    for player in players:
        count = 0
        for stand in player["stand_visitati"]:
            if player["stand_visitati"][stand]:
                count += 1
        result[player["nomecognome"]] = {
            "visited_stands": count,
            "team": f'{players["squadra"]}'
        }
    return result


def count_stands(players):
    stands = [{"stand": stand, "team": sq, "count": 0} for sq in "12345" for stand in "ABCDEFGHIL"]
    for player in players:
        for stand in player["stand_visitati"]:
            if player["stand_visitati"][stand]:
                for x in stands:
                    if x["team"] == f'{players["squadra"]}' and x["stand"] == stand:
                        x["count"] += 1
    return stands
