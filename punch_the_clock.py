# Was brauche ich?

# Einstempeln!
###############
# es kann nur eingestempelt werden, wenn zuvor ausgestempelt wurde
# speichert aktuelle Zeit
# generiert einzigartigen zeitstempel
# generiert einen hash aus diesem zeitstempel um sicherzustellen,
# dass dieser tatsächlich einzigartig ist
# aber vielleicht ist es nicht nötig einen hash wert zu errechnen
# es wird vieles einfacher machen einfach die UNIX zeit im klartext abzuspeichern

# zählt zeit ab einstempelzeitpunkt
# setzt den zustand auf "eingestempelt" oder "aktiv" ...
# ... oder eingestempelt = True
# speichert einstempelzeitpunkt mit in XML datei
# zeitstempel wird ebenfalls in XML datei abgelegt

# Ausstempeln!
###############
# es kann nur ausgestempelt werden, wenn zuvor eingestempelt wurde
# speichert ausstempelzeitpunkt
# generiert einzigartigen zeitstempel
# generiert einen hash aus diesem zeitstempel um sicherzustellen,
# dass dieser tatsächlich einzigartig ist
# aber vielleicht ist es nicht nötig einen hash wert zu errechnen
# es wird vieles einfacher machen einfach die UNIX zeit im klartext abzuspeichern

# stoppt die zeitzählung des einstempelvorgangs
# setzt den "eingestempelt" zustand zurück auf "False"
# speichert ausstempelzeitpunkt mit datum in XML datei
# zeitstempel wird ebenfalls in XML datei abgelegt

# XML Struktur
###############
# <xml>
#     <date day="10" month="12" year="2017">
#         <entry unixtime="47272722" uuid="753692ec36adb4c794c973945e" state="in"/>
#         <entry unixtime="47272722" uuid="0d16219802f027f25d35e207b2" state="out"/>
#     </date>
#     <date day="11" month="12" year="2017">
#         <entry unixtime="49089889" uuid="1b3ad8863d4e11223ff95862b6" state="in"/>
#         <entry unixtime="47272722" uuid="d5adb2bb1c7d6f93b3b1564a26" state="out"/>
#         <entry unixtime="47272722" uuid="2a99c1649703ea6f76bf259abb" state="in"/>
#         <entry unixtime="47272722" uuid="1df5c4b4ab2df41657ac0ae243" state="out"/>
#     </date>
# </xml>


# Zeitüberwachung
###############
# Möglichkeit maximale tägliche Arbeitsstunden einzustellen
# Erinnerung nach Hause zu gehen falls diese Zeit überschritten wurde

# Zusammenfassung
###############
# Export ins csv format (vielleicht)






import threading
from datetime import datetime as dt
import time
import xml.etree.ElementTree as et

def generateTimestamp(Type=""):
    """Generates a Timestamp in either POSIX or human radable format.

    Use "posix" as the argument to get UNIX posix time.
    Leave blank for human readable time. """
    CurrentPosixTime = dt.timestamp(dt.now())
    if Type == "posix":
        Timestamp = CurrentPosixTime
        return Timestamp
    else:
        Timestamp = dt.fromtimestamp(CurrentPosixTime)
        return Timestamp

def startTimeTracking():
    """Starts tracking"""
    timestamp = dt.now()
    return timestamp

def stopTimeTracking():
    """Stops tracking"""
    timestamp = dt.now()
    return timestamp

def printPretty(String):
    """Creates a nice border around a line of text"""
    StringLength = len(String)
    if StringLength > 0:
        print("╔" + "═" * (StringLength + 2) + "╗")
        print("║", String, "║")
        print("╚" + "═" * (StringLength + 2) + "╝")
    else:
        print(String)

def inputPretty(string):
    """Creates a nice border around user input"""
    string_length = len(string)
    if string_length > 0:
        print("╔" + "═" * (string_length + 2) + "╗")
        print("║", string, "║")
        print("╠" + "═" * (string_length + 2) + "╣")
        input_string = input("╠ >> ")
        print("╚" + "═" * (string_length + 2) + "╝")
        return input_string

def printPrettyElapsed(string, timedelta):
    duration = convertTimedelta(timedelta)
    hms = []
    for i in range(0,len(duration)):
        hms.append(str(duration[i]).zfill(2))
    printPretty(string + hms[0] + ":" + hms[1] + ":" + hms[2])

def convertTimedelta(timedelta):
    """Converts timedelta to hours, minutes and seconds. Returns a list"""
    # convert input timedelta to seconds
    passed_seconds = timedelta.total_seconds()

    # divide the total seconds by 60 and save the rest (modulo)
    # this ensures that it won't exceed 60
    remaining_seconds = int(passed_seconds % 60)

    # divide the total seconds by 60 and round down to whole minutes
    full_minutes = int(passed_seconds // 60)

    # divide the whole minutes by 60 and save the rest
    remaining_minutes = int(full_minutes % 60)

    # get the total hours
    hours = int(full_minutes // 60)

    return hours, remaining_minutes, remaining_seconds

def main():
    """Main loop of the program"""
    time_a = None
    time_b = None
    tracking = None
    max_time = None
    # Introduction to the program
    printPretty("Welcome to the Timestamp application.")
    while True:
        print(("═" * 64))
        printPretty("What do you want to do?")
        choice = inputPretty("Punch in/out, duration, quit? (i/o/d/q)")

        # Ask the user what to do
        # He can either start or stop time tracking
        # Additionally he can measure the duration of the tracked time

        # start time tracking if the user enters "i"
        if choice == "i":
            # check if the program is already tracking the users time
            if tracking == False or tracking == None:
                time_a = startTimeTracking()
                tracking = True
                output = "Punched IN: " + time_a.strftime("%d.%m.%Y - %H:%M:%S")
                printPretty(output)
            else:
                # notify the user that he can't start time tracking twice without stopping it once
                printPretty("You already punched in.")
                # ask the user whether he wants to edit the current time
                edit = inputPretty("Do you want to edit/correct the punched in time? (y/n)").lower()
                # if yes, provide interface for editing the time
                if edit == "y":
                    new_time = inputPretty("Enter the new punch in time. (HH:MM:SS)")
                    if ":" in new_time and len(new_time) == 8:
                        new_time = [int(i) for i in new_time.split(":")]
                        # datetime(year, month, day, hour, minute, second)
                        time_a = dt(time_a.year, time_a.month, time_a.day, new_time[0], new_time[1], new_time[2])
                        output = "Punch IN time changed"
                        printPretty(output)
                        output = "Punched IN: " + time_a.strftime("%d.%m.%Y - %H:%M:%S")
                        printPretty(output)
                    else:
                        print("Invalid input.")
                else:
                    output = "Punch IN time unchanged"
                    printPretty(output)
                    output = "Punched IN: " + time_a.strftime("%d.%m.%Y - %H:%M:%S")
                    printPretty(output)
        # stop time tracking if the user wishes to
        elif choice == "o":
            if tracking == True and tracking != None:
                time_b = stopTimeTracking()
                tracking = False
                output = "Punched OUT: " + time_b.strftime("%d.%m.%Y - %H:%M:%S")
                printPretty(output)
            else:
                printPretty("Punch in first.")
        # show duration of already tracked time
        elif choice == "d":
            if time_b != None or time_a != None:
                # if the user already tracks time
                if tracking == True:
                    # show the elapsed time
                    printPrettyElapsed("Currently tracking work: ", dt.now() - time_a)
                else:
                    printPrettyElapsed("Worked for: ", time_b - time_a)
            else:
                printPretty("Punch in and out first.")
        elif choice == "q":
            exit(0)
        else:
            printPretty("Invalid input")

main()
