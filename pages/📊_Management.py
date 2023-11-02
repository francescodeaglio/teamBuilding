import streamlit as st

from charts.active_players_message import ActivePlayersMessage
from charts.counting_charts import CountingCharts
from charts.player_search import PlayerSearch
from charts.stages_pie_chart import StagesPieChart
from databases.mongo_handler import MongoHandler

mongo_handler = MongoHandler()


def __main__():
    c1, c2 = st.columns((0.865, 0.135))
    c1.markdown("## Management page")
    c2.text("\n")

    if c2.button("Aggiorna"):
        st.rerun()

    with st.expander("Conteggio fase per fase"):
        pie_chart = StagesPieChart(mongo_handler.singles_db,
                                   mongo_handler.couples_db,
                                   mongo_handler.quartets_db,
                                   mongo_handler.octets_db)
        st.plotly_chart(pie_chart.get_pie_chart_figure())

    with st.expander("Ricerca partecipante"):
        search = PlayerSearch(mongo_handler.singles_db,
                              mongo_handler.couples_db,
                              mongo_handler.quartets_db,
                              mongo_handler.octets_db)
        search.show()

    st.markdown("### Prima Fase")
    counting_charts = CountingCharts(mongo_handler.singles_db)
    with st.expander("Progressi Individui"):
        fig = counting_charts.get_counter_player()
        st.plotly_chart(fig)
    with st.expander("Progressi Stand"):
        fig = counting_charts.get_counter_stands()
        st.plotly_chart(fig)

    st.markdown("### Seconda fase")
    messages = ActivePlayersMessage(mongo_handler.singles_db,
                                    mongo_handler.couples_db,
                                    mongo_handler.quartets_db,
                                    mongo_handler.octets_db)
    with st.expander("Awaiting"):
        messages.show_awaiting()

    st.markdown("### Terza fase")
    with st.expander("Attivi"):
        messages.show_active_third()
    st.markdown("### Quarta fase")
    with st.expander("Attivi"):
        messages.show_active_fourth()


if __name__ == "__main__":
    __main__()
