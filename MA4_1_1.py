"""
Solutions to module 4
Review date:
"""

student = "Miranda Lindgren"
reviewer = "ddd"

import random as r
import math
import matplotlib.pyplot as plt

def approximate_pi(n):
    # Anropa monte_carlo_pi för att uppskatta π
    pi_estimate, x_inside, y_inside, x_outside, y_outside = monte_carlo_pi(n)
    return pi_estimate  # Returnera det uppskattade värdet

def monte_carlo_pi(n):
    inside_circle = 0
    x_inside, y_inside = [], []
    x_outside, y_outside = [], []
    
    for _ in range(n):
        x, y = r.uniform(-1, 1), r.uniform(-1, 1)
        if x**2 + y**2 <= 1:
            inside_circle += 1
            x_inside.append(x)
            y_inside.append(y)
        else:
            x_outside.append(x)
            y_outside.append(y)
    
    pi_estimate = 4 * inside_circle / n
    print(f'Antal punkter inom cirkeln: {inside_circle}')
    print(f'Uppskattning av pi: {pi_estimate}')
    print(f'Inbyggt pi: {math.pi}')

    # Skapa plot
    plt.figure(figsize=(6, 6))
    plt.scatter(x_inside, y_inside, color='red', label='Inom cirkeln')
    plt.scatter(x_outside, y_outside, color='blue', label='Utanför cirkeln')
    plt.legend()
    plt.title(f'Uppskattning av π med {n} punkter')
    plt.savefig(f'pi_estimate_{n}.png')
    #plt.show()

    return pi_estimate, x_inside, y_inside, x_outside, y_outside  # Returnera datan

def main():
    dots = [1000, 10000, 100000]
    for n in dots:
        approximate_pi(n)

if __name__ == '__main__':
    main()
