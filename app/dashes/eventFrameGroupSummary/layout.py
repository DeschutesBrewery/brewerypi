import dash_core_components as dcc
import dash_html_components as html
import dash_table
from app.dashes.components import collapseExpand, eventFrameGroupDropdown, eventFrameTemplateViewDropdown, refreshButton, refreshInterval

layout = html.Div(children =
[
    html.Div(id = "loadingDiv", className = "text-center", children = [html.Img(src = "/static/images/loading.gif")]),
    dcc.Location(id = "url"),
    dcc.Interval(id = "interval", n_intervals = 0, disabled = True),
    html.Div(id = "dashDiv", style = {"display": "none"}, children =
    [
        html.Div(children =
        [
            refreshButton.layout(),
            refreshInterval.layout()
        ]),
        html.Br(),
        collapseExpand.layout(
        [
            eventFrameGroupDropdown.layout()
        ]),
        dcc.Tabs(id = "tabs"),
        eventFrameTemplateViewDropdown.layout(),
        html.Div(className = "well", children =
        [
            dash_table.DataTable(id = "table", cell_selectable = False, filter_action = "native", sort_action = "native", sort_mode = "multi",
                style_cell = {"whiteSpace": "normal", "height": "auto", "textAlign": "left"},
                style_cell_conditional = [{"if": {"column_id": "Start"}, "width": "175px"}, {"if": {"column_id": "End"}, "width": "175px"}])
        ])
    ])
])
