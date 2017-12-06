# Was brauche ich?

# Einstempeln!
###############
# es kann nur eingestempelt werden, wenn zuvor ausgestempelt wurde
# speichert aktuelle Zeit
# zählt zeit ab einstempelzeitpunkt
# setzt den zustand auf "eingestempelt" oder "aktiv" ...
# ... oder eingestempelt = True
# speichert einstempelzeitpunkt mit datum in XML datei

# Ausstempeln!
###############
# es kann nur ausgestempelt werden, wenn zuvor eingestempelt wurde
# speichert ausstempelzeitpunkt
# stoppt die zeitzählung des einstempelvorgangs
# setzt den "eingestempelt" zustand zurück auf "False"
# speichert ausstempelzeitpunkt mit datum in XML datei

# Zeitüberwachung
###############
# Möglichkeit maximale tägliche Arbeitsstunden einzustellen
# Erinnerung nach Hause zu gehen falls diese Zeit überschritten wurde

# Zusammenfassung
###############
# Export ins csv format
import threading
import datetime
import time

def punch_in():
    """Starts tracking"""
    timestamp = datetime.datetime.now()
    return timestamp

def punch_out():
    """Stops tracking"""
    timestamp = datetime.datetime.now()
    return timestamp

def printPretty(string):
    """Creates a nice border around a line of text"""
    string_length = len(string)
    if string_length > 0:
        print("╔" + "═" * (string_length + 2) + "╗")
        print("║", string, "║")
        print("╚" + "═" * (string_length + 2) + "╝")
    else:
        print(string)

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
    printPretty("Welcome to the Timestamp application.")
    while True:
        print(("═" * 64))
        printPretty("What do you want to do?")
        choice = inputPretty("Punch in/out, duration? (i/o/d)")

        if choice == "i":
            if tracking == False or tracking == None:
                time_a = punch_in()
                tracking = True
                output = "Punched IN: " + time_a.strftime("%d.%m.%Y - %H:%M:%S")
                printPretty(output)
            else:
                printPretty("You already punched in.")
                edit = inputPretty("Do you want to edit/correct the punched in time? (y/n)").lower()
                if edit == "y":
                    new_time = inputPretty("Enter the new punch in time. (HH:MM:SS)")
                    if ":" in new_time and len(new_time) == 8:
                        new_time = [int(i) for i in new_time.split(":")]
                        # datetime(year, month, day, hour, minute, second)
                        time_a = datetime.datetime(time_a.year, time_a.month, time_a.day, new_time[0], new_time[1], new_time[2])
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
        elif choice == "o":
            if tracking == True and tracking != None:
                time_b = punch_out()
                tracking = False
                output = "Punched OUT: " + time_b.strftime("%d.%m.%Y - %H:%M:%S")
                printPretty(output)
            else:
                printPretty("Punch in first.")
        elif choice == "d":
            if time_b != None and time_a != None:
                if tracking == True:
                    printPretty("Stop tracking first to stop measuring the time.")
                else:
                    hours = convertTimedelta(time_b - time_a)[0]
                    s_hours = str(hours).zfill(2)
                    minutes = convertTimedelta(time_b - time_a)[1]
                    s_minutes = str(minutes).zfill(2)
                    seconds = convertTimedelta(time_b - time_a)[2]
                    s_seconds = str(seconds).zfill(2)
                    printPretty("Worked for " + s_hours + ":" + s_minutes + ":" + s_seconds)
            else:
                printPretty("Punch in and out first.")
        else:
            printPretty("Invalid input")

main()
