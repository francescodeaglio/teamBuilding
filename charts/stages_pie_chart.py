import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px

from databases import SinglesDB, CouplesDB, QuartetsDB, OctectsDB


class StagesPieChart:

    def __init__(self, singles_db: SinglesDB, couples_db: CouplesDB, quartets_db: QuartetsDB, octets_db: OctectsDB):
        self.singles_db = singles_db
        self.couples_db = couples_db
        self.quartets_db = quartets_db
        self.octects_db = octets_db
        self.grid = {1: (1, 2), 2: (1, 3), 3: (2, 1), 4: (2, 2), 5: (2, 3)}

    def get_pie_chart_figure(self):

        first = count_partecipants(self.singles_db)
        second = count_partecipants(self.couples_db)
        third = count_partecipants(self.quartets_db)
        fourth = count_partecipants(self.octects_db)

        data = {"singoli": first, "coppie": second, "quartetti": third, "ottetti": fourth}
        df = pd.DataFrame(data).T

        fig = make_subplots(rows=2, cols=3, specs=[[{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}],
                                                   [{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]],
                            subplot_titles=["Tutti"] + [f"   Team <b>{team}" for team in list("12345")]
                            )

        fig.update_layout(title="Conteggio fase per fase", title_x=0.5, title_xanchor="center")

        for i in range(1, 6):
            chart = px.pie(df, values=i, names=df.index, title=f"Squadra **{i}**")
            fig.add_trace(chart.data[0], row=self.grid[i][0], col=self.grid[i][1])

        chart = px.pie(df, values="tot", names=df.index, title=f"Squadra **{i}**")
        fig.add_trace(chart.data[0], row=1, col=1)

        for i in range(6):
            fig.layout["annotations"][i]["x"] -= 0.15

        return fig


def count_partecipants(db):
    active_players = db.get_active_players()
    grouped_teams = [(int(el["squadra"]),
                      len(el["ids"]) if "ids" in el else 1)
                     for el in active_players]

    counter = {int(el): 0 for el in "12345"}
    counter["tot"] = 0
    for team, count in grouped_teams:
        counter[team] += 1
        counter["tot"] += 1
    return counter
