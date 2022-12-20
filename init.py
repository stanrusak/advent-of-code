import requests, shutil, os
from sys import argv, exit
from time import sleep
from datetime import datetime, timedelta

def main():

    year = 2022
    day = int(argv[1])

    now = datetime.utcnow() - timedelta(hours=5)
    if now < datetime(year, 12, day, 0, 0, 0):
        exit("Too early!")

    init_files(day)
    data = fetch_input(day, year)

    with open(f"day{day:02}/input.txt", "w") as f:
        f.write(data)

def init_files(day):

    name = f"day{day:02}"

    try:
        os.mkdir(name)
    except FileExistsError:
        exit(f"Error: {name} already exists")
    
    shutil.copy("day00/day00.py", f"{name}/{name}.py")

def fetch_input(day, year):

    url = f"https://adventofcode.com/{year}/day/{day}"

    with open(".session", "r") as f:
        cookie = f.read().strip()

    session = requests.Session()
    session.headers.update({
        "Cookie": f"session={cookie}",
        "User-Agent": "https://github.com/stanrusak/advent-of-code/blob/main/init.py by stanislav.rusak@gmail.com",
        })
    
    retries = 3
    while retries:
        
        response = session.get(url + "/input")
        if response.status_code == 200:
            data = response.text
            print(f"Input preview ({len(data.splitlines())} lines):\n")
            print(data[:200]+"...\n")
            return data
        
        print(f"Couldn't get input ({response.status_code}). Retrying...")
        sleep(2)
        retries -= 1

    exit("Error: couldn't get input")
    
if __name__ == "__main__":

    main()