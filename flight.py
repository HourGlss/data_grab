import plotly.graph_objects as go


class Flight:

    def __init__(self, _uid):
        self.uid = _uid
        self.lats = []
        self.longs = []

    def add_coords(self, _lat, _lon):
        # print(f"adding {_lat},{_lon}")
        self.lats.append(float(_lat))
        self.longs.append(float(_lon))

    def get_flight_path(self):
        return go.Scattermapbox(
            mode="markers+lines",
            lon=self.longs,
            lat=self.lats,
            marker={'size': 2})
