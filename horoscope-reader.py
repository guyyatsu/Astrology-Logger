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
              "horoscope.table.txt",
              "horoscope.chart.bmp"           ]

    # Path to executable binary representing astrolog7.60.
    astrolog_command = f"./astrolog-cli/astrolog.exe"

    # TimeDate / Location arguments required for non-interactive mode.
    astrolog_arguments = f"{month} {day} {year} {time} EST 36.07N 79.79W"

    # Flags for the astrolog-cli program; -I -qa is for horoscopes, -qa is for charts.
    astrolog_flags = {
        "interpretation": "-I -qa",
        "table": "-qa",
        "chart": "-Xb -Xo {} -qa",
    }

    # Create the chart directory, if it doesn't exist.
    system(f"mkdir -p {prefix} 2> /dev/null")


    """ Here's where everything before all comes together;
    We have two files, each requiring slightly different alterations of the same command.
    Depending on which file we're working with, we slot the correct arguments into an f-string
    by plugging the unique part of the filename into a dictionary keyed for both of the unique
    filename components.
    """

    ''' Execute the appropriate command for each type of output file. '''
    # Open either of the files at our target directory.
    for file in files:

        target = f"{prefix}/{file}"
        filetype = file.split(".")[1]

        if filetype == "chart":
            flag = astrolog_flags[filetype].format(target)
            execution = f"{astrolog_command} {flag} {astrolog_arguments}"
            command( execution.split() )

        else:
            execution = f"{astrolog_command} {astrolog_flags[filetype]} {astrolog_arguments}"


            with open(target, "w") as output_file:
           
                # Formulate our command; $Binary-File, $$File-DesiredFlags, $DateTime-Location
                command( execution.split(),
                         stdout=output_file )


            ''' Review the results of our command and clean up the file for presentation. '''
            # Read the contents of the file to a local namespace.
            with open(target, "r") as lines: horoscope = lines.read()

            # Slice the file into individual lines, separated by line-breaks.
            edits = horoscope.split("\n")
    
            # NOTE: The first two lines of BOTH filetypes are filler/headers; delete them.
            del edits[0:2]
    
            # Remove any empty lines within the file.
            for line in edits:
                if len(line) == 0:
                    del edits[edits.index(line)]
    
            # Execute file-specific formatting.
            secondary_edits = []
    
    
            # For the `horoscope.table.txt` files;
            if filetype == "table":
                for line in edits:
    
                    line = line.split()
                    if line[1] == ":": del line[1]
                    else: line[0] = line[0].strip(":")
                    secondary_edits.append(" ".join(line))
    
                edits = secondary_edits
    
            # For the `horoscope.interpretation.txt` files;
            if filetype == "interpretation": pass
    
    
            # Re-Write the file with our edits.
            with open(target, "w") as horoscope:
                horoscope.write("\n".join(edits))
    
HoroscopeDaemon()
