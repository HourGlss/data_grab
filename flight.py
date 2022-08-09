import plotly.graph_objects as go


class Flight:
    uid: str
    lats: list[float]
    longs: list[float]

    def __init__(self, _uid):
        self.uid = _uid
        self.lats = []
        self.longs = []

    def add_coords(self, _lat: float | int, _lon: float | int) -> None:
        # print(f"adding {_lat},{_lon}")
        self.lats.append(float(_lat))
        self.longs.append(float(_lon))

    def get_flight_path(self) -> go.Scattermapbox:
        return go.Scattermapbox(
            mode="markers+lines",
            lon=self.longs,
            lat=self.lats,
            marker={'size': 2})

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        ret = f"{self.uid}\n"
        ret += f'{",".join([str(e) for e in zip(self.lats, self.longs)])}\n'
        return ret
