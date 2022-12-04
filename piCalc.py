"""
piCalc - Using probabilities of prime cofactors to calculate & visualize Pi

This is based on the Pi Day video done by Matt Parker on YouTube (LINK)

Author: Matthew Sunner, 2022
"""

import random
import math

# Config

max = 100_000
trials = 100_000_000

def prime_list_gen(max: int) -> list:
    x = 0
    primes = []
    for x in range(0, trials):
        # Pair Assignment
        pair_1 = random.randint(0, max)
        pair_2 = random.randint(0, max)

        if math.gcd(pair_1, pair_2) == 1:
            primes.append(1)
        
        x += 1
    
    return primes

def sum_calc(primes_list: list) -> int:
    ele = 0
    total = 0

    while(ele < len(primes_list)):
        total = total + primes_list[ele]
        ele += 1
    
    return total

if __name__ == '__main__':
    primes = prime_list_gen(max)

    prob = sum_calc(primes) / trials

    pi_est = math.sqrt(6 / prob)

    print(pi_est)

