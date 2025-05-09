import polars as pl
import plotly.graph_objects as go

def graph_scatter_by_key(
    df: pl.DataFrame,
    x: str,
    y: str,
    x_title = None,
    y_title = '',
    title = '',
    color = None,
    mode = 'lines',
    group_name: str = None,
    options: dict = {},
    fig: go.Figure = None,
    axis = 1,
    theme = 'plotly_dark',
    alt_y_name = None,
):

    # TODO use datafarme interface instead of grabbing data and copying?

    if x_title is None:
        x_title = x

    if fig is None:
        fig = go.Figure()
    
    if alt_y_name is None:
        alt_y_name = y

    y_axis_info = dict(
        title=dict(text=y_title),
        anchor="free",
        overlaying="y",
        autoshift=True,
        side="left"
    )

    if color is not None:
        y_axis_info['color'] = color

    data = dict(
        x = df[x],
        y = df[y],
        name = alt_y_name,
        mode = mode,
        legendgroup = group_name,
        legendgrouptitle_text = group_name,
        **options
    )

    if mode == 'lines':
        data['line'] = dict(color = color)
    elif mode == 'markers':
        data['marker'] = dict(color = color)
    elif mode == 'lines+markers':
        data['line'] = dict(color = color)
        data['marker'] = dict(color = color)
    

    if axis == 1:
        fig.add_trace(go.Scatter(
            **data
        ))
        fig.update_layout(yaxis=dict(title=dict(text=y_title)))
    elif axis == 2:
        fig.add_trace(go.Scatter(
            yaxis='y2',
            **data
        ))
        fig.update_layout(
            yaxis2=y_axis_info,
        )
    elif axis == 3:
        fig.add_trace(go.Scatter(
            yaxis='y3',
            **data
        ))
        fig.update_layout(
            yaxis3=y_axis_info,
        )
    elif axis == 4:
        fig.add_trace(go.Scatter(
            yaxis='y4',
            **data
        ))
        fig.update_layout(
            yaxis4=y_axis_info,
        )

    fig.update_layout(
        title = title,
        template = theme,
        showlegend = True
    )

    return fig

def graph_scatter_all(
    df: pl.DataFrame,
    x: str,
    x_title = None,
    y_title = '',
    title = '',
    mode = 'lines',
    options: dict = {},
    fig: go.Figure = None,
    theme = 'plotly_dark'
):
    if fig is None:
        fig = go.Figure()

    for key in df:
        graph_scatter_by_key(
            df,
            x = x,
            y = key.name,
            x_title = x_title, 
            y_title = y_title,
            title = title,
            mode = mode,
            options = options,
            fig = fig,
            theme = theme
        )

    return fig