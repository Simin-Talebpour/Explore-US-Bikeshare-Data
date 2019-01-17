import csv
import calendar
import time
from datetime import datetime
from collections import Counter

## Filenames
chicago = 'chicago.csv'
new_york_city = 'new_york_city.csv'
washington = 'washington.csv'

# The months user choose from as a filter
months_choices = ['january','february','march','april','may','june']

def get_city():
    '''Asks the user for a city and returns the filename for that city's bike share data.

    Args:
        none.
    Returns:
        (str) Filename for a city's bikeshare data.
    '''

    while True:
        city = input('\nHello! Let\'s explore some US bikeshare data!\n'
                 'Would you like to see data for Chicago, New York, or Washington?\n')
        city = city.title()
        if city == "Chicago" or city == "New York" or city == "Washington":
            break
        else:
            print("that\'s not a valid entry.\n Try: Chicago, New York or Washington")
    if city == 'Chicago':
        return(chicago)
    elif city == 'New York':
        return(new_york_city)
    else:
        return(washington)

def get_time_period():
    '''Asks the user for a time period and returns the specified filter.

    Args:
        none.
    Returns:
        returns 'none' if user decided for no filter
        or the name of a month from months_choices
        or an integer for a day in week
    '''
    while True:
        time_period = input('\nWould you like to filter the data by month, day, or not at'
                            ' all? Type "none" for no time filter.\n')
        time_period = time_period.lower()

        if time_period  == 'none':
            return('none')
        elif time_period == 'month':
           return(get_month())
        elif time_period == 'day':
            return(get_day())
        else:
            print("that\'s not a valid entry.\n Try: date, month or none")

def get_month():
    '''Asks the user for a month and returns the specified month.

    Args:
        none.
    Returns:
       (str) month name from months_choices
    '''
    while(True):
        month = input('\nWhich month? January, February, March, April, May, or June?\n')
        valid = ('january' , 'february' , 'march' , 'april' , 'may' , 'june')
        month = month.lower()
        if month in valid:
            return(month)
        else:
            print("that\'s not a valid entry.\n Try: January, February, March, April, May, or June")

def get_day():
    '''Asks the user for a day and returns the specified day.

        Args:
            none.
        Returns:
            an integer between 0(Monday) to 6(Friday) for days in the week

    '''

    while(True):
        try:
            day = int(input('\nWhich day? Please type your response as an integer '
             'between 0(Monday) and 6(Sunday).\n'))
        except ValueError:
            print("that\'s not a valid entry.\n"
            "type your response as an integer between 0(Monday) and 6(Sunday)")
        else:
            if 1 <= day <= 6:
                return(day)
            else:
                print("that\'s not a valid entry.\n"
                "type your response as an integer between 0(Monday) and 6(Sunday)")

def load_city_data(city_file):
    '''opens slected csv file in read mode and load data into a list of dictionaries
    each dictionary is a row of selected city file

    Args:
       (str) name of the cvs file for selected city
    Returns:
       (list) each element is a dictionary that contains one row of selected csv file
    '''
    #i = 1
    city_data=[]
    with open(city_file) as csvfile:
        reader= csv.DictReader(csvfile)
        city_data = [{k: v for k, v in row.items()} for row in reader]
        '''
        # just for testing on a smaller collection of data
        for row in reader:
            city_data.append({k: v for k, v in row.items()})
            i += 1
            if i>200:
                break
        '''
    return(city_data)


def popular_month(city_data):
    '''finds the most popular month in start time field in the selected csv file

    Args:
       (list) data from selected csv file
    Returns:
       (str) month name
    '''
    month_col =  [0,0,0,0,0,0]
    # a list of six integers for six months in months_choices
    #month_col[0] shows the number of Januarys in Start Time field
    #month_col[5] shows the number of Junes in Start Time field
    for row in city_data:
        dt = datetime.strptime(row['Start Time'], '%Y-%m-%d %H:%M:%S')
        month_col[(dt.month)-1] += 1

    max_index = month_col.index(max(month_col))
    popular_month = calendar.month_name[max_index+1]
    return(popular_month)

def popular_day(city_data, time_period):
    '''finds the most popular day in start time field in the selected csv file

    Args:
       (list) data from selected csv file
    Returns:
       (integer) a number between 0(Monday) to 6(Friday) that shows day in the week
    '''
    day_col=[0,0,0,0,0,0,0]
    #day_col is a list of seven integers for seven days of the week
    #day_col[0] shows the number of Mondays in the "start time"
    #day_col[6] shows the number of Sundays in the "start time"
    for row in city_data:
        dt = datetime.strptime(row['Start Time'], '%Y-%m-%d %H:%M:%S')
        if time_period == 'none':
            day_col[dt.weekday()] += 1
        else:
            if calendar.month_name[dt.month].lower() == time_period:
                day_col[dt.weekday()] += 1


    max_index = day_col.index(max(day_col))
    popular_day = calendar.day_name[max_index]
    return(popular_day)

def popular_hour(city_data, time_period):
    '''finds the most popular hour in start time field in the selected csv file for selected time period

    Args:
       (list) data from selected csv file
    Returns:
       (integer) a number between 0 to 23 for hour
    '''

    hours =  []
    # hours is a list that contains hour of start_time
    for row in city_data:
        dt = datetime.strptime(row['Start Time'], '%Y-%m-%d %H:%M:%S')
        if time_period == 'none':
            hours.append(dt.hour)
        elif time_period in months_choices:
            if calendar.month_name[dt.month].lower() == time_period:
                hours.append(dt.hour)
        else:
            if dt.weekday() == time_period:
                hours.append(dt.hour)
    cnt = Counter(hours)
    popular_hour = cnt.most_common(1)
    return(popular_hour[0][0])

def trip_duration(city_data, time_period):
    '''finds the total and average of trip duration field in the selected csv file for selecte time period

    Args:
       (list) data from selected csv file
    Returns:
       (float,float) returns two number: total trip duration and average trip duration
    '''
    total_trip = 0
    average_trip = 0
    for row in city_data:
        dt = datetime.strptime(row['Start Time'], '%Y-%m-%d %H:%M:%S')
        if time_period == 'none':
            total_trip += float(row['Trip Duration'])
        elif time_period in months_choices:
            if calendar.month_name[dt.month].lower() == time_period:
                total_trip += float(row['Trip Duration'])
        else:
            if dt.weekday() == time_period:
                total_trip += float(row['Trip Duration'])

    average_trip = total_trip/len(city_data)
    return(total_trip, average_trip)

def popular_stations(city_data, time_period):
    '''finds the most popular start/end stations in the selected csv file for selected time period

    Args:
       (list) data from selected csv file
    Returns:
       (str, str) the most popular start station, the most popular end station
    '''
    start_stations = []
    #a list that includes just start statins from csv file based on time filter
    end_stations = []
    # a list that includes just end statins from csv file based on time filter
    for row in city_data:
        dt = datetime.strptime(row['Start Time'], '%Y-%m-%d %H:%M:%S')
        if time_period == 'none':
            start_stations.append(row['Start Station'])
            end_stations.append(row['End Station'])
        elif time_period in months_choices:
            if calendar.month_name[dt.month].lower() == time_period:
                start_stations.append(row['Start Station'])
                end_stations.append(row['End Station'])
        else:
            if dt.weekday() == time_period:
                start_stations.append(row['Start Station'])
                end_stations.append(row['End Station'])

    cnt_start_stations = Counter(start_stations)
    cnt_end_stations = Counter(end_stations)
    popular_start_station = cnt_start_stations.most_common(1)
    popular_end_station = cnt_end_stations.most_common(1)

    return(popular_start_station[0][0], popular_end_station[0][0])

def popular_trip(city_data, time_period):
    '''finds the most popular trip between start and end stations in the selected csv file for selected time period

    Args:
       (list) data from selected csv file
    Returns:
       (str) the most popular trip between start station and end station
    '''
    trips = []
    # a list included two fiels from selected csv file: start station and end station
    for row in city_data:
        dt = datetime.strptime(row['Start Time'], '%Y-%m-%d %H:%M:%S')
        if time_period == 'none':
            trips.append({'Start Station':row['Start Station'],'End Station':row['End Station']})
        elif time_period in months_choices:
            if calendar.month_name[dt.month].lower() == time_period:
                trips.append({'Start Station':row['Start Station'],'End Station':row['End Station']})
        else:
            if dt.weekday() == time_period:
                trips.append({'Start Station':row['Start Station'],'End Station':row['End Station']})

    counter_result = Counter((row['Start Station'],row['End Station']) for row in trips )
    popular_trip = counter_result.most_common(1)

    return(popular_trip[0][0])

def count_usertype(city_data, time_period):
    '''finds the number of customers and subscribers from User Type field
    in the selected csv file for the selected time period

    Args:
       (list) data from selected csv file
    Returns:
       (int,int ) the number of subscribers and customers
    '''
    subscribers = 0
    customers = 0
    for row in city_data:
        dt = datetime.strptime(row['Start Time'], '%Y-%m-%d %H:%M:%S')
        if time_period == 'none':
            if row['User Type'] == 'Subscriber':
                subscribers += 1
            else:
                customers += 1
        elif time_period in months_choices:
            if calendar.month_name[dt.month].lower() == time_period:
                if row['User Type'] == 'Subscriber':
                    subscribers += 1
                else:
                    customers += 1
        else:
            if dt.weekday() == time_period:
                if row['User Type'] == 'Subscriber':
                    subscribers += 1
                else:
                    customers += 1

    return(subscribers, customers)

def count_gender(city_data, time_period):
    '''finds the number of males and females from Gender field
    in the selected csv file for the selected time period

    Args:
       (list) data from selected csv file
    Returns:
       (int, int) the number of females, the number of males
    '''
    female_count = 0
    male_count = 0
    for row in city_data:
        dt = datetime.strptime(row['Start Time'], '%Y-%m-%d %H:%M:%S')
        if time_period == 'none':
            if row['Gender'] == 'Female':
                female_count += 1
            elif row['Gender'] == 'Male':
                male_count += 1

        elif time_period in months_choices:
            if calendar.month_name[dt.month].lower() == time_period:
                if row['Gender'] == 'Female':
                    female_count += 1
                elif row['Gender'] == 'Male':
                    male_count += 1

        else:
            if dt.weekday() == time_period:
                if row['Gender'] == 'Female':
                    female_count += 1
                elif row['Gender'] == 'Male':
                    male_count += 1

    return(female_count,male_count)

def birthyear(city_data, time_period):
    '''finds the earliest,most_recent and the most popular birth years
    from Birt Year field
    in the selected csv file for the selected time period

    Args:
       (list) data from selected csv file
    Returns:
       (int, int, int) the earliest, most recent and most popular birth year
    '''

    birthyear =  []
    #a list that includes just Birth Year filed from csv file based on time filter
    popular_birthyear = 0

    for row in city_data:
        dt = datetime.strptime(row['Start Time'], '%Y-%m-%d %H:%M:%S')
        if time_period == 'none':
            if row['Birth Year'] != '':
                birthyear.append(int(float(row['Birth Year'])))
        elif time_period in months_choices:
            if calendar.month_name[dt.month].lower() == time_period:
                if row['Birth Year'] != '':
                    birthyear.append(int(float(row['Birth Year'])))
        else:
            if dt.weekday() == time_period:
                if row['Birth Year'] != '':
                    birthyear.append(int(float(row['Birth Year'])))

    cnt = Counter(birthyear)
    popular_birthyear=cnt.most_common(1)
    return(min(birthyear), max(birthyear), popular_birthyear[0][0])

def display_data(city_data):
    '''Displays five lines of data if the user specifies that they would like to.
    After displaying five lines, ask the user if they would like to see five more,
    continuing asking until they say stop.

    Args:
        none.
    Returns:
        nothing
    '''

    i = 0
    while True:
        display = input('\nWould you like to view individual trip data?'
                        'Type \'yes\' or \'no\'.\n')
        if display.lower() == 'yes':
            for row in city_data:
                print(row)
                i += 1
                if i == 5:
                    while True:
                        more = input('\nWould you like to see five more trip data?'
                                        'Type \'yes\' or \'no\'.\n')
                        if more.lower() == 'yes':
                            i = 0
                            break
                        elif more.lower() == 'no':
                            return()
                        else:
                            print('\nPlease enter:\'yes\' or \'no\'.')
                            continue
        elif display.lower() == 'no':
            return()
        else:
            print('\nPlease enter:\'yes\' or \'no\'.')
            continue

def statistics():
    '''Calculates and prints out the descriptive statistics about a city and time period
    specified by the user via raw input.

    Args:
        none.
    Returns:
    none.
    '''
    # Filter by city (Chicago, New York, Washington)
    city_file = get_city()

    # Filter by time period (month, day, none)
    time_period = get_time_period()

    print('\n\nCalculating the first statistic...')

    # open csv file for selected city and load the file into a list
    city_data = load_city_data(city_file)

    # What is the most popular month for start time?
    if time_period == 'none':
        start_time = time.time()
        print("The most popular month for start time is ", popular_month(city_data))
        print("That took %s seconds." % (time.time() - start_time))
        print("\n\nCalculating the next statistic...")

    # What is the most popular day of week (Monday, Tuesday, etc.) for start time?
    if time_period == 'none' or time_period == 'month':
        start_time = time.time()
        print("The most popular day for start time is ",popular_day(city_data,time_period))
        print("That took %s seconds." % (time.time() - start_time))
        print("\n\nCalculating the next statistic...")

    start_time = time.time()
    # What is the most popular hour of day for start time?
    print("The most popular hour of day for start time is ",popular_hour(city_data,time_period))
    print("That took %s seconds." % (time.time() - start_time))
    print("\n\nCalculating the next statistic...")

    start_time = time.time()
    total_trip , average_trip = trip_duration(city_data,time_period)
    # What is the total trip duration and average trip duration?
    print("The total trip duration is ", total_trip)
    print("The average trip duration is ", average_trip)
    print("That took %s seconds." % (time.time() - start_time))
    print("\n\nCalculating the next statistic...")

    start_time = time.time()
    #What is the most popular start station and most popular end station?
    start_station , end_station = popular_stations(city_data, time_period)
    print("The most poular start station is ", start_station)
    print("The most popular end station is ", end_station)
    print("That took %s seconds." % (time.time() - start_time))
    print("\n\nCalculating the next statistic...")


    start_time = time.time()
    #What is the most popular trip?
    start_station , end_station = popular_trip(city_data, time_period)
    print("The most popular trip is from {} to {}.".format(start_station, end_station))
    print("That took %s seconds." % (time.time() - start_time))
    print("\n\nCalculating the next statistic...")

    start_time = time.time()
    # What are the counts of each user type?
    subscribers, customers = count_usertype(city_data, time_period)
    print("Theere are {} subscribers.".format(subscribers))
    print("Theere are {} customers.".format(customers))
    print("That took %s seconds." % (time.time() - start_time))
    print("\n\nCalculating the next statistic...")

    if city_file != washington:
        start_time = time.time()
        # What are the counts of gender?
        females, males = count_gender(city_data, time_period)
        print("Theere are {} females and {} males.".format(females, males))
        print("That took %s seconds." % (time.time() - start_time))
        print("\n\nCalculating the next statistic...")

        start_time = time.time()
        # What are the earliest, most recent, and most popular birth years?
        earliest_by, latest_by, popular_by = birthyear(city_data, time_period)
        print("The earlise birth year is ", earliest_by)
        print("The most recent birthe year is ", latest_by)
        print("The most popular birth year is ", popular_by)
        print("That took %s seconds." % (time.time() - start_time))

    # Display five lines of data at a time if user specifies that they would like to
    display_data(city_data)

    #restart the program if user want to
    while True:
        restart = input('\nWould you like to restart? Type \'yes\' or \'no\'.\n')
        if restart.lower() == 'yes':
            statistics()
            break
        elif restart.lower() == 'no':
            break
        else:
            print("\nThat's not a valid entry. Please enter 'yes' or 'no'")

if __name__ == "__main__":
	statistics()
