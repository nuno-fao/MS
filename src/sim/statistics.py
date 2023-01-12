import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import json

def get_max_percentage_occupancy():
    # load the json file
    with open('occupancies.json', 'r') as f:
        data = json.load(f)
        
    total = 0
    count = 0

    # Iterate over all keys in the JSON file
    for key in data:
        # Get the values for the current key
        values = data[key]
        # Iterate over the values and add them to the total and count
        for value in values:
            total += value
            count += 1

    # Calculate the average
    average = total / count

    # Get the maximum value
    maximum = max([max(data[key]) for key in data])

    # Print the results
    print("Maximum value:", maximum)
    print("Average value:", average)

def waiting_cars_per_step():
    # load the json file
    with open('waitingCarsPerStep.json', 'r') as f:
        data = json.load(f)

    # extract the keys and values from the json data
    keys = list(map(int,data.keys()))
    values = list(data.values())

    # create the groups
    groups = [keys[i:i + 1000] for i in range(0, len(keys), 1000)]
    values_group = [values[i:i + 1000] for i in range(0, len(values), 1000)]

    # create the line graph
    for i in range(len(groups)):
        plt.plot(groups[i], values_group[i])

    # set the x and y axis labels
    plt.xlabel('Time')
    plt.ylabel('Number of Vehicles')

    # show the graph
    plt.show()

def average_waiting_time() :

    # Load file into a DataFrame
    data = pd.read_json('wait_times.json')

    # Create an empty DataFrame
    results_df = pd.DataFrame(columns=['Station', 'Average Waiting Time'])

    # Iterate over each key = station
    for key in data.keys():
        # Extract the values in the station
        df = data[key]

        if (df.isnull().all()):
            # Add the station id and the average waiting time to the DataFrame
            results_df = pd.concat([results_df, pd.DataFrame({'Station': key, 'Average Waiting Time': None}, index=[0])], ignore_index=True)

        else:   
            # Flatten the lists of integers
            df = df.apply(lambda x: np.mean(x) if isinstance(x, list) else x)

            # Calculate the average time of all values contained in the station
            average_time = df.mean().mean()

            # Add the station id and the average waiting time to the DataFrame
            results_df = pd.concat([results_df, pd.DataFrame({'Station': key, 'Average Waiting Time': average_time}, index=[0])], ignore_index=True)

    print(results_df['Average Waiting Time'])
    # Calculate the total average of waiting time
    total_average_time = results_df['Average Waiting Time'].mean()
    print(f"The total average of waiting time is: {total_average_time}")

    # create the bar graph
    plt.bar(results_df.index, results_df['Average Waiting Time'])

    # set the x and y axis labels
    plt.xlabel('Station')
    plt.ylabel('Average Waiting Time')

    plt.xticks(results_df.index, results_df['Station'], rotation=90, ha="right")
    plt.title(f"The total average of waiting time is: {total_average_time}", loc="center", fontsize=7)
    plt.subplots_adjust(bottom=0.2)

    # show the graph
    plt.show()

def number_cars() :

    # Load file into a DataFrame
    data = pd.read_json('wait_times.json')

    # Create an empty DataFrame
    results_df = pd.DataFrame(columns=['Station', 'Number of Vehicles'])

    # iterate through the outer keys
    for outer_key in data:

        # Add the station id and number of vehicles that pass the respective station to the DataFrame
        results_df = pd.concat([results_df, pd.DataFrame({'Station': outer_key, 'Number of Vehicles': data[outer_key].count()}, index=[0])], ignore_index=True)

    # Calculate the average cars
    average_number_cars = results_df['Number of Vehicles'].mean()
    print(f"The average number of cars served per stations: {average_number_cars}")

    # create the bar graph
    plt.bar(results_df.index, results_df['Number of Vehicles'])

    # set the x and y axis labels
    plt.xlabel('Station')
    plt.ylabel('Number of Vehicles')

    plt.xticks(results_df.index, results_df['Station'], rotation=90, ha="right")
    plt.subplots_adjust(bottom=0.2)
    plt.title(f"The average number of cars served per stations: {average_number_cars}", loc="center", fontsize=7)

    # show the graph
    plt.show()

average_waiting_time()

number_cars()

waiting_cars_per_step()

get_max_percentage_occupancy()
