import json
import plotly.express as px
from datetime import datetime

def convert_date(iso_string):
    """Converts and ISO formatted date into a human readable format.   
    Args:
        iso_string: An ISO date string..
    Returns:
        A date formatted like: Weekday Date Month Year
    """
    d = datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%S%z")
    return d.strftime("%A %d %B %Y")

def convert_f_to_c(temp_in_farenheit):
    """Converts an temperature from farenheit to celcius
    Args:
        temp_in_farenheit: integer representing a temperature.
    Returns:
        An integer representing a temperature in degrees celcius.
    """
    temp_in_farenheit = float(temp_in_farenheit)
    temp_in_celcius = round((temp_in_farenheit - 32) * (5/9),1)
    return temp_in_celcius

def process_weather(forecast_file):
    """Converts raw weather data into meaningful text.
    Args:
        forecast_file: A string representing the file path to a file
            containing raw weather data.
    Returns:
        A string containing the processed and formatted weather data.
    """

    min_temps = []
    max_temps = []
    min_realFeel_temps = []
    min_realFeelShade_temps = []
    dates = []
    graph_data = {}

    with open(forecast_file) as file:
        data = json.load(file)

    for day in data["DailyForecasts"]:
        min_temp = convert_f_to_c(day["Temperature"]["Minimum"]["Value"])
        min_temps.append(min_temp)
        
        max_temp = convert_f_to_c(day["Temperature"]["Maximum"]["Value"])
        max_temps.append(max_temp)

        min_realFeel_temp = convert_f_to_c(day["RealFeelTemperature"]["Minimum"]["Value"])
        min_realFeel_temps.append(min_realFeel_temp)
        
        min_realFeelShade_temp = convert_f_to_c(day["RealFeelTemperatureShade"]["Maximum"]["Value"])
        min_realFeelShade_temps.append(min_realFeelShade_temp)

        date = convert_date(day['Date'])
        dates.append(date)

    print(min_temps)
    print(max_temps)
    print(min_realFeel_temps)
    print(min_realFeelShade_temps)
    print(dates)

    # df = {
    # "our_data": [123, 567, 435, 345, 678, 900, 345, 233],
    # "more_data": [23, 45, 12, 34, 45, 56, 34, 56],
    # "columns": ["a", "b", "c", "d", "e", "f", "g", "h"]
    # }    
    
    graph_1_data = {
    "mins" : min_temps,
    "maxs" : max_temps,
    "dates": dates,
    }
    
    graph_2_data = {
    "mins" : min_temps,
    "min_realFeel_temps" : min_realFeel_temps,
    "min_realFeelShade_temps": min_realFeelShade_temps,
    "dates": dates
    }

    fig_1 = px.line(
        graph_1_data, 
        y = ["mins", "maxs"],
        x = "dates"
    )

    fig_2 = px.line(
        graph_2_data, 
        y = ["mins", "min_realFeel_temps", "min_realFeelShade_temps"],
        x = "dates"
    )

    return fig_1.show(), fig_2.show()

if __name__ == "__main__":
    print(process_weather("data/forecast_5days_a.json"))
