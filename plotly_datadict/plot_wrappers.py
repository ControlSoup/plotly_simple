import numpy as np
import plotly.graph_objects as go


def graph_by_key(
    datadict: str,
    key_list: list[str],
    x_key: str,
    title: str = "",
    yaxis_num: int = 1,
    yaxis_title: str = "",
    show_fig: bool = False,
    export_path: bool = None,
    fig: go.Figure = None,
    log_x: bool =False,
    color: str  = None,
) -> go.Figure:

    if fig == None:
        fig = go.Figure()

    yaxis = None
    if 1 <= yaxis_num <= 4:
        yaxis = f'y{yaxis_num}' if yaxis_num > 1 else None
    else:
        raise ValueError(
            f"Cannot set axis number [{yaxis_num}]; use 1, 2, 3, or 4"
        )


    print(yaxis)
    for y_key in key_list:
        fig.add_trace(
            go.Scatter(
                x=datadict[x_key],
                y=datadict[y_key],
                name=y_key,
                yaxis=yaxis,
                mode="lines",
                fill = color
            )
        )

    fig.update_layout(
        title=title, 
        xaxis_title=x_key
    )

    yaxis_str = f'yaxis{yaxis_num}' if yaxis_num > 1 else 'yaxis'
    fig.update_layout({
        yaxis_str: dict(
            title=dict(text=yaxis_title),
            anchor="x" if yaxis_num == 1 else "free",
            overlaying="y" if yaxis_num > 1 else None,
            side="left" if yaxis_num % 2 != 0 else "right",
        )
    })
        

    if log_x:
        fig.update_layout(_xaxis_type="log")

    if show_fig:
        fig.show()

    if export_path:
        fig.write_html(export_path)

    return fig


def graph_datadict(
    datadict: str,
    x_key: str,
    title: str = "",
    yaxis_num: int = 1,
    yaxis_title: str = "",
    show_fig: bool = False,
    export_path: bool = None,
    fig: go.Figure = None,
    log_x: bool =False,
    color: str  = None,
) -> go.Figure:
    key_list = [key for key in datadict if key != x_key]

    return graph_by_key(
        datadict = datadict,
        x_key = x_key,
        key_list=key_list,
        title = title,
        yaxis_num = yaxis_num,
        yaxis_title = yaxis_title,
        show_fig = show_fig,
        export_path = export_path,
        fig = fig,
        log_x = log_x,
        color = color,
    )

