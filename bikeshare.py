import pandas as pd
import calendar
from datetime import date
import os

month_dict = {"january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6, "july": 7, "august": 8,
              "september": 9, "october": 10, "november": 11, "december": 12}

numdays_in_month_dict = {"january": 31, "february": 28, "march": 31, "april": 30, "may": 31, "june": 30}


def month_to_dict(name):
    return month_dict[name.lower()]


def numdays_in_month(name):
    return numdays_in_month_dict[name.lower()]


def check_city(prompt):
    while True:
        try:
            value = str(input(prompt))
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue

        if value.lower() not in ("chicago", "new york", "washington"):
            print("Sorry, your response must not be either Chicago or New York or Washington")
            continue
        else:
            break
    return value


def check_filter(prompt):
    while True:
        try:
            value = str(input(prompt))
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue

        if value.lower() not in ("month", "day", "none"):
            print("Sorry, your response must not be either month or day or both")
            continue
        else:
            break
    return value


def check_day_filter(prompt):
    while True:
        try:
            value = str(input(prompt))
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue

        if value.lower() not in ("yes", "no"):
            print("Sorry, your response must not be either month or day or both")
            continue
        else:
            break
    return value


def check_month(input_month):
    while True:
        try:
            value = str(input(input_month))
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue

        if value.lower() not in ("january", "february", "march", "april", "may", "june"):
            print("Sorry, your response must be valid.")
            continue
        else:
            break
    return value


def check_day(day, selected_month):
    while True:
        try:
            value = int(input(day))
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue

        number_of_day_in_month = numdays_in_month(selected_month.lower())

        if not (value > 0 and value < number_of_day_in_month):
            print("Sorry, your response must not be a valid number")
            continue
        else:
            break
    return value


def check_week_of_day(prompt):
    while True:
        try:
            value = str(input(prompt))
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue

        if value.lower() not in ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"):
            print("Sorry, your response must not be a valid day")
            continue
        else:
            break
    return value


def load_data(city, analysis_month, selected_day, analysis_day_of_week):
    if analysis_month != "":
        print("Data for {} {} is loading... Thank you for your patience...".format(city.capitalize(),
                                                                                   analysis_month.capitalize()))
        print("\n")

    elif analysis_day_of_week != "":
        print("Data for {} {} is loading... Thank you for your patience...".format(city.capitalize(),
                                                                                   analysis_day_of_week.capitalize()))
        print("\n")

    else:
        print("Data for {} is loading... Thank you for your patience...".format(city.capitalize()))
        print("\n")

    path = os.path.abspath(os.path.dirname("./data/"))

    CITY_DATA = {'chicago': path + '/chicago.csv',
                 'new york': path + '/new_york_city.csv',
                 'washington': path + 'washington.csv'}


    df = pd.read_csv(CITY_DATA[city.lower()])


    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month

    # extract month and day of week from Start Time to create new columns
    df['day'] = df['Start Time'].dt.day
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # extract hour of day from Start Time to create new columns
    df['hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if analysis_month != "":
        # use the index of the months list to get the corresponding int
        selected_month_number = month_to_dict(analysis_month.lower())

        # filter by month to create the new dataframe
        df = df[df['month'] == selected_month_number]
        if selected_day !="":
            df = df[df['day'] == selected_day]
    # filter by day of week if applicable
    elif analysis_day_of_week != "":
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == analysis_day_of_week.title()]

    return df

# when no filter is selected, i.e. "none", the most popular month is found using whole dataset
def calc_popular_month(df):
    print("Calculating statistics for the most popular month...")

    # if the user hasn't selected any specific month, the whole dataframe will be analysed for the most popular day of week
    print(calendar.month_name[df['month'].value_counts().idxmax()] +" is the most popular month.")
    print("\n")


    input("Press Enter to continue...")
    print("\n")

# when no filter is selected, i.e. "none", the most popular day is found using the whole dataset
# when month filter is selected, i.e. "month", the most popular day in selected month is found using
# a dataset filtered by the selected month
# input parameters are arranged to write better comments in the command prompt
def calc_popular_day_of_week(df,city,analysis_type,selected_month):
    print("Calculating statistics for the most popular day of week...")

    if 'day_of_week' in df.columns:
        # if the user hasn't selected any specific month, the whole dataframe will be analysed for the most
        # popular day of week
        if analysis_type=='none':
            print(df['day_of_week'].value_counts().idxmax() + " is the most popular day of the week.")
            print("\n")

        elif analysis_type=='month':
            print(df['day_of_week'].value_counts().idxmax() + " is the most popular day of the week in {}.".format(selected_month.capitalize()))
            print("\n")

    else:
        print("Rental day information is not available for {}.".format(city.capitalize()))

    input("Press Enter to continue...")
    print("\n")

# when no filter is selected, i.e. "none", the most popular hour is found using the whole dataset
# when month filter is selected, i.e. "month", the most popular hour in selected month is found using a
# dataset filtered by the selected month (for example, for January)
# when month filter is selected for a specific day, i.e. "month", the most popular hour in selected month
# for that selected day is found using a dataset filtered by the selected month and selected day in that month
# (for example January 20)
# input parameters are arranged to write better comments in the command prompt
def calc_popular_hour(df,city,analysis_type,selected_month,selected_day,selected_day_of_week):
    print("Calculating statistics for the most popular hour to start trip...")

    if 'hour' in df.columns:

        if  analysis_type=='none':
        # if the user hasn't selected any specific month, the whole dataframe will be analysed for the most popular day of week
            print(str(df['hour'].value_counts().idxmax()) +" is the most popular hour of the day to start trip.")
            print("\n")

        elif analysis_type=='month':
            if selected_day!='':
                print(str(df['hour'].value_counts().idxmax()) +" is the most popular hour on {} {} to start trip.".format(selected_month.capitalize(),selected_day))
                print("\n")

            else:
                print(str(df['hour'].value_counts().idxmax()) +" is the most popular hour of the day in {} to start trip.".format(selected_month.capitalize()))
                print("\n")

        elif analysis_type=='day':
            print(str(df['hour'].value_counts().idxmax()) +" is the most popular hour on {}s to start trip.".format(selected_day_of_week.capitalize()))
            print("\n")

    else:
        print("Rental hour information is not available for {}.".format(city.capitalize()))


    input("Press Enter to continue...")
    print("\n")

def calc_user_gender(df,city,analysis_type,selected_month,selected_day,selected_day_of_week):
    print("Calculating statistics for the user genders...")

    if 'Gender' in df.columns:

        if  analysis_type=='none':
        # if the user hasn't selected any specific month, the whole dataframe will be analysed for the most popular day of week
            print(df['Gender'].value_counts().idxmax() +" customers used this application more frequently in general.")
            print("\n")

        elif analysis_type=='month':
            if selected_day!='':
                print(df['Gender'].value_counts().idxmax() +" customers used this application more frequently on {} {}.".format(selected_month.capitalize(),selected_day))
                print("\n")

            else:
                print(df['Gender'].value_counts().idxmax() +" customers used this application more frequently in {}.".format(selected_month.capitalize()))
                print("\n")

        elif analysis_type=='day':
            print(df['Gender'].value_counts().idxmax() +" customers used this application more frequently on {}s.".format(selected_day_of_week.capitalize()))
            print("\n")

    else:
        print("Gender information is not available for {}.".format(city.capitalize()))
    input("Press Enter to continue...")
    print("\n")



def calc_user_type(df,city,analysis_type,selected_month,selected_day,selected_day_of_week):
    print("Calculating statistics for the user types...")

    if 'User Type' in df.columns:
        if  analysis_type=='none':
        # if the user hasn't selected any specific month, the whole dataframe will be analysed for the most popular day of week
            print(df['User Type'].value_counts().idxmax() +" type of users used this application more frequently in general.")
            print("\n")

        elif analysis_type=='month':
            if selected_day!='':
                print(df['User Type'].value_counts().idxmax() +" type of users used this application more frequently on {} {}.".format(selected_month.capitalize(),selected_day))
                print("\n")
            else:
                print(df['User Type'].value_counts().idxmax() +" type of users used this application more frequently in {}.".format(selected_month.capitalize()))
                print("\n")

        elif analysis_type=='day':
            print(df['User Type'].value_counts().idxmax() +" type of users used this application more frequently on {}s.".format(selected_day_of_week.capitalize()))
            print("\n")

    else:
        print("User Type information is not available for {}.".format(city.capitalize()))

    input("Press Enter to continue...")
    print("\n")

def calc_user_birth_year(df,city,analysis_type,selected_month,selected_day,selected_day_of_week):
    print("Calculating statistics for the user birth year...")

    if 'Birth Year' in df.columns:
        if  analysis_type=='none':
        # if the user hasn't selected any specific month, the whole dataframe will be analysed for the most popular day of week
            print("People who were born in " \
                  + str(int(df['Birth Year'].value_counts().idxmax())) \
                  +" used this application more frequently in general.")
            print("\n")

        elif analysis_type=='month':
            if selected_day!='':
                print("People who were born in " \
                      +str(int(df['Birth Year'].value_counts().idxmax())) \
                      +" users used this application more frequently on {} {}."\
                      .format(selected_month.capitalize(),selected_day))
                print("\n")

            else:
                print("People who were born in " \
                      +str(int(df['Birth Year'].value_counts().idxmax())) \
                      +" users used this application more frequently in {}.".format(selected_month.capitalize()))
                print("\n")

        elif analysis_type=='day':
            print("People who were born in " \
                  +str(int(df['Birth Year'].value_counts().idxmax())) +" users used this application more frequently on {}s.".format(selected_day_of_week.capitalize()))
            print("\n")

    else:
        print("Birth Year information is not available for {}.".format(city.capitalize()))

    input("Press Enter to continue...")
    print("\n")


def calc_popular_trip(df,city,analysis_type,selected_month,selected_day,selected_day_of_week):
    print("Calculating statistics for the most popular trip from start to end")

    if ('Start Station' in df.columns) and ('End Station' in df.columns):
        grouped= df.groupby(['Start Station', 'End Station'],sort=False)['Start Time'] \
                    .count() \
                    .reset_index(name='Count') \
                    .sort_values(['Count'], ascending=False) \
                    .head(1)

        station_info = str(grouped.iloc[0]['Start Station']) \
                        + " - " \
                        + str(grouped.iloc[0]['End Station'])

        trip_counts = str(grouped.iloc[0]['Count'])

        if  analysis_type=='none':
        # if the user hasn't selected any specific month, the whole dataframe will be analysed for the most popular day of week
            print( station_info +" is the most popular trip with {} trips in general.".format(trip_counts))
            print("\n")

        elif analysis_type=='month':
            if selected_day!='':
                print(station_info +" is the most popular trip with {} trips on {} {}.".format(trip_counts,selected_month.capitalize(),selected_day))
                print("\n")
            else:
                print(station_info +" is the most popular trip with {} trips in {}.".format(trip_counts,selected_month.capitalize()))
                print("\n")
        elif analysis_type=='day':
            print(station_info +" is the most popular trip with {} trips in {}s.".format(trip_counts,selected_day_of_week.capitalize()))
            print("\n")

    else:
        print("Start Station or End Station information is not available for {}.".format(city))

    input("Press Enter to continue...")
    print("\n")

def calc_longest_trip_duration(df,city,analysis_type,selected_month,selected_day,selected_day_of_week):
    print("Calculating statistics for the longest trip duration from start to end")

    if 'Trip Duration' in df.columns:

        tripDuration = df['Trip Duration'].max()

        if  analysis_type=='none':
        # if the user hasn't selected any specific month, the whole dataframe will be analysed for the most popular day of week
            print(str(tripDuration) +" is the longest trip duration in general.")
            print("\n")
        elif analysis_type=='month':
            if selected_day!='':
                print(str(tripDuration) +" is the longest trip duration on {} {}.".format(selected_month.capitalize(),selected_day))
                print("\n")

            else:
                print(str(tripDuration) +" is the longest trip duration in {}.".format(selected_month.capitalize()))
                print("\n")

        elif analysis_type=='day':
            print(str(tripDuration) +" is the longest trip duration in {}s.".format(selected_day_of_week.capitalize()))
            print("\n")

    else:
        print("Trip Duration information is not available for {}.".format(city.capitalize()))

def display_data(df,city,analysis_type,selected_month,selected_day,selected_day_of_week):

    keep_showing = "y"

    start = 0
    length = 5
    i = 0


    while keep_showing == "y":
        end_index = length+(i*5)
        print("\n")
        print("Displaying the {}th 5 individual trip data...".format(str(i+1)))
        print(df.iloc[(start+(i*5)):(length+(i*5)),1:8])

        if end_index<len(df.index):
            i += 1
            keep_showing = input("Would you like to continue displaying data? Press \'y\' or \'n\'")
        else:
            keep_showing == "n"
            print("You have reached to the end of the Data for {}".format(city.capatilize()))

    print("\n")
    print ("Thank you!")
    print("\n")


def execute_analysis():
    print("\n")
    print("\n")

    print("Hello! Let's explore US bikeshare statistics.")

    city = check_city("Please select the city you want to see the statistics; Chicago, New York, Washington: ")
    print("You have selected to view statistics for " +city.capitalize())
    print("\n")

    analysis_type = check_filter("Would you like to run the analysis for {} on a monthly basis or daily basis or not at all? Type out \'month\' or \'day\' or \'none\' :".format(city.capitalize()))

    selected_month = ""
    selected_day = ""
    selected_day_of_week = ""
    filter_type = ""

    if analysis_type == "month":
        print("\n")
        selected_month = check_month("Please type out the month you want to view the data for; January, February, March, April, May, June: ")
        print("\n")
        filter_type = check_day_filter("Would you like to run analysis for a specific day in {} ? \'yes\' or \'no\'".format(selected_month.capitalize()))
        if filter_type=="yes":
            print("\n")
            selected_day = ("Which day in {}?".format(selected_month.capitalize()))
            selected_day = check_day(selected_day, selected_month)
    elif analysis_type == "day":
        print("\n")
        selected_day_of_week = check_week_of_day("Please type out a day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday: ")

    df = load_data(city,selected_month,selected_day,selected_day_of_week)

    if analysis_type=="none":
        # Calculating the most popular month in whole dataset
        calc_popular_month(df)

        # Calculating the most popular day of week in whole dataset
        calc_popular_day_of_week(df,city,analysis_type,selected_month)
    elif analysis_type=="month":
        # Calculating the most popular week for a given month
        calc_popular_day_of_week(df,city,analysis_type,selected_month)


    # Calculating the most popular hour
    calc_popular_hour(df,city,analysis_type,selected_month,selected_day,selected_day_of_week)

    # Calculating the user type
    calc_user_gender(df,city,analysis_type,selected_month,selected_day,selected_day_of_week)

    # Calculating the user type
    calc_user_type(df,city,analysis_type,selected_month,selected_day,selected_day_of_week)

    # Calculating the most popular age group
    calc_user_birth_year(df,city,analysis_type,selected_month,selected_day,selected_day_of_week)

    # Calculating the most popular trip from start to end
    calc_popular_trip(df,city,analysis_type,selected_month,selected_day,selected_day_of_week)

    # Calculating the duration of trip
    calc_longest_trip_duration(df,city,analysis_type,selected_month,selected_day,selected_day_of_week)

    # Displaying the data for a set of five
    display_data(df,city,analysis_type,selected_month,selected_day,selected_day_of_week)

#########################################



def main():

    restart = "y"

    while restart == "y":
        execute_analysis()
        print("\n")
        restart = input("Would you like to run another analysis? Press \'y\' or \'n\'")
    print("\n")
    print ("Thank you!")
    print("\n")


main()
