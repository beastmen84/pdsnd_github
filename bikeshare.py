import time
import pandas as pd

# GLOBAL VARIABLES
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
error_message = '{} is not a valid input. Please try again.\n'


def get_user_data(valid_items_list, prompt, error_msg):
    """Used to simplify the get_filters() function"""
    correct_input = False
    while not correct_input:
        user_input = (input(prompt))
        if user_input.lower() not in valid_items_list:
            print(error_msg.format(user_input))
        else:
            return user_input.lower()


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by,
        or "all" to apply no month filter
        (str) day - name of the day of week to filter by,
        or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # Get user input for the city
    city_prompt = ('Enter the city you would like to analyze data for;\n'
                   'VALID INPUTS ARE: Chicago, New York City, Washington\n')
    valid_cities = ['chicago', 'new york city', 'washington']
    city = get_user_data(valid_cities, city_prompt, error_message)
    # Get user input for the month
    month_prompt = ('\nSpecify the month you would like to analyze data for;\n'
                    'VALID INPUTS ARE: All or January, February, March, April, '
                    'May, June\n')
    valid_months = ['all', 'january', 'february', 'march',
                    'april', 'may', 'june']
    month = get_user_data(valid_months, month_prompt, error_message)
    # Get user input for the day
    day_prompt = ('\nSpecify the day you would like to analyze data for;\n'
                  'VALID INPUTS ARE: All or Monday, Tuesday, Wednesday, '
                  'Thursday, Friday, Saturday, Sunday\n')
    valid_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday',
                  'friday', 'saturday', 'sunday']
    day = get_user_data(valid_days, day_prompt, error_message)
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city
    and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by,
        or "all" to apply no month filter
        (str) day - name of the day of week to filter by,
        or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    start_time_column = 'Start Time'
    df = pd.read_csv(CITY_DATA[city])
    df[start_time_column] = pd.to_datetime(df[start_time_column])
    df['month'] = df[start_time_column].dt.month_name()
    df['day_of_week'] = df[start_time_column].dt.day_name()
    df['hour'] = df[start_time_column].dt.hour
    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month'] == month.title()]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        print('The most common month is {}'
              .format(df['month'].mode()[0]))

    # display the most common day of week
    if day == 'all':
        print('The most common day of week is {}'
              .format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    print('The most common start hour is {}\n'
          .format(df['hour'].mode()[0]))

    print("This took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station is {}'
          .format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('The most commonly used end station is {}'
          .format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    station_combo = df[['Start Station', 'End Station']].value_counts().idxmax()
    print('The most frequent combination of start station and end station '
          'trip is from {} to {}\n'.format(station_combo[0], station_combo[1]))

    print("This took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total travel time is {}'.format(df['Trip Duration'].sum()))

    # display mean travel time
    print('The mean travel time is {}\n'.format(df['Trip Duration'].mean()))

    print("This took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Count by user type:\n{}\n'
          .format(df['User Type'].value_counts().to_string(header=False)))

    # Display counts of gender
    try:
        print('Count by clientele gender:\n{}\n'
              .format(df['Gender'].value_counts().to_string(header=False)))
    except KeyError:
        print('Gender data for {} city is NOT available.\n'.format(city))

    # Display earliest, most recent, and most common year of birth
    birth_year_column = 'Birth Year'
    try:
        print('The oldest client was born in {}'
              .format(int(df[birth_year_column].min())))
        print('The youngest client was born in {}'
              .format(int(df[birth_year_column].max())))
        print('The most common year of birth of the clientele is {}\n'
              .format(int(df[birth_year_column].mode()[0])))
    except KeyError:
        print('Birth data for {} city is NOT available.\n'.format(city))

    print("This took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """Display raw data, 5 row at a time, until the user wants to stop
    or until the rows are finished."""
    idx = 0
    display_lines = True
    while display_lines:
        print('\n', df.iloc[idx:idx + 5, :].to_string())
        extra_raw_data_prompt = ('\nWould you like to display 5 more lines?'
                                 '\nVALID INPUTS ARE: Yes, No\n')
        valid_answers = ['yes', 'no']
        user_choice = get_user_data(valid_answers,
                                    extra_raw_data_prompt,
                                    error_message)
        if user_choice == 'yes':
            idx += 5
        else:
            display_lines = False


def ask_to_display_data(df):
    """Ask the user whether he would like to display raw data or not."""
    display_raw_data_prompt = ('\nWould you like to display 5 lines of raw '
                               'data?\nVALID INPUTS ARE: Yes, No\n')
    valid_answers = ['yes', 'no']
    user_choice = get_user_data(valid_answers,
                                display_raw_data_prompt,
                                error_message)
    if user_choice == 'yes':
        display_raw_data(df)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city.title())
        ask_to_display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
