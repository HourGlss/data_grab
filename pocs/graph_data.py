import plotly.graph_objects as go

fig = go.Figure()

fig.add_trace(go.Scattermapbox(
    mode="markers+lines",
    lon=[-71.14964250347128, -60, 40],
    lat=[42.34630677574536, 10.6, -20.5],
    marker={'size': 10}))


fig.update_layout(
    margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
    mapbox={
        'center': {'lon': 10, 'lat': 10},
        'style': "stamen-terrain",
        'zoom': 1})

fig.show()
