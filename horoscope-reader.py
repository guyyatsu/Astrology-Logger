from subprocess import run as command
from os import system
from datetime import datetime


def HoroscopeDaemon(outputBasePath: str="./charts"):

    # Datetime objects; for setting the current date down to the minute.
    today = datetime.now(); year = today.year; month = today.month; day = today.day
    hour = today.hour; minute = today.minute; time = f"{hour}:{minute}"

    # Target directory for outputting result text.
    prefix = f"{outputBasePath}/{year}/{month}/{day}"

    # Filenames for containing results.
    files = [ "horoscope.interpretation.txt", 
              "horoscope.chart.txt"           ]

    # Path to executable binary representing astrolog7.60.
    astrolog_command = f"./astrolog-cli/astrolog.exe"

    # TimeDate / Location arguments required for non-interactive mode.
    astrolog_arguments = f"{month} {day} {year} {time} EST 36.07N 79.79W"

    # Flags for the astrolog-cli program; -I -qa is for horoscopes, -qa is for charts.
    astrolog_flags = {
        "interpretation": "-I -qa",
        "chart": "-qa"
    }


    system(f"mkdir -p {prefix} 2> /dev/null")

    for file in files:
        with open(file, "w") as output_file:
            
            execution = f"{astrolog_command} {astrolog_flags[file.split('.')[2]]} {astrolog_arguments}"
            print(execution)
            command( execution.split(),
                     stdout=output_file )
            

    for file in files:
        with open(file, "r") as lines:
            horoscope = lines.read()

        edits = horoscope.split("\n")
        del edits[0:2]
        for line in edits:
            if len(line) == 0:
                del edits[edits.index(line)]

        with open(file, "w") as horoscope:
            horoscope.write("\n".join(edits))

HoroscopeDaemon()
