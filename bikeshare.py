import time
import datetime
import pandas as pd
import os

cwd = os.getcwd()

#SELECT FILTER
def filters():
    """
    Sets filters for city, month, day and weekday - or select all

    Args:
        Non
    Returns:
        str (city): abbreviation of the city, or all or '' to apply no filter
        str (month): number of the month, or all to apply no filter
        str (day): number of the day, or all to apply no filter
        str (weekday): name of the day, or all or '' to apply no filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    list_cities = ['chi','nyc','wsh','all','']
    while True:
        city = input('\nWhich City do you want to analyse?: \n\n'
            'CHI for Chicago\n'
            'NYC for New Yor City\n'
            'WSH for Washington\n'
            'ALL or leave empty for all three cities\n'
            ).lower()
        if city in list_cities:
            break
        else:
            print('\nPlease give correct abbreviation\n')

    while True:
        try:
            month = int(input('\nWhich month are you interested in? Give number of the month or leave empty for all months:\n'))
            if month in range(1,13):
                break
            else:
                print('\nNot a proper integer! Try it again\n')
        except ValueError as e:
            print('All months have been selected')
            month = 'all'
            break

    while True:
        try:
            day = int(input('\nWhich day are you interested in? Give number of the date or enter "all":\n'))
            if day in range(1,32):
                break
            else:
                print('\nNot a proper integer! Try it again\n')
        except ValueError as e:
            print('All days have been selected')
            day = 'all'
            break

    list_weekdays = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday','all','')
    while True:
        weekday = input('\nWhich day would you like to filter by? Give fullname or enter "all":\n').lower()
        if weekday in list_weekdays:
            break
        else:
            print('\nPlease give correct Weekday\n')
    return city, month, day, weekday

#LOAD DATA
def load_data(city, month, day, weekday):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - number of the month to filter by, or "all" to apply no month filter
        (str) day - number of the day to filter by, or "all" to apply no day filter
        (str) weekday - name of the day of the week to filter by, or "all" to apply no weekday filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    if city == 'chi':
        city = 'chicago.csv'
        file = cwd + '/' + city
        df = pd.read_csv(file)
    if city == 'nyc':
        city = 'new_york_city.csv'
        file = cwd + '/' + city
        df = pd.read_csv(file)
    if city == 'wsh':
        city = 'washington.csv'
        file = cwd + '/' + city
        df = pd.read_csv(file)
    if city == 'all':
        all_files = os.listdir(cwd)    
        csv_files = list(filter(lambda f: f.endswith('.csv'), all_files))
        df = pd.concat(map(pd.read_csv, csv_files))
    if city == '':
        all_files = os.listdir(cwd)    
        csv_files = list(filter(lambda f: f.endswith('.csv'), all_files))
        df = pd.concat(map(pd.read_csv, csv_files))

    # fill NaN with NA for Gender
    if 'Gender' in df:
        df['Gender'] = df['Gender'].fillna('not available')
   
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month not in ('all',''):
        # use the index of the months list to get the corresponding int
        month = month

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day not in ('all',''):
        # filter by day of week to create the new dataframe
        df = df[df['day'] == day]

    # filter by weekday if applicable
    if weekday not in ('all',''):
        #filter by weekday to create the new dataframe
        df = df[df['day_of_week'] == weekday.title()]

    return df
'''
Various function with regards to Time analysis
    Args:
        df: the filtered dataframe
    Return:
        Various infos wrt Time
'''
#POPULAR MONTH
def popular_month(df):
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('\nMost Popular Month:', popular_month)
#POPULAR DAY
def popular_day(df):
    df['day'] = df['Start Time'].dt.day
    popular_day = df['day'].mode()[0]
    print('\nMost Popular Day:', popular_day)
#POPULAR HOUR
def popular_hour(df):
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('\nMost Popular Start Hour:', popular_hour)
'''
Various function with regards to Station and Trip analysis
    Args:
        df: the filtered dataframe
    Return:
        Various infos wrt Station and Trip
'''
#POPULAR START STATION
def popular_start_station(df):
    popular_start_station = df['Start Station'].mode()[0]
    print('\nMost Popular Start Station:', popular_start_station)
#POPULAR END STATION
def popular_end_station(df):
    popular_end_station = df['End Station'].mode()[0]
    print('\nMost Popular End Station:', popular_end_station)
#POPULAR TRIP
def station_trip(df):
    df['trip']=df['Start Station']+" "+"to"+" "+ df['End Station']
    popular_trip= df['trip'].mode()[0]
    print('\nThe most frequent combination of Start and End Station is', popular_trip)
'''
Various function with regards to Travel Times analysis
    Args:
        df: the filtered dataframe
    Return:
        Various infos wrt Travel Times
'''
#TOTAL TRAVEL TIME
def total_travel_time(df):
    total_travel_time = int(df['Trip Duration'].sum())
    ttt_formatted = str(datetime.timedelta(seconds=total_travel_time))
    print('\nTotal Travel Time:',ttt_formatted)
#AVERAGE TRAVEL TIME
def average_travel_time(df):
    average_travel_time = int(df['Trip Duration'].mean())
    avg_formatted = str(datetime.timedelta(seconds=average_travel_time))
    print('\nAvergage Travel Time:',avg_formatted)
'''
Various function with regards to user info analysis
    Args:
        df: the filtered dataframe
    Return:
        Various infos wrt User info and detals
'''
#USER TYPES
def user_types(df):
    user_types = df['User Type'].value_counts()
    print('\nThe count per user types are:\n',user_types)
#USER GENDER
def gender(df,city):
    if city == 'chi' or city == 'nyc':
        gender_counts= df['Gender'].value_counts()
        print('\nThe counts of each gender are:\n',gender_counts)
#USER BIRTH
def birth(df,city):
    if city == 'chi' or city == 'nyc':
        youngest= int(df['Birth Year'].max())
        print('\nThe youngest user is born in the year',youngest)
        oldest= int(df['Birth Year'].min())
        print('\nThe oldest user is born in the year',oldest)
        common= int(df['Birth Year'].mode()[0])
        print('\nMost users are born in the year',common)
        mean= int(df['Birth Year'].mean())
        print('\nThe average birth year is',mean)

#RAW DATA
def display_raw_data(df):
    '''
    Display 5 rows of the raw data

    Args:
        df: the filtered dataframe
    
    Return:
        displayed data
    '''
    #dropping of created columns
    df = df.drop(['trip','hour','day','month','day_of_week'], axis = 1)
    row_index = 0
    display_data = input('\nYou like to see rows of the data used to compute the stats? Please write "yes" or "no" \n').lower()
    while True:
        try:
            if display_data[0] == 'n':
                return
            if display_data[0] == 'y':
                print(df[row_index: row_index + 5])
                row_index = row_index + 5
            else:
                print('Incorrect input. Showing raw data has beeen skipped')
                return
        except:
            return
        display_data = input('\n Would you like to see five more rows of the data used to compute the stats? Please write "yes" or "no" \n').lower()

#MAIN FUNCTION
def main():
    '''
    Main function to call the previous functions
    '''
    while True:
        city, month, day, weekday = filters()
        start_time = time.time()
        df = load_data(city, month, day, weekday)
        if df.empty: 
            print('Your filters have produced no results')
        else:
            print('\n\n\n\n')
            popular_month(df)
            popular_day(df)
            popular_hour(df)
            popular_start_station(df)
            popular_end_station(df)
            station_trip(df)
            total_travel_time(df)
            average_travel_time(df)
            user_types(df)
            gender(df,city)
            birth(df,city)
            display_raw_data(df)
        restart = input('\nWould you like to restart? Enter "yes" or "no".\n').lower()
        try:
            if restart[0] == 'y':
                continue
            else:
                break
        except:
            break
    
if __name__ == "__main__":
	main()