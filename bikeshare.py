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
    print('Hello! Welcome to the US bikeshare data portal. Let\'s explore some data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("\nWhich city would you like to explore the data for? Please choose from Chicago, New York City or Washington.\n").lower()
        if city.lower() not in ('chicago', 'new york city', 'washington'):
            print("Sorry, that option is not valid. Please enter the correct option as listed.")
        else:
            print("Thanks for choosing",city)
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nWhich month would you like to explore the data for? Please choose from January, February, March, April, May, June, or All if you would like to explore all the months.\n").lower()
        if month.lower() not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            print("Sorry, that option is not valid. Please enter the correct option as listed.")
        else:
            print("Thanks for choosing",month)
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nWhich day would you like to explore the data for? Please choose from Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All if you would like to explore all the days.\n").lower()
        if day.lower() not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
            print("Sorry, that option is not valid. Please enter the correct option as listed.")
        else:
            print("Thanks for choosing",day)
            break

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

# load the selected city data file into a pandas dataframe and create relevant date variables
    df = pd.read_csv(CITY_DATA[city])
# convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
# extract month from the Start Time column to create a month column
    df['month'] = df['Start Time'].dt.month
# extract day from the Start Time column to create a day column
    df['day_name'] = df['Start Time'].dt.weekday_name
# extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
# filter by selected month if chosen
    if month.lower() != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
# filter by selected day if chosen
    if day.lower() != 'all':
        df = df[df['day_name'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month1 = df['month'].mode()[0]
    months2 = pd.Series(data = ['january', 'february', 'march', 'april', 'may', 'june'], index = [1,2,3,4,5,6])
    popular_month2 = months2[popular_month1].title()
    print('Based on your selection the most popular month for riding a bike is ',popular_month2)

    # display the most common day of week
    popular_day = df['day_name'].mode()[0]
    print('Based on your selection the most popular day for riding a bike is ',popular_day)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Based on your selection the most popular hour for riding a bike is ',popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_st = df['Start Station'].mode()[0]
    print('Based on your selection the most popular start station is ',popular_start_st)

    # display most commonly used end station
    popular_end_st = df['End Station'].mode()[0]
    print('Based on your selection the most popular end station is ',popular_end_st)

    # display most frequent combination of start station and end station trip
    start_stop_combo = (df['Start Station'] + " to " + df['End Station'])
    frequent_combination = start_stop_combo.mode()[0]
    print('Based on your selection the most popular start and end station combination is ',frequent_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    total_hours = int(total_travel/3600)
    total_days = int(total_travel/86400)
    print('Based on your selection the total travel time across all riders is ',total_travel,' seconds = ',total_hours,' hours = ',total_days,' days.')

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    means_mins = int(mean_travel/60)
    print('Based on your selection the average travel time across all riders is ',int(mean_travel),' seconds = ',means_mins,' minutes.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users. Includes gender and birth year if available in the dataset"""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nThe total number of each type of user is...\n', user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        genders = df['Gender'].value_counts()
        print('\nThe total number of persons of each gender is...\n', genders)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest = df['Birth Year'].min()
        latest = df['Birth Year'].max()
        common = df['Birth Year'].mode()[0]
        print('The earliest year of birth is', int(earliest), 'and the oldest age is', int(2017-earliest), 'years')
        print('The latest year of birth is', int(latest), 'and the youngest age is', int(2017-latest), 'years')
        print('The most common year of birth is', int(common), 'and the most common age is', int(2017-common), 'years')

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def describe_data(df):
    """Displays descriptive statistics about the dataset."""
    print("\nHere are some descriptive statistics about the data you have selected:\n")
    print(df.describe())

def show_data(df):
    """Displays first five rows of data if user says yes and then continuously prompts for five more."""
    start = int(0)
    end = int(5)
    while True:
        show_data = input("\nWould you like to see the first five rows of data? Please enter 'Yes' or 'No'.\n").lower()
        if show_data.lower() not in ('yes', 'no'):
            print("Sorry, that option is not valid. Please enter the correct option as listed.")
        elif show_data.lower() == 'no':
            print("Ok thanks")
            break
        else:
            print(df.iloc[start:end])
            break
    while True:
        show_more = input("\nWould you like to see the next five rows of data? Please enter 'Yes' or 'No'.\n").lower()
        if show_more.lower() not in ('yes', 'no'):
            print("Sorry, that option is not valid. Please enter the correct option as listed.")
        elif show_more.lower() == 'no':
            print("Ok thanks")
            break
        else:
            start = int(start + 5)
            end = int(end + 5)
            print(df.iloc[start:end])


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        describe_data(df)
        show_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
