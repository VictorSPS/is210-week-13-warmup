#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Work on boroughs module"""

import csv
import json


GRADES = {
    'A': float(1.00),
    'B': float(0.90),
    'C': float(0.80),
    'D': float(0.70),
    'F': float(0.60),
}


def get_score_summary(filename):
    """Function takes only one argument as string which represent the filename
       whose data will be read and interpreted.
    Args:
        filename(str): csv file with data.
    Returns: a dictionary
    Examples:
        >>> get_score_summary('inspection_results.csv')
        {'BRONX': (156, 0.9762820512820514),
        'BROOKLYN': (417, 0.9745803357314141),
        'STATEN ISLAND': (46, 0.9804347826086955),
        'MANHATTAN': (748, 0.9771390374331531),
        'QUEENS': (414, 0.9719806763285017)}
    """
    data = {}
    fhandler = open(filename, 'r')
    csv_f = csv.reader(fhandler)

    for row in csv_f:
        if row[10] not in ['P', '', 'GRADE']:
            data[row[0]] = [row[1], row[10]]
            data.update(data)
    fhandler.close()

    new_data = {}
    for value in data.itervalues():
        if value[0] not in new_data.iterkeys():
            val1 = 1
            val2 = GRADES[value[1]]
        else:
            val1 = new_data[value[0]][0] + 1
            val2 = new_data[value[0]][1] + GRADES[value[1]]
        new_data[value[0]] = (val1, val2)
        new_data.update(new_data)

    final_data = {}
    for key in new_data.iterkeys():
        val1 = new_data[key][0]
        val2 = new_data[key][1]/new_data[key][0]
        final_data[key] = (val1, val2)
    return final_data


def get_market_density(filename):
    """Function takes one argument, loads a file and returns a dictionary.
    Args:
        filename(file): a file
    Return: a dictionary
    Examples:
        >>> get_market_density('green_markets.json')
        {u'Bronx': 32, u'Brooklyn': 48,
        u'Staten Island': 2, u'Manhattan': 39,
        u'Queens': 16}
    """
    fhandler = open(filename, 'r')
    all_data = json.load(fhandler)
    new_data = all_data["data"]
    final_data = {}
    fhandler.close()
    for data in new_data:
        data[8] = data[8].strip()
        if data[8] not in final_data.iterkeys():
            val = 1
        else:
            val = final_data[data[8]] + 1
        final_data[data[8]] = val
        final_data.update(final_data)
    return final_data


def correlate_data(file1='inspection_results.csv',
                   file2='green_markets.json',
                   file3='result.json'):
    """Takes three arguments and combines the data into a single dictionary.
        Args:
            file1(file): inspection.csv file with restaurant scores data
            file2(file): green_markets.json file containing market data
            file3(file): contain the output of this functon
        Returns: file3 with new data
    """
    data1 = get_score_summary(file1)
    data2 = get_market_density(file2)
    result = {}
    for key2 in data2.iterkeys():
        for key1 in data1.iterkeys():
            if key1 == str(key2).upper():
                val1 = data1[key1][1]
                val2 = float(data2[key2])/(data1[key1][0])
                result[key2] = (val1, val2)
                result.update(result)
    jdata = json.dumps(result)
    fhandler = open(file3, 'w')
    fhandler.write(jdata)
    fhandler.close()
