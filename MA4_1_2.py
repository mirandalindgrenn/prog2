
"""
Solutions to module 4
Review date:
"""

student = "Miranda Lindgren"
reviewer = "DDD"

import math as m
import random as r

# Monte Carlo approximation av hypersfärens volym
def sphere_volume(n, d):
    # Skapa en lista med n punkter där varje punkt har d koordinater
    # Här används List Comprehension för att generera punkterna
    n_points = [[r.uniform(-1, 1) for _ in range(d)] for _ in range(n)]  # List Comprehension, detta är en lista med n stycken listor bestående av d element
    # Testa om varje punkt ligger inom hypersfären genom att summera kvadraten av varje koordinat
    # Använd lambda och map() för att beräkna kvadraterna och summan av koordinaterna
    inside_sphere = sum(1 for point in n_points if sum(map(lambda x: x**2, point)) <= 1)  # Lambda och map(). Kontrollerar så att summan
    #av alla kvadrater av x i varje punkt r mindre än 1 för att då ligger i i sfären med radie 1. sum 1 lägger till 1 för varje punkt
    # som uppfyller kravet till en summa som returneras och används vid uppskattningen av volymen
    
    # Approximation av volymen
    volume_estimate = (2 ** d) * (inside_sphere / n)
    return volume_estimate

# Exakt volym av en hypersfär enligt formeln
def hypersphere_exact(n, d):
    # Använd n för att iterativt beräkna den exakta volymen n gånger
    exact_volume = (m.pi ** (d / 2)) / m.gamma(d / 2 + 1)
    
    # Skapa en lista med exakt volym n gånger (simulering av n punkter som i Monte Carlo)
    exact_volumes = [exact_volume for _ in range(n)]  # Användning av n för att skapa en lista

    # Summera eller returnera genomsnittet av dessa exakta volymer
    return sum(exact_volumes) / n  # Returnerar exakta volymen

def main():
    # Variabler för student och reviewer (behövs för testfilen)
    n = 100000
    d = 2
    print(f"Approximerad volym för (n={n}, d={d}): {sphere_volume(n, d)}")
    print(f"Exakt volym för (d={d}): {hypersphere_exact(n, d)}")

if __name__ == '__main__':
    main()
