#!/usr/bin/env python3
"""
piCalc - Using probabilities of prime cofactors to calculate & visualize Pi

This is based on the Pi Day video done by Matt Parker on YouTube (https://www.youtube.com/watch?v=RZBhSi_PwHU)
in 2017. This script is developed using formulas and methodologies from this video, and all credit for that work
belongs to Matt Parker. This script is available for use under the MIT license as well. Please see repository
LICENSE for more details.

This script is designed as a CLI tool connected to a local SQLite database for gathering data for a data
visualization project to show how the values are calcualted and averaged out.


Author: Matthew Sunner, 2022
"""

import random
import math
import sqlite3
import os

import numpy as np

def prime_list_gen(max_pair_value: int, num_of_trials: int) -> int:
    """prime_list_gen - Method to calculate the number of prime number GCD pairs. The 
    function is customized to a user input maximum pair value and set number of trials to run.

    Args:
        max_pair_value (int): Maximum value for coprime computation
        num_of_trials (int): Number of times the computation should run to sum up the number
        of coprime values

    Returns:
        int: Sum of coprime values found out of the number of trials done
    """
    x = 0
    prime_counter = 0
    for x in range(0, num_of_trials):
        # Pair Assignment
        pair_1 = random.randint(0, max_pair_value)
        pair_2 = random.randint(0, max_pair_value)

        if math.gcd(pair_1, pair_2) == 1:
            prime_counter += 1
        
        x += 1
    
    return prime_counter


def prime_array_gen(max_pair_value: int, num_of_trials: int) -> int:
    """prime_array_gen - Rebuild of prime_list_gen function to calculate the number of experimental prime
    number GCD pairs. Uses custom values for random number maximums and the number of trials used to calcualte.

    Args:
        max_pair_value (int): Maximum value for coprime computation
        num_of_trials (int): Number of times the computation should run to sum up the number
        of coprime values

    Returns:
        int: Sum of coprime values found out of the number of trials done
    """
    primes_range_array = np.array([np.gcd(np.random.randint(max_pair_value), np.random.randint(max_pair_value)) for i in range(num_of_trials)])
    filtered_primes_array = np.where(primes_range_array == 1, 1, 0)
    sum_primes = np.sum(filtered_primes_array)

    return sum_primes


def connect_to_db(conn_file: str) -> object:
    """connect_to_db - SQLite3 connection function based on whether or not a db exists.

    Args:
        conn_file (str): Path the database file to be used

    Returns:
        object: SQLite3 connection object
    """
    if os.path.exists(conn_file):
        conn = sqlite3.connect(conn_file)

        return conn
    else:
        conn = sqlite3.connect(conn_file)

        cur.execute('''
                CREATE TABLE results (
                    id integer PRIMARY KEY,
                    result REAL
                ); ''')
        
        return conn


if __name__ == '__main__':
    # SQLite Config
    conn = connect_to_db('primesPi.db')

    cur = conn.cursor()

    # User Inputs
    max = 100_000_000_000
    trials = 100_000
    iterations = int(input('Enter the Number of times the Script Should Calculate Pi: '))

    # Actual Logic Run
    # Looping through the iterations of full trials
    i = 0
    for i in range(0, iterations):
        print('Calculating...')
        primes = prime_array_gen(max, trials)
        prob = primes / trials
        pi_est = math.sqrt(6 / prob)
        cur.execute('INSERT INTO results (result) VALUES (?)', (pi_est,))

        print(f'Trial {i} Completed...Pi = {pi_est}')

        i += 1
    
    # Save all content to the database and close out the connection
    conn.commit()    
    conn.close()