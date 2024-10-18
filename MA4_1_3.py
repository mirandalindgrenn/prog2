"""
Solutions to module 4
Review date:
"""

student = "Miranda Lindgren"  # Skriv ditt namn här
reviewer = "DDD"  # Skriv din reviewers namn här

import math as m
import random as r
from time import perf_counter as pc
import ast
from concurrent.futures import ProcessPoolExecutor, as_completed

def sphere_volume(n, d):
    # Skapa en lista med n punkter där varje punkt har d koordinater
    n_points = [[r.uniform(-1, 1) for _ in range(d)] for _ in range(n)]  # List Comprehension
    # Testa om varje punkt ligger inom hypersfären
    inside_sphere = sum(1 for point in n_points if sum(map(lambda x: x**2, point)) <= 1)  # Lambda och map()
    
    # Approximation av volymen
    volume_estimate = (2 ** d) * (inside_sphere / n)
    return volume_estimate 

def hypersphere_exact(n, d):
    exact_volume = (m.pi ** (d / 2)) / m.gamma(d / 2 + 1)
    return exact_volume  # Returnerar den exakta volymen

# Parallellisering av en loop för att beräkna volymen
def sphere_volume_parallel1(n, d, np=8):
    with ProcessPoolExecutor(max_workers=np) as executor:
        # Dela upp n punkter bland processerna
        futures = [executor.submit(sphere_volume, n // np, d) for _ in range(np)]
        
        # Samla resultaten
        results = [future.result() for future in as_completed(futures)]
    
    # Beräkna genomsnittlig uppskattad volym
    average_volume = sum(results) / len(results)
    return average_volume

# Parallellisering av själva beräkningarna genom att dela upp data
def sphere_volume_parallel2(n, d, np=8):
    points_per_process = n // np
    futures = []

    # Skapa och dela upp punkterna mellan processerna
    with ProcessPoolExecutor(max_workers=np) as executor:
        for _ in range(np):
            # Generera punkter för varje process
            futures.append(executor.submit(generate_points_and_count, points_per_process, d))

        # Samla resultaten
        inside_sphere_counts = [future.result() for future in as_completed(futures)]
    
    # Total räkning av punkter inom sfären
    inside_sphere = sum(inside_sphere_counts)

    # Approximation av volymen
    volume_estimate = (2 ** d) * (inside_sphere / n)
    return volume_estimate

# Hjälpfunktion för att räkna hur många punkter som ligger inom hypersfären
def generate_points_and_count(n, d):
    inside_sphere = 0
    for _ in range(n):
        point = [r.uniform(-1, 1) for _ in range(d)]
        if sum(map(lambda x: x**2, point)) <= 1:  # Kontrollera om den ligger inom sfären
            inside_sphere += 1
    return inside_sphere

def check_higher_order_functions(file_path):
    try:
        with open(file_path, "r") as source_file:
            source_code = source_file.read()

        # Parse the file content
        tree = ast.parse(source_code)
        checker = HighOrderFunctionChecker()
        checker.visit(tree)

        if not checker.found_higher_order:
            print("No higher-order functions, lambdas, or comprehensions found.")
        return checker.found_higher_order
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return False
    except SyntaxError as e:
        print(f"Syntax error in file '{file_path}': {e}")
        return False

class HighOrderFunctionChecker(ast.NodeVisitor):
    def __init__(self):
        self.found_higher_order = False

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id in {"map", "filter", "reduce", "sorted"}:
            print(f"Higher-order function '{node.func.id}' found at line {node.lineno}")
            self.found_higher_order = True
        if isinstance(node.func, ast.Attribute) and node.func.attr in {"map", "filter", "reduce", "sorted"}:
            print(f"Higher-order function '{node.func.attr}' found at line {node.lineno} in module '{node.func.value.id}'")
            self.found_higher_order = True
        for arg in node.args:
            if isinstance(arg, ast.Lambda):
                print(f"Lambda function used as argument in '{node.func.id if isinstance(node.func, ast.Name) else node.func.attr}' at line {node.lineno}")
                self.found_higher_order = True
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        for arg in node.args.args:
            if isinstance(arg.annotation, ast.Name) and arg.annotation.id == 'function':
                print(f"Custom higher-order function '{node.name}' found at line {node.lineno}")
                self.found_higher_order = True
        for body_item in node.body:
            if isinstance(body_item, ast.Lambda):
                print(f"Lambda function defined inside function '{node.name}' at line {node.lineno}")
                self.found_higher_order = True
        self.generic_visit(node)

    def visit_Lambda(self, node):
        print(f"Lambda function found at line {node.lineno}")
        self.found_higher_order = True
        self.generic_visit(node)

    def visit_ListComp(self, node):
        print(f"List comprehension found at line {node.lineno}")
        self.found_higher_order = True
        self.generic_visit(node)

    def visit_SetComp(self, node):
        print(f"Set comprehension found at line {node.lineno}")
        self.found_higher_order = True
        self.generic_visit(node)

    def visit_DictComp(self, node):
        print(f"Dictionary comprehension found at line {node.lineno}")
        self.found_higher_order = True
        self.generic_visit(node)

    def visit_GeneratorExp(self, node):
        print(f"Generator comprehension found at line {node.lineno}")
        self.found_higher_order = True
        self.generic_visit(node)

def main():
    # Del 1: Parallellisering av en loop bland processer
    n = 100000
    d = 11
    np = 8  # Antal processer

    # Tidmätning för sekventiell beräkning
    start_time = pc()
    estimated_volume = sphere_volume(n, d)
    end_time = pc()
    print(f"Approximerad volym (sekventiellt) för (n={n}, d={d}): {estimated_volume}")
    print(f"Tid (sekventiellt): {end_time - start_time:.4f} sekunder")

    # Tidmätning för parallellisering av loop
    start_time = pc()
    estimated_volume_parallel1 = sphere_volume_parallel1(n, d, np)
    end_time = pc()
    print(f"Approximerad volym (parallellt, loop) för (n={n}, d={d}): {estimated_volume_parallel1}")
    print(f"Tid (parallellt, loop): {end_time - start_time:.4f} sekunder")

    # Tidmätning för parallellisering av själva beräkningarna
    start_time = pc()
    estimated_volume_parallel2 = sphere_volume_parallel2(n, d, np)
    end_time = pc()
    print(f"Approximerad volym (parallellt, beräkningar) för (n={n}, d={d}): {estimated_volume_parallel2}")
    print(f"Tid (parallellt, beräkningar): {end_time - start_time:.4f} sekunder")

    # Beräkna den exakta volymen
    exact_volume = hypersphere_exact(n, d)
    print(f"Exakt volym för (d={d}): {exact_volume}")

    # Kontrollera användning av högre ordningens funktioner
    check_higher_order_functions(__file__)

if __name__ == '__main__':
    main()