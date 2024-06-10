import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
   
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    # get user input for city (chicago, new york city, washington).
    print('Would you like to see data for Chicago, New York, or Washington?')
    city = input().lower()

    # Check valid City input
    while city not in CITY_DATA.keys():
        print('\nInvalid Input. Please choose Chicago, New York, or Washington (Case Incensitive)')
        city = input().lower()
    
    print('\nYou have selected', city.title())

    # get user input for month (all, january, february, ... , june)
    print('Would you like to filter data by month? Enter "Y" or "N"')
    month_filter = input().lower()
     # Check for Valid month_filter input
    while month_filter not in ['y','n']:
        print('\nInvalid Input. Please enter "Y" for Yes and "N" for No')
        month_filter = input().lower()
    if month_filter == 'n':
        month = 'all'
    elif month_filter == 'y':
        # Collect user input for month
        print('\nPlease select a Month to filter. Data is available for January-June.')
        month = input().lower()
        # Check for valid Month input
        while month not in MONTHS:
            print('\nInvalid Input. Please choose a month between January and June. You may also type "all" to select all months.')
            month = input().lower()
    else:
        print('\nInvalid Input.')

    print('\nYou have selected', month.title())

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print('Would you like to filter data by Day of the Week? Please enter "Y" for Yes and "N" for No' )
    day_filter = input().lower()
    # Check for Valid day_filter input
    while day_filter not in ['y','n']:
        print('\nInvalid Input. Please enter "Y" for Yes and "N" for No')
        day_filter = input().lower()
    if day_filter == 'n':
        day = 'all'
    elif day_filter == 'y':
        # Collect user input for Day
        print('\nPlease select a Day (Monday-Sunday) to filter.')
        day = input().lower()
        # Check for valid Day input
        while day not in DAYS:
            print('\nInvalid Input. Please input a Day of the Week. You may also type "all" to select all days.')
            day = input().lower()
    else:
        print('\nInvalid Input.')

    print('\nYou have selected', day.title())

    print('-'*40)
    return city, month, day

def load_data(city):

    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        
    Returns:
        df - Pandas DataFrame containing city data
    """

    # Load City Data
    df = pd.read_csv(CITY_DATA[city])

    return df

def apply_filters(month, day, df):

    """
    Applies Filters specififed in get_filters function

    Args:
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        df - Pandas DataFrame containing city data
        
    Returns:
        df - Pandas DataFrame containing filtered city data
    """

    # Change Start Time column type
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Create Month and Day Column
    df['month'] = df['Start Time'].dt.month
    df['weekday'] = df['Start Time'].dt.weekday

    # Apply Month Filter
    if month != 'all':
        month_num = MONTHS.index(month) + 1
        df = df[df['month'] == month_num]

    # Apply Day Filter
    if day != 'all':
        day_num = DAYS.index(day)
        df = df[df['weekday'] == day_num]

    return df

def view_data(df):

    """
    Allows User to view a sample of the filtered data set

    Args: 
        df - Pandas DataFrame containing filtered city data
    """
    row = 0
    next = 'y'
    max = len(df)
    while next != 'n':
        print(df[row:row+5])
        row = row + 5
        
        # Break function at end of data set
        if row > max:
            print('\n End of Data Frame')
            break

        # Get User input if they would like to continue
        print('\nWould you like to view the next 5 rows? Type "Y" for Yes and "N" for No')
        next = input().lower()

        # Check for valid user input
        while next not in ['y','n']:
            print('\nInvalid Input. Please enter Y or N.')
            next = input().lower()
    
    print('-'*40)

def check_filters(city, month, day):

    """
    Allows user to check city, month, and day values

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nCurrent Filters:\nCity:', city.title(), '\nMonth:', month.title(), '\nWeekday:', day.title())
    
    print('-'*40)
    
def time_stats(df):
   
    """
    Displays statistics on the most frequent times of travel.
    
    Args:
        df - Pandas DataFrame containing filtered city data
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Get most frequent month
    frequent_month = df['month'].mode()[0]
    month = MONTHS[frequent_month - 1]
    print('Most frequently traveled Month:' , month.title())

    #Get most frequent day
    frequent_day = df['weekday'].mode()[0]
    day = DAYS[frequent_day]
    print('Most frequently traveled weekday:', day.title())

    # Get performance statistics
    print("\nThis took %s seconds." % (time.time() - start_time))
    
    print('-'*40)

def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    
    Args:
        df - Pandas DataFrame containing filtered city data
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    frequent_start = df['Start Station'].mode()[0]
    print('Most frequent Start Station:', frequent_start)

    # display most commonly used end station
    frequent_end = df['End Station'].mode()[0]
    print('Most frequent End Station:', frequent_end)

    # display most frequent combination of start station and end station trip
    df['Route'] = df['Start Station'] + ' to ' + df['End Station']
    frequent_route = df['Route'].mode()[0]
    print('Most frequent Route:', frequent_route)

    # Get performance statistics
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    
    Args - 
        df - Pandas DataFrame containing filtered city data
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print('Total Trip Time:', total_time, 'seconds')

    # display mean travel time
    avg_time = round(df['Trip Duration'].mean())
    print('Average Trip Time:', avg_time, 'seconds')

    # Get performance statistics
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(city, df):
    
    """
    Displays statistics on bikeshare users.
    
    Args - 
        (str) city - name of the city to analyze
        df - Pandas DataFrame containing filtered city data
    """
    
    # No users stats if Washington filter is selected
    if city == 'washington':
        print('\nUser Data not available for Washington')
    else:
        print('\nCalculating User Stats...\n')
        start_time = time.time()

        # Display counts of user types
        user_type_count = df['User Type'].value_counts()
        print('Count of Users by Type:\n', user_type_count)

        # Display counts of gender
        gender_count = df['Gender'].value_counts()
        print('\nCount of Users by Gender:\n', gender_count)

        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = round(df['Birth Year'].min())
        recent_birth_year = round(df['Birth Year'].max())
        common_birth_year = round(df['Birth Year'].mode()[0])
        print('\nEarliest Birth Year:', earliest_birth_year)
        print('Most Recent Birth Year:', recent_birth_year)
        print('Most Common Birth Year:', common_birth_year)

        print("\nThis took %s seconds." % (time.time() - start_time))
    
    print('-'*40)

def main():

    """Main Function that runs the program"""

    print('Hello! Let\'s explore some US bikeshare data!')
    city, month, day = get_filters()
    df = load_data(city)
    df = apply_filters(month, day, df)

    # Run functions based on user input
    command = ''
    while command != 'esc':
        print('\nType "m" for menu.')
        command = input().lower()
        if command == 'm':
            print('\nTo view a sample of the data frame, type "df"\nTo view current filters, type "Filters"\nTo view Time stats, type "Time"\nTo view station stats, type "station"\nTo view trip duration stats, type "Trip"\nTo view User stats, type "User"\nTo exit the program, type "esc"')
            print('-'*40)
        elif command == 'filters':
            check_filters(city, month, day)
        elif command == 'df':
            view_data(df)
        elif command == 'time':
            time_stats(df)
        elif command == 'station':
            station_stats(df)
        elif command == 'trip':
            trip_duration_stats(df)
        elif command == 'user':
            user_stats(city, df)
        elif command == 'esc':
            print('\nClosing Program...\n')
        else:
            print('\nInvalid Input')

main()