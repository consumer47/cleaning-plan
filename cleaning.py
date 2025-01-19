import argparse
import random
from collections import defaultdict
from itertools import combinations, cycle
from datetime import datetime, timedelta
from ics import Calendar, Event


def create_combination_of_names(names, team_size):
    if team_size < 1:
        raise ValueError("Team size must be at least 1.")
    return list(combinations(names, team_size))


def generate_cleaning_plan(start_date_str, end_date_str, names, team_size, frequency='weekly'):
    combinations = create_combination_of_names(names, team_size)
    combinations_random = random.sample(combinations, len(combinations))

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    delta = timedelta(weeks=1) if frequency == 'weekly' else timedelta(days=1)

    current_date = start_date
    schedule = defaultdict(list)
    combinations_cycle = cycle(combinations_random)

    while current_date <= end_date:
        current_team = next(combinations_cycle)
        schedule[current_date.strftime("%Y-%m-%d")] = current_team
        current_date += delta

    return schedule


def print_cleaning_plan(schedule):
    print("\nCleaning Schedule:")
    for date, team in schedule.items():
        print(f"{date}: {' & '.join(team)}")


def create_calendar_files(schedule, names):
    # Ensure output directory exists
    import os
    os.makedirs('output', exist_ok=True)

    # Calendar for all members
    all_calendar = Calendar()
    for date_str, team in schedule.items():
        event = Event()
        event.name = 'Clean! ' + ', '.join(team) 
        date = datetime.strptime(date_str, "%Y-%m-%d")
        event.begin = date.replace(hour=13, minute=0)  # Set time to 13:00
        event.duration = timedelta(hours=1)
        event.description = f"Team: {', '.join(team)}"
        all_calendar.events.add(event)

    with open('output/all_people.ics', 'w') as f:
        f.writelines(all_calendar)

    # Separate calendars for each individual
    for name in names:
        personal_calendar = Calendar()
        for date_str, team in schedule.items():
            if name in team:
                event = Event()
                event.name = 'Clean! ' + ', '.join(team) 
                date = datetime.strptime(date_str, "%Y-%m-%d")
                event.begin = date.replace(
                    hour=13, minute=0)  # Set time to 13:00
                event.duration = timedelta(hours=1)
                event.description = f"Team: {', '.join(team)}"
                personal_calendar.events.add(event)

        filename = f'output/{name.strip()}.ics'
        with open(filename, 'w') as f:
            f.writelines(personal_calendar)


def interactive_input():
    print("Interactive Mode: Please provide the following details.")
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    names = input(
        "Enter the names of people in the flat, separated by commas: ").split(',')
    team_size = int(input("Enter the team size: "))

    return start_date, end_date, names, team_size


def main():
    parser = argparse.ArgumentParser(
        description="Generate a weekly cleaning plan for shared flats.")
    parser.add_argument('--start-date', type=str, required=True,
                        help='Start date in YYYY-MM-DD format.')
    parser.add_argument('--end-date', type=str, required=True,
                        help='End date in YYYY-MM-DD format.')
    parser.add_argument('--names', type=str, required=True,
                        help='Comma-separated list of names for people in the flat.')
    parser.add_argument('--team-size', type=int, required=True,
                        help='How many people a team consists of.')

    args = parser.parse_args()

    if not args.start_date or not args.end_date or not args.names or not args.team_size:
        print("Some arguments are missing, switching to interactive mode.")
        start_date, end_date, names, team_size = interactive_input()
    else:
        start_date = args.start_date
        end_date = args.end_date
        names = args.names.split(',')
        team_size = args.team_size

    schedule = generate_cleaning_plan(start_date, end_date, names, team_size)
    print_cleaning_plan(schedule)
    create_calendar_files(schedule, names)


if __name__ == "__main__":
    main()
