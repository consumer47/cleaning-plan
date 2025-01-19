import argparse
import random
from collections import defaultdict

from itertools import combinations


def create_combination_of_names(names, team_size):
    """
    Create combinations of names where each combination has the specified team size.

    Args:
        names (list): List of names.
        team_size (int): Size of each team.

    Returns:
        list: List of combinations, each a tuple with the specified team size.
    """
    if team_size < 1:
        raise ValueError("Team size must be at least 1.")

    # Generate all combinations of the given size
    all_combinations = list(combinations(names, team_size))

    return all_combinations


def generate_cleaning_plan(start_date_str, end_date_str, names, team_size, frequency='weekly'):
    from datetime import datetime, timedelta
    from itertools import cycle

    combinations = create_combination_of_names(names, team_size)
    # randomize the combinations:
    combinations_random = random.sample(combinations, len(combinations))
    # Convert string dates to datetime objects
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    # Determine the frequency in terms of days (only considering weekly for now)
    if frequency == 'weekly':
        delta = timedelta(weeks=1)

    current_date = start_date
    schedule = defaultdict(list)

    # Create a circular iterator over names to ensure even distribution
    people_cycle = cycle(names)
    temp = list(people_cycle)
    people_list = list(people_cycle)[:team_size]  # initial team setup
    random.shuffle(people_list)  # randomize to start iterations
    while current_date <= end_date:
        # Form the team
        current_team = people_list[:team_size]
        # Append the team to the schedule
        schedule[current_date.strftime("%Y-%m-%d")] = current_team
        # Shuffle people_list and create next team
        random.shuffle(people_list)
        people_list = people_list[team_size:] + current_team
        # Move the date forward by delta
        current_date += delta
    return schedule


def print_cleaning_plan(schedule):
    print("\nCleaning Schedule:")
    for date, team in schedule.items():
        print(f"{date}: {' & '.join(team)}")


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
        names = args.names.split(',')  # Split comma-separated names
        team_size = args.team_size

    schedule = generate_cleaning_plan(start_date, end_date, names, team_size)
    print_cleaning_plan(schedule)


if __name__ == "__main__":
    main()
