import os
import sys
import csv
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# idk why we have to do this tbh
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.helpers.dmaics_parser import parse_multi_instance_dimacs
from src.sat import SatSolver

def run_solver_and_write_csv(instances, out_csv, method_name, solver_func):
    #running solver and writing the results to our CSV files
    os.makedirs(os.path.dirname(out_csv) or ".", exist_ok=True)
    nvars_list, times_list, sat_flags = [], [], []

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["instance_id", "n_vars", "n_clauses", "method", "satisfiable", "time_seconds", "solution"])

        #timing each instance for graphing purposes
        for (inst_id, n_vars, clauses) in instances:
            n_clauses = len(clauses)
            t0 = time.perf_counter()
            ok, assign = solver_func(n_vars, clauses)
            dt = time.perf_counter() - t0

            sat_flag = "S" if ok else "U"
            sol_str = str(assign) if ok else "{}"

            w.writerow([inst_id, n_vars, n_clauses, method_name, sat_flag, dt, sol_str])

            nvars_list.append(n_vars)
            times_list.append(dt)
            sat_flags.append(ok)

    return nvars_list, times_list, sat_flags


def read_team_inputs(input_file, results_folder):
    #parsing input file and generating CSV files for each solving method
    os.makedirs(results_folder, exist_ok=True)
    
    #using parsing helper method
    instances = parse_multi_instance_dimacs(input_file)

    solver = SatSolver(input_file)
    
    #paths for CSV files
    brute_csv = os.path.join(results_folder, "brute_force_results.csv")
    back_csv = os.path.join(results_folder, "backtracking_results.csv")
    
    #brute force solver
    run_solver_and_write_csv(instances, brute_csv, "BruteForce", solver.sat_bruteforce)
    
    #backtracking solverr
    run_solver_and_write_csv(instances, back_csv, "BackTracking", solver.sat_backtracking)
    
    return brute_csv, back_csv


def plot_brute_vs_backtrack(brute_csv, back_csv, output_name="plot_brute_vs_backtrack.png"):
    #read CSV files
    brute_df = pd.read_csv(brute_csv)
    back_df = pd.read_csv(back_csv)

    plt.figure(figsize=(12, 6))
    added_labels = set()

    #helper function
    def plot_method(df, method_name, color_base):
        unsat_sizes, unsat_times = [], []
        
        for i in range(len(df)):
            size = df.loc[i, "n_vars"]
            time_val = df.loc[i, "time_seconds"]
            sat_flag = df.loc[i, "satisfiable"] == "S"

            if sat_flag:
                label = f"{method_name} (Sat)"
                color = color_base
                marker = "o"
            else:
                label = f"{method_name} (Unsat)"
                color = "red" if color_base == "blue" else "orange"
                marker = "^"
                unsat_sizes.append(size)
                unsat_times.append(time_val)

            if label not in added_labels:
                plt.scatter(size, time_val, color=color, marker=marker, label=label)
                added_labels.add(label)
            else:
                plt.scatter(size, time_val, color=color, marker=marker)
        
        #accounting for expontential fitting in unsat cases
        if len(unsat_sizes) > 1:
            log_unsat_times = np.log(unsat_times)
            fit = np.polyfit(unsat_sizes, log_unsat_times, 1)
            a, b = np.exp(fit[1]), fit[0]

            def exp_fit(x):
                return a * np.exp(b * x)
            sizes_fit = np.linspace(min(unsat_sizes), max(unsat_sizes), 100)
            times_fit = exp_fit(sizes_fit)
            plt.plot(
                sizes_fit,
                times_fit,
                '--',
                color=color_base,
                label=f'{method_name} Best Fit: y={a:.2e}*e^({b:.2f}x)'
            )

    plot_method(brute_df, "BruteForce", "blue")
    plot_method(back_df, "BackTracking", "green")

    #formats
    plt.xlabel("Number of Variables")
    plt.ylabel("Execution Time (s)")
    plt.title("SAT Solver Comparison: Brute Force vs. Backtracking")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(output_name)
    plt.show()


def main():
    if len(sys.argv) < 3:
        print("Try: uv run src/team_sat.py input/team_tests.cnf results")
        sys.exit(1)

    input_file = sys.argv[1]
    #print(input_file)
    results_folder = sys.argv[2]
    #print(results_folder)

    brute_csv, back_csv = read_team_inputs(input_file, results_folder)

    if brute_csv and back_csv:
        plot_path = os.path.join(results_folder, "plot_brute_vs_backtrack.png")
        plot_brute_vs_backtrack(brute_csv, back_csv, plot_path)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
