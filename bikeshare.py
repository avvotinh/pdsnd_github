import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city (chicago, new york city, washington)
    while True:
        city = input("Enter a city (Chicago, New York City, Washington): ").lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid city. Please choose from: Chicago, New York City, Washington.")

    # Get user input for month (all, january, february, ... , june)
    while True:
        month = input("Enter the month you want to filter by (January to June, enter 'all' to view all data): ").lower()
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
        if month in months:
            break
        else:
            print("Invalid month input. Please enter a month between January and June, or 'all'.")

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Enter the day of the week you would like to filter by (enter 'all' to view all data): ").lower()
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
        if day in days:
            break
        else:
            print("Invalid day input. Please enter a valid day of the week, or 'all'.")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load data file into a DataFrame
    df = pd.read_csv(CITY_DATA[city])

    # Convert 'Start Time' and 'End Time' to datetime objects
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # Extract month and day of the week from 'Start Time'
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # Filter by month if applicable
    if month != 'all':
        df = df[df['month'] == month.title()]

    # Filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if not df.empty:
        # Display the most common month
        common_month = df['month'].mode()[0]
        print("The most common month is: ", common_month.title())

        # Display the most common day of week
        common_day = df['day_of_week'].mode()[0]
        print("The most common day of the week is: ", common_day.title())

        # Display the most common start hour
        df['hour'] = df['Start Time'].dt.hour
        common_start_hour = df['hour'].mode()[0]
        print("The most common start hour is: ", common_start_hour)
    else:
        print("No data available for the selected filters.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station is: ", common_start_station)


    # Display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("The most commonly used end station is: ", common_end_station)

    # Display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + ' to ' + df['End Station']
    common_trip = df['trip'].mode()[0]
    print("The most frequent combination of start station and end station trip is: ", common_trip)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("The total travel time is: ", total_travel_time, "seconds")

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("The mean travel time is: ", mean_travel_time, "seconds")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_counts = df['User Type'].value_counts()
    print("Counts of each user type:\n", user_counts)

    # Display counts of gender
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of gender:\n", gender_counts)


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_birth_year = int(df['Birth Year'].min())
        recent_birth_year = int(df['Birth Year'].max())
        common_birth_year = int(df['Birth Year'].mode()[0])
        print("\nEarliest year of birth:", earliest_birth_year)
        print("Most recent year of birth:", recent_birth_year)
        print("Most common year of birth:", common_birth_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Asks the user if they want to see 5 lines of raw data at a time."""
    view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no? ").lower()
    start_loc = 0
    while view_data == 'yes':
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        view_display = input("Do you wish to continue?: ").lower()
        if view_display != 'yes':
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
