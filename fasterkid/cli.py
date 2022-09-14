__version__ = '0.1.0'

import os
from time import sleep
from .speed import accuracy,get_words,gross_wpm,net_wpm
from .utilities.utils import clear,sleep
from .records.manageRecord import update_user_data,view_records,create_file,view_leaderboard
from datetime import datetime
from rich.console import Console
from rich.align import Align
from rich.panel import Panel

console = Console()

ARTWORK = """

███████╗░█████╗░░██████╗████████╗███████╗██████╗░░░░░░░██╗░░██╗██╗██████╗░
██╔════╝██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗░░░░░░██║░██╔╝██║██╔══██╗
█████╗░░███████║╚█████╗░░░░██║░░░█████╗░░██████╔╝█████╗█████═╝░██║██║░░██║
██╔══╝░░██╔══██║░╚═══██╗░░░██║░░░██╔══╝░░██╔══██╗╚════╝██╔═██╗░██║██║░░██║
██║░░░░░██║░░██║██████╔╝░░░██║░░░███████╗██║░░██║░░░░░░██║░╚██╗██║██████╔╝
╚═╝░░░░░╚═╝░░╚═╝╚═════╝░░░░╚═╝░░░╚══════╝╚═╝░░╚═╝░░░░░░╚═╝░░╚═╝╚═╝╚═════╝░
\n
"""
def ostype()->str:
    return "cls" if os.name == "nt" else "clear"
        

def TypingSpeed(username):
    """Main TypingSpeed function. includes all front-end logic"""

    string = get_words()
    _string = "\u200e ".join(string)  # get string to be displayed, added zero width char to prevent cheating

    console.print(Align("Words:\n    " + _string,align="center"),style="yellow")

    # timer(3)
    sleep(1)
    start_time = datetime.now()
    user_input = input("(¯\_(ツ)_/¯)\t\t\t")
    end_time = datetime.now()
    timetaken = round((end_time - start_time).total_seconds(), 1)  # calc timetaken and round off

    if "\u200e " in user_input:  # anti-cheat
        print("Nice Try but you can't do that here")
        return

    netWPM = net_wpm(user_input, _string, timetaken)
    grossWPM = gross_wpm(user_input, timetaken)
    Accuracy, errors = accuracy(user_input, _string)

    # Print results

    results = f"""
    Net WPM: {netWPM}     Errors: {errors}    Gross WPM: {grossWPM}
    Time Taken: {timetaken}     Accuracy: {Accuracy}%
    """

    data = {'String': ' '.join(string), 'userInput': user_input, 'timeTaken': timetaken, 'netWPM': netWPM,
            'grossWPM': grossWPM, 'Accuracy': Accuracy, 'Error': errors}  # Data to be sent to update_user_data()
    update_user_data(username, data)
    console.print(Align(results + "\n",align="center"),style="green")


def main():
    # Check if records.dat file exists
    if not os.path.exists('history.dat'):
        create_file()

    console.print(Align(ARTWORK,align="center"),style="cyan")
    username = input("Username: ").strip().lower()  # gets username and removes any extra spaces

    scrclear = ostype()
    # Menu-driven program
    while True:
        choice = console.input(Align("   [bold][green] 1.Play [/green]   [yellow]2.View My Stats[/yellow]    [blue]3.Leaderboard[/blue]   [red] 0.Exit [/red][/bold]\n\t",align="center"))
        clear()
        if choice.lower() in ["p", 'play', '1']:
            os.system(scrclear)
            console.print(Align(ARTWORK,align="center"),style="cyan")
            with console.status("Making words... ",spinner="runner"):
                sleep(5)
            TypingSpeed(username)

        elif choice.lower() in ["r", 'records', 'view records', '2']:
            os.system(scrclear)
            console.print(Align(ARTWORK,align="center"),style="cyan")
            view_records(username)
        elif choice.lower().split()[0] in ["l", 'leaderboard', '3']:
            os.system(scrclear)
            console.print(Align(ARTWORK,align="center"),style="cyan")
            try:
                param = choice.lower().split()[1]
                view_leaderboard()
            except IndexError:
                view_leaderboard()

        elif choice.lower() in ["e", 'exit', '0']:
            os.system(scrclear)
            break

