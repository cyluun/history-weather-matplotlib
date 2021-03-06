# Playing with weather data sets and matplotlib
# Author: Ada Vasileiou
# Csv files include weather data for all the Septembers from 2000 to 2015
# Location: SKG


import numpy as np
from matplotlib import pyplot as plt
from matplotlib import dates as mpldates
from matplotlib.ticker import MultipleLocator
from datetime import datetime
import csv
import glob

path = 'csv-files/*.csv'


def parse(rawfile, delimiter):
    """ Parses a raw csv file to a JSON-like object """

    opened_file = open(rawfile)
    rawdata = csv.reader(opened_file, delimiter=delimiter)
    parsed_data = []
    categories = rawdata.next()

    for row in rawdata:
        parsed_data.append(dict(zip(categories, row)))
    opened_file.close()
    return parsed_data



def daily_mean(docum):
    """ Returns the date and the mean temperature for that date """

    parsed = parse(docum, ',')

    # From parsed data we keep the date 'EEST' and the temperature
    # 'Mean TemperatureC' in a dictionary. Also transforming the date
    # into a datetime object and the temperature into an integer.
    mean_temps = {datetime.strptime(item['EEST'], '%Y-%m-%d'):
                    int(item['Mean TemperatureC']) for item in parsed}

    # Sorting dates by turning the dictionary into a list of tuples
    mean_temps_tup = [(date, temp) for date, temp in mean_temps.items()]
    mean_temps_tup.sort()

    # Splitting into two lists in order to make plot
    dates, temps = zip(*mean_temps_tup)

    return [dates, temps]



def plot_daily(docum):
    """ Makes a figure of daily mean temperatures """

    dates, temps = daily_mean(docum)

    fig, ax = plt.subplots()
    ax.plot(dates, temps, color='royalblue')

    # Customizing appearance
    plt.ylabel('Mean Temperature C')
    plt.xticks(rotation=90, color='grey')
    plt.yticks(np.arange(13, 31), color='firebrick')
    plt.subplots_adjust(bottom=0.2)
    plt.grid()
    minorLocator = MultipleLocator(1)
    ax.xaxis.set_minor_locator(minorLocator)
    plt.rcParams['font.size'] = 8

    # Saving figure and closing
    plt.savefig('%s.png' % (str(docum).split('.')[0]))
    plt.clf()



def run_all_daily_means():
    """ Running plot_daily for all the files in the directory """

    for f in glob.glob(path):
        print 'Processing ' + f.split('/')[-1]
        plot_daily(f)



######################## BY YEAR ########################



def monthly_mean(docum):
    """ Takes the daily low, mean and max temperatures and returns
        the mean_low temp, mean_mean temp, and mean_max temp for the month """

    parsed = parse(docum, ',')

    low_temps = [int(item['Min TemperatureC']) for item in parsed]
    mean_low = sum(low_temps)/30.0

    mean_temps = [int(item['Mean TemperatureC']) for item in parsed]
    mean_mean = sum(mean_temps)/30.0

    max_temps = [int(item['Max TemperatureC']) for item in parsed]
    mean_max = sum(max_temps)/30.0

    return [mean_low, mean_mean, mean_max]



def run_all_monthly_means():
    """ Collects the means from all files through monthly_mean
        function and rearranges data to all_lows, all_means, all_maximums """

    all_lmm = []
    for f in sorted(glob.glob(path)):
        print 'processing', f
        all_lmm.append(monthly_mean(f))

    all_lows = [lst[0] for lst in all_lmm]
    all_means = [lst[1] for lst in all_lmm]
    all_maxs = [lst[2] for lst in all_lmm]

    return [all_lows, all_means, all_maxs]



def plot_yearly():
    """ Makes a figure with 3 plots (lows, means, maximums) """

    means = run_all_monthly_means()
    all_lows, all_means, all_maxs = means[0], means[1], means[2]

    x = range(2000, 2016)

    fig, ax = plt.subplots()
    ax.plot(x, all_lows, label='Lows', color='royalblue')
    ax.plot(x, all_means, label='Means', color='gold')
    ax.plot(x, all_maxs, label='Maxes', color='r')

    ax.axis('tight')
    ax.legend(loc=4,prop={'size':11})
    plt.grid()
    plt.title('September through the years')
    plt.ylabel('Temperatures C')
    plt.xticks(np.arange(min(x), max(x)+1, 1.0), rotation=90, color='grey')
    plt.yticks(np.arange(13, 31), color='firebrick')
    plt.subplots_adjust(bottom=0.1)
    plt.rcParams['font.size'] = 8

    plt.savefig('2000-2015.png')
    plt.clf()
