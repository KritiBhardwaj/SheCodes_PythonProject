import json
from datetime import datetime

DEGREE_SYBMOL = u"\N{DEGREE SIGN}C"

def format_temperature(temp):
    """Takes a temperature and returns it in string format with the degrees and celcius symbols.
    
    Args:
        temp: A string representing a temperature.
    Returns:
        A string contain the temperature and "degrees celcius."
    """
    return f"{temp}{DEGREE_SYBMOL}"

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


def calculate_mean(total, num_items):
    """Calculates the mean.
    
    Args:
        total: integer representing the sum of the numbers.
        num_items: integer representing the number of items counted.
    Returns:
        An integer representing the mean of the numbers.
    """
    mean = float(total)/ num_items
    mean = round(mean,1)
    return mean


def process_weather(forecast_file):
    """Converts raw weather data into meaningful text.
    Args:
        forecast_file: A string representing the file path to a file
            containing raw weather data.
    Returns:
        A string containing the processed and formatted weather data.
    """
    with open(forecast_file) as file:
        data = json.load(file)
    
    num_of_days = 0
    minTemps = []
    maxTemps = []
    date_List = []
    output = ""
    outputDaily = ""

    for day in data["DailyForecasts"]:
        num_of_days += 1
        date = convert_date(day['Date'])
        date_List.append(date)

        min_temp = convert_f_to_c(day["Temperature"]["Minimum"]["Value"])
        minTemps.append(min_temp)
        totalMin = sum(minTemps)
        lowestIndex = minTemps.index(min(minTemps))       
        lowest_temp = format_temperature(min(minTemps))
        lowestTempDate = date_List[lowestIndex]
        avgMin = format_temperature(calculate_mean(totalMin, num_of_days))

        max_temp = convert_f_to_c(day["Temperature"]["Maximum"]["Value"])
        maxTemps.append(max_temp)
        totalMax = sum(maxTemps)
        highestIndex = maxTemps.index(max(maxTemps))
        highest_temp = format_temperature(max(maxTemps))
        highestTempDate = date_List[highestIndex]
        avgMax = format_temperature(calculate_mean(totalMax, num_of_days))

        dayDesc = day["Day"]["LongPhrase"]
        dayRainProb = day["Day"]["RainProbability"]
        nightDesc = day["Night"]["LongPhrase"]
        nightRainProb = day["Night"]["RainProbability"]

        min_temp = format_temperature(min_temp)
        max_temp = format_temperature(max_temp)

        line1 = f"\n-------- {date} --------"
        line2 = f"Minimum Temperature: {min_temp}"
        line3 = f"Maximum Temperature: {max_temp}"
        line4 = f"Daytime: {dayDesc}"
        line5 = f"    Chance of rain:  {dayRainProb}%"
        line6 = f"Nighttime: {nightDesc}"
        line7 = f"    Chance of rain:  {nightRainProb}%"
        outputDaily += line1 + "\n" + line2 + "\n" + line3 + "\n" + line4 + "\n" + line5 + "\n" + line6 + "\n" + line7 + "\n"

    output += f"{num_of_days} Day Overview\n\
    The lowest temperature will be {lowest_temp}, and will occur on {lowestTempDate}.\n\
    The highest temperature will be {highest_temp}, and will occur on {highestTempDate}.\n\
    The average low this week is {avgMin}.\n\
    The average high this week is {avgMax}.\n\
    "

    output = output + outputDaily + "\n" +"\n"
    return output

if __name__ == "__main__":
    print(process_weather("data/forecast_5days_a.json"))
