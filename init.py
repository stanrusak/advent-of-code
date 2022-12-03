import requests, shutil, os
from sys import argv

def main():

    year = 2022
    day = int(argv[1])

    init_files(day)
    fetch_input(day, year)

def init_files(day):

    n = f"{day:02}"
    print(n)
    os.mkdir(f"day{n}")
    shutil.copy("day00/day00.py", f"day{n}/day{n}.py")

def fetch_input(day, year):

    url = f"https://adventofcode.com/{year}/day/{day}"

    with open(".session", "r") as f:
        cookie = f.read().strip()

    session = requests.Session()
    session.headers.update({"Cookie": f"session={cookie}"})
    data = session.get(url + "/input", ).text
    
    with open(f"day{day:02}/input.txt", "w") as f:
        f.write(data)

if __name__ == "__main__":

    main()