import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

months = [x.lower() for x in list(calendar.month_name)[1:]]
months.append('all')

days = [x.lower() for x in list(calendar.day_name)[1:]]
days.append('all')


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city = month = day = None
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input(f'chose a city in: {[x for x in CITY_DATA.keys()]}\n').lower()
        if city not in [x for x in CITY_DATA.keys()]:
            print(f'city is not a valid choice, try again')
            continue
        break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input(f'chose a month in: {months}\n').lower()
        if month not in months:
            print(f'{month} is not a valid choice, try again')
            continue
        break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input(f'chose a day in: {days}\n').lower()
        if day not in days:
            print(f'{day} is not a valid choice, try again')
            continue
        break

    print('-' * 40)

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
    filename = CITY_DATA[f'{city}']

    df = pd.read_csv(filename)

    df.rename(columns={
        'Unnamed: 0': 'Trip Id',
    },inplace=True)

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Month Name'] = df['Start Time'].dt.month_name().str.lower()
    df['Day Name'] = df['Start Time'].dt.day_name().str.lower()
    df['Start Hour'] = df['Start Time'].dt.hour
    if 'Gender' not in df.columns:
        df['Gender'] = None
    if 'Birth Year' not in df.columns:
        df['Birth Year'] = None
    if month != 'all':
        df = df[df['Month Name'] == month].copy()
    if day != 'all':
        df = df[df['Day Name'] == day].copy()

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('the most common month\n',df[['Month Name']].mode().values)

    # display the most common day of week
    print('the most common day of week\n',df[['Day Name']].mode().values)

    # display the most common start hour
    print('the most common start hour\n',df[['Start Hour']].mode().values)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    df['Station Combination'] = df['Start Station'] + ' to ' + df['End Station']

    # display most commonly used start station
    print('most commonly used start station\n', df[['Start Station']].mode().values)

    # display most commonly used end station
    print('most commonly used end station\n', df[['End Station']].mode().values)

    # display most frequent combination of start station and end station trip
    print('most frequent combination of start station and end station trip\n', df[['Station Combination']].mode().values)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')

    start_time = time.time()

    # display total travel time
    print('display total travel time\n', df[['Trip Duration']].sum())

    # display mean travel time
    print('display mean travel time\n', df[['Trip Duration']].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    df1 = df[['Trip Id','User Type','User Type']].copy()
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('counts of user types\n', df[['Trip Id', 'User Type']].groupby(df['User Type']).count().iloc[:, 0])

    # Display counts of gender
    print('counts of gender\n', df[['Trip Id', 'Gender']].groupby(df['Gender']).count().iloc[:, 0])

    # Display earliest, most recent, and most common year of birth

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
