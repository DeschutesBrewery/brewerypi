import dash
import pytz
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from datetime import datetime
from dateutil.relativedelta import calendar, relativedelta
from urllib.parse import parse_qs, urlparse
from app.models import EventFrame
from . import refreshButton, refreshInterval

def callback(dashApp):
    refreshInterval.callback(dashApp)
    @dashApp.callback(quickTimeRangePickerCallbackOutputs(),
        quickTimeRangePickerCallbackInputs(),
        [State(component_id = "fromTimestampInput", component_property = "value")])
    def callback(*args, **kwargs):
        return fromToTimestamps(*args, **kwargs)

def eventFrameCallback(dashApp):
    refreshInterval.callback(dashApp)
    @dashApp.callback(quickTimeRangePickerCallbackOutputs(),
        quickTimeRangePickerCallbackInputs(),
        [State(component_id = "fromTimestampInput", component_property = "value"),
        State(component_id = "eventFrameDropdown", component_property = "value")])
    def eventFrameCallback(urlHref, *args, **kwargs):
        timestamps = fromToTimestamps(urlHref, *args[:-1], **kwargs)
        fromTimestamp = timestamps[0]
        toTimestamp = timestamps[1]
        queryString = parse_qs(urlparse(urlHref).query)
        if len(list(filter(lambda property: property["prop_id"] == "url.href", dash.callback_context.triggered))) > 0:
            # url href input fired.
            if "eventFrameId" in queryString:
                eventFrameId = int(queryString["eventFrameId"][0])
                eventFrame = EventFrame.query.get(eventFrameId)
                if eventFrame is not None:
                    fromTimestamp = eventFrame.StartTimestamp.strftime("%Y-%m-%dT%H:%M:%S")
                    if eventFrame.EndTimestamp is not None:
                        # A closed event frame exists so use the end timestamp.
                        toTimestamp = (eventFrame.EndTimestamp + relativedelta(minutes = 1)).strftime("%Y-%m-%dT%H:%M:%S")
        elif len(list(filter(lambda property: property["prop_id"] == "interval.n_intervals", dash.callback_context.triggered))) > 0:
            # interval n_intervals input fired.
            if eventFrameDropdownValue is not None:
                eventFrame = EventFrame.query.get(eventFrameDropdownValue)
                if eventFrame is not None:
                    if eventFrame.EndTimestamp is not None:
                        raise PreventUpdate

        return fromTimestamp, toTimestamp

def fromToTimestamps(urlHref, lastFiveMinutesLiNClicks, lastFifthteenMinutesLiNClicks, lastThirtyMinutesLiNClicks, lastOneHourLiNClicks,
    lastThreeHoursLiNClicks, lastSixHoursLiNClicks, lastTwelveHoursLiNClicks, lastTwentyFourHoursLiNClicks, lastTwoDaysLiNClicks, lastThirtyDaysLiNClicks,
    lastNinetyDaysLiNClicks, lastSixMonthsLiNClicks, lastOneYearLiNClicks, lastTwoYearsLiNClicks, lastFiveYearsLiNClicks, yesterdayLiNClicks,
    lastSevenDaysLiNClicks, dayBeforeYesterdayLiNClicks, thisDayLastWeekLiNClicks, previousWeekLiNClicks, previousMonthLiNClicks, previousYearLiNClicks,
    todayLiNClicks, todaySoFarLiNClicks, thisWeekLiNClicks, thisWeekSoFarLiNClicks, thisMonthLiNClicks, thisMonthSoFarLiNClicks, thisYearLiNClicks,
    thisYearSoFarLiNClicks, intervalNIntervals, fromTimestampInputValue):
    queryString = parse_qs(urlparse(urlHref).query)
    if "localTimezone" in queryString:
        localTimezone = pytz.timezone(queryString["localTimezone"][0])
    else:
        localTimezone = pytz.utc

    utcNow = pytz.utc.localize(datetime.utcnow())
    localNow = utcNow.astimezone(localTimezone)
    today = datetime(localNow.year, localNow.month, localNow.day, 0, 0, 0)
    toTimestamp = localNow
    changedId = [property['prop_id'] for property in dash.callback_context.triggered][0]
    if "lastFiveMinutesLi" in changedId:
        fromTimestamp = localNow - relativedelta(minutes = 5)
    elif "lastFifthteenMinutesLi" in changedId:
        fromTimestamp = localNow - relativedelta(minutes = 15)
    elif "lastThirtyMinutesLi" in changedId:
        fromTimestamp = localNow - relativedelta(minutes = 30)
    elif "lastOneHourLi" in changedId:
        fromTimestamp = localNow - relativedelta(hours = 1)
    elif "lastThreeHoursLi" in changedId:
        fromTimestamp = localNow - relativedelta(hours = 3)
    elif "lastSixHoursLi" in changedId:
        fromTimestamp = localNow - relativedelta(hours = 6)
    elif "lastTwelveHoursLi" in changedId:
        fromTimestamp = localNow - relativedelta(hours = 12)
    elif "lastTwentyFourHoursLi" in changedId:
        fromTimestamp = localNow - relativedelta(hours = 24)
    elif "lastTwoDaysLi" in changedId:
        fromTimestamp = localNow - relativedelta(days = 2)
    elif "lastSevenDaysLi" in changedId:
        fromTimestamp = localNow - relativedelta(days = 7)
    elif "lastThirtyDaysLi" in changedId:
        fromTimestamp = localNow - relativedelta(days = 30)
    elif "lastNinetyDaysLi" in changedId:
        fromTimestamp = localNow - relativedelta(days = 90)
    elif "lastSixMonthsLi" in changedId:
        fromTimestamp = localNow - relativedelta(months = 6)
    elif "lastOneYearLi" in changedId:
        fromTimestamp = localNow - relativedelta(years = 1)
    elif "lastTwoYearsLi" in changedId:
        fromTimestamp = localNow - relativedelta(years = 2)
    elif "lastFiveYearsLi" in changedId:
        fromTimestamp = localNow - relativedelta(years = 5)
    elif "yesterdayLi" in changedId:
        fromTimestamp = today - relativedelta(days = 1)
        toTimestamp = today - relativedelta(seconds = 1)
    elif "dayBeforeYesterdayLi" in changedId:
        fromTimestamp = today - relativedelta(days = 2)
        toTimestamp = today - relativedelta(days = 1) - relativedelta(seconds = 1)
    elif "thisDayLastWeekLi" in changedId:
        fromTimestamp = today - relativedelta(weeks = 1)
        toTimestamp = today - relativedelta(days = 6) - relativedelta(seconds = 1)
    elif "previousWeekLi" in changedId:
        oneWeekAgo = today - relativedelta(weeks = 1)
        twoWeeksAgo = today - relativedelta(weeks = 2)
        fromTimestamp = twoWeeksAgo + relativedelta(weekday = calendar.SUNDAY)
        toTimestamp = oneWeekAgo + relativedelta(weekday = calendar.SUNDAY) - relativedelta(seconds = 1)
    elif "previousMonthLi" in changedId:
        oneMonthAgo = today - relativedelta(months = 1)
        fromTimestamp = datetime(oneMonthAgo.year, oneMonthAgo.month, 1, 0, 0, 0)
        toTimestamp = datetime(today.year, today.month, 1, 0, 0, 0) - relativedelta(seconds = 1)
    elif "previousYearLi" in changedId:
        oneYearAgo = today - relativedelta(years = 1)
        fromTimestamp = datetime(oneYearAgo.year, 1, 1, 0, 0, 0)
        toTimestamp = datetime(today.year, 1, 1, 0, 0, 0) - relativedelta(seconds = 1)
    elif "todayLi" in changedId:
        fromTimestamp = today
        toTimestamp = today + relativedelta(days = 1) - relativedelta(seconds = 1)
    elif "todaySoFarLi" in changedId:
        fromTimestamp = today
    elif "thisWeekLi" in changedId:
        oneWeekAgo = today - relativedelta(weeks = 1)
        fromTimestamp = oneWeekAgo + relativedelta(weekday = calendar.SUNDAY)
        toTimestamp = today + relativedelta(weekday = calendar.SUNDAY) - relativedelta(seconds = 1)
    elif "thisWeekSoFarLi" in changedId:
        oneWeekAgo = today - relativedelta(weeks = 1)
        fromTimestamp = oneWeekAgo + relativedelta(weekday = calendar.SUNDAY)
    elif "thisMonthLi" in changedId:
        fromTimestamp = datetime(today.year, today.month, 1, 0, 0, 0)
        oneMonthAhead = today + relativedelta(months = 1)
        toTimestamp = datetime(oneMonthAhead.year, oneMonthAhead.month, 1, 0, 0, 0) - relativedelta(seconds = 1)
    elif "thisMonthSoFarLi" in changedId:
        fromTimestamp = datetime(today.year, today.month, 1, 0, 0, 0)
    elif "thisYearLi" in changedId:
        fromTimestamp = datetime(today.year, 1, 1, 0, 0, 0)
        oneYearAhead = today + relativedelta(years = 1)
        toTimestamp = datetime(oneYearAhead.year, 1, 1, 0, 0, 0) - relativedelta(seconds = 1)
    elif "thisYearSoFarLi" in changedId:
        fromTimestamp = datetime(today.year, 1, 1, 0, 0, 0)
    elif "interval" in changedId:
        fromTimestamp = datetime.strptime(fromTimestampInputValue, "%Y-%m-%dT%H:%M:%S")
    else:
        fromTimestamp = (localNow - relativedelta(months = 3))

    return fromTimestamp.strftime("%Y-%m-%dT%H:%M:%S"), toTimestamp.strftime("%Y-%m-%dT%H:%M:%S")

def fromToTimestampsLayout():
    return html.Div(className = "btn-group", role = "group", children =
    [
        "From: ", 
        dcc.Input(id = "fromTimestampInput", type = "datetime-local", step = "1"),
        " to: ",
        dcc.Input(id = "toTimestampInput", type = "datetime-local", step = "1")
    ])

def layout():
    return html.Div(children =
    [
        fromToTimestampsLayout(),
        quickTimeRangePickerLayout(),
        refreshButton.layout(),
        refreshInterval.layout()
    ])

def quickTimeRangePickerCallbackInputs():
    return [Input(component_id = "url", component_property = "href"),
        Input(component_id = "lastFiveMinutesLi", component_property = "n_clicks"),
        Input(component_id = "lastFifthteenMinutesLi", component_property = "n_clicks"),
        Input(component_id = "lastThirtyMinutesLi", component_property = "n_clicks"),
        Input(component_id = "lastOneHourLi", component_property = "n_clicks"),
        Input(component_id = "lastThreeHoursLi", component_property = "n_clicks"),
        Input(component_id = "lastSixHoursLi", component_property = "n_clicks"),
        Input(component_id = "lastTwelveHoursLi", component_property = "n_clicks"),
        Input(component_id = "lastTwentyFourHoursLi", component_property = "n_clicks"),
        Input(component_id = "lastTwoDaysLi", component_property = "n_clicks"),
        Input(component_id = "lastSevenDaysLi", component_property = "n_clicks"),
        Input(component_id = "lastThirtyDaysLi", component_property = "n_clicks"),
        Input(component_id = "lastNinetyDaysLi", component_property = "n_clicks"),
        Input(component_id = "lastSixMonthsLi", component_property = "n_clicks"),
        Input(component_id = "lastOneYearLi", component_property = "n_clicks"),
        Input(component_id = "lastTwoYearsLi", component_property = "n_clicks"),
        Input(component_id = "lastFiveYearsLi", component_property = "n_clicks"),
        Input(component_id = "yesterdayLi", component_property = "n_clicks"),
        Input(component_id = "dayBeforeYesterdayLi", component_property = "n_clicks"),
        Input(component_id = "thisDayLastWeekLi", component_property = "n_clicks"),
        Input(component_id = "previousWeekLi", component_property = "n_clicks"),
        Input(component_id = "previousMonthLi", component_property = "n_clicks"),
        Input(component_id = "previousYearLi", component_property = "n_clicks"),
        Input(component_id = "todayLi", component_property = "n_clicks"),
        Input(component_id = "todaySoFarLi", component_property = "n_clicks"),
        Input(component_id = "thisWeekLi", component_property = "n_clicks"),
        Input(component_id = "thisWeekSoFarLi", component_property = "n_clicks"),
        Input(component_id = "thisMonthLi", component_property = "n_clicks"),
        Input(component_id = "thisMonthSoFarLi", component_property = "n_clicks"),
        Input(component_id = "thisYearLi", component_property = "n_clicks"),
        Input(component_id = "thisYearSoFarLi", component_property = "n_clicks"),
        Input(component_id = "interval", component_property = "n_intervals")]

def quickTimeRangePickerCallbackOutputs():
    return [Output(component_id = "fromTimestampInput", component_property = "value"),
        Output(component_id = "toTimestampInput", component_property = "value")]

def quickTimeRangePickerLayout():
    return html.Div(className = "btn-group", role = "group", children =
    [
        html.Button(id = "timestampRangePickerButton", className = "btn btn-default dropdown-toggle btn-sm", **{"data-toggle": "dropdown",
            "aria-haspopup": "true", "aria-expanded": "false"}, children = ["Quick time range"]),
        html.Ul(className = "dropdown-menu", children =
        [
            html.Li(id = "lastFiveMinutesLi", children = html.A("Last 5 minutes")),
            html.Li(id = "lastFifthteenMinutesLi", children = html.A("Last 15 minutes")),
            html.Li(id = "lastThirtyMinutesLi", children = html.A("Last 30 minutes")),
            html.Li(id = "lastOneHourLi", children = html.A("Last 1 hour")),
            html.Li(id = "lastThreeHoursLi", children = html.A("Last 3 hours")),
            html.Li(id = "lastSixHoursLi", children = html.A("Last 6 hours")),
            html.Li(id = "lastTwelveHoursLi", children = html.A("Last 12 hours")),
            html.Li(id = "lastTwentyFourHoursLi", children = html.A("Last 24 hours")),
            html.Li(id = "lastTwoDaysLi", children = html.A("Last 2 days")),
            html.Li(id = "lastSevenDaysLi", children = html.A("Last 7 days")),
            html.Li(id = "lastThirtyDaysLi", children = html.A("Last 30 days")),
            html.Li(id = "lastNinetyDaysLi", children = html.A("Last 90 days")),
            html.Li(id = "lastSixMonthsLi", children = html.A("Last 6 months")),
            html.Li(id = "lastOneYearLi", children = html.A("Last 1 year")),
            html.Li(id = "lastTwoYearsLi", children = html.A("Last 2 years")),
            html.Li(id = "lastFiveYearsLi", children = html.A("Last 5 years")),
            html.Li(id = "yesterdayLi", children = html.A("Yesterday")),
            html.Li(id = "dayBeforeYesterdayLi", children = html.A("Day before yesterday")),
            html.Li(id = "thisDayLastWeekLi", children = html.A("This day last week")),
            html.Li(id = "previousWeekLi", children = html.A("Previous week")),
            html.Li(id = "previousMonthLi", children = html.A("Previous month")),
            html.Li(id = "previousYearLi", children = html.A("Previous year")),
            html.Li(id = "todayLi", children = html.A("Today")),
            html.Li(id = "todaySoFarLi", children = html.A("Today so far")),
            html.Li(id = "thisWeekLi", children = html.A("This week")),
            html.Li(id = "thisWeekSoFarLi", children = html.A("This week so far")),
            html.Li(id = "thisMonthLi", children = html.A("This month")),
            html.Li(id = "thisMonthSoFarLi", children = html.A("This month so far")),
            html.Li(id = "thisYearLi", children = html.A("This year")),
            html.Li(id = "thisYearSoFarLi", children = html.A("This year so far"))
        ])
    ])