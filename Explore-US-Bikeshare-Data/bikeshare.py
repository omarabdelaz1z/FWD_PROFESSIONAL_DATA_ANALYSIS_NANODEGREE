import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

DAYS = {
    'monday': 0,
    'tuesday': 1,
    'wednesday': 2,
    'thursday': 3,
    'friday': 4,
    'saturday': 5,
    'sunday': 6
}

# only the first six months.
MONTHS = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # User Input for City.
    city = ""
    while(city not in CITY_DATA):
        city = input("- Select City (Chicago, Washington or New York City): ").strip().lower()
    
    # User Input for Month.
    month = ""
    while(month not in MONTHS):
        month = input("\n- Select Month (January, February, ....., June) or 'all' for no filter.\n\n- Input : ").strip().lower()
        if(month == 'all'):
            break
    
    # User Input for Day.
    day = ""
    while(day not in DAYS):
        day = input("\n- Select Day (Saturday, Sunday, ....., Friday) or 'all' for no filter.\n\n- Input : ").strip().lower()
        if(day == 'all'):
            break
    
    print('-'*40)
    
    # Return a lower-case values encapsulated in a tuple.
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
    # Creating a DataFrame by acessing the value (.csv file) of the given city.
    df = pd.read_csv(CITY_DATA[city])
    
    # I changed column names to be more convenient during accessing them.
    df.rename(columns={'Start Time': 'start_time', 'End Time': 'end_time', 'Trip Duration': 'trip_duration',
                       'Start Station': 'start_station', 'End Station': 'end_station', 'User Type': 'user_type', 'Birth Year': 'birth_year'}, inplace=True)
    
    # Changing Date Columns to be datetime instead of Object so we can use their properties and it is better than using .str methods.
    df[['start_time', 'end_time']] = df[['start_time', 'end_time']].apply(pd.to_datetime)
    
    # No Filters.
    if(month == day):
        return df
    
    # Day Only.
    elif month == 'all':
        return df[(df.start_time.dt.dayofweek == DAYS[day])]
    
    # Month Only.
    elif day == 'all':
        return df[(df.start_time.dt.month == MONTHS[month])]
    
    # Both Filtered.
    else:
        both_filtered = (df.start_time.dt.month == MONTHS[month]) & (df.start_time.dt.dayofweek == DAYS[day])
        return df[both_filtered]

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
   
    # By Using value_counts() method, we can get the frequency of each value in the dataset sorted in descending order. 
    # To Get The Most/First Item (e.g. month), we use idxmax()
    
    # Most Common Month.
    print(f"- Common Month : {df.start_time.dt.month_name().value_counts().idxmax()}.")
    
    # Most Common Day.
    print(f"- Common Day : {df.start_time.dt.day_name().value_counts().idxmax()}.")

    # Most Common Hour.
    print(f"- Common Hour {df.start_time.dt.hour.value_counts().idxmax()}.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Most commonly used start station.
    print(f"- Start Station : {df.start_station.value_counts().idxmax()}.")

    # Most commonly used end station.
    print(f"- End Station : {df.end_station.value_counts().idxmax()}.")

    # Most frequent combination of start station and end station trip.
    # Using groupby, I counted the number of unqiue pairs and return the most occurance.
    
    pair_of_stations = df.groupby('start_station').end_station.value_counts().idxmax()
    print(f"- Start/End Station : {pair_of_stations}.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    # By Using the sum method, we can get the sum of all values in the series i.e. df.trip_duration or df['trip_duration']
    
    total_time = sum(df.trip_duration)
    print(f"Total travel time in minutes is {round(total_time * (1/60))}")

    # Display mean travel time
    # I used mean() to get the average of the series trip_duration.
    
    average_time = df.trip_duration.mean()
    print(f"Average travel time in minutes is {round(average_time * (1/60))}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    print("- User Types :- \n")
    print(pd.DataFrame(df.user_type.value_counts()))
    print('-'*40)

    # Display counts of gender
    # In this part I used try/except block to prevent any error occurs as washingnton city doesn't have gender/birth year column.
    
    try:
        # I used the constructor of pd.DataFrame() to create a good looking of value_counts() method.
        print(f"- User Gender :- \n{pd.DataFrame(df.Gender.value_counts())}")    
        print('-'*40)
    except Exception:
        print("Gender statistics is not available for Washington.")

    # Display earliest, most recent, and most common year of birth
    try:
        print(f"- Earliest Year : {int(df.birth_year.min())}.")
        print(f"- Recent Year : {int(df.birth_year.max())}.")
        print(f"- Common Year : {int(df.birth_year.value_counts().idxmax())}.")
    except Exception:
        print("Birth Year statistics is not available for Washington.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    # Looping until the user type 'no'
    while True:
        answer = input("Do you want to see raw data? Enter yes or no.\n\n- Answer : ")
        if answer.lower() != 'yes':
            break

        else:
            # creating a random sample of size 5 by using np.random.choice method.
            random_idx = np.random.choice(1000, replace=False, size=5)
            # and used .iloc[] to get those rows.
            print(df.iloc[random_idx])    

def main():
    # Looping until the user type 'no'
    while True:
        
        # Getting user input and path them into the three variables.
        city, month, day = get_filters()
        
        # Loading our filters and store the filtered DataFrame into df
        df = load_data(city, month, day)
        
        # Calculating our descriptive statistics.
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        # Asking the user if he wants to display random rows from the dataset.
        display_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("Don't forget to comeback again! Have a Great Day.")
            break


if __name__ == "__main__":
	main()
    
