import random
import time
import tracemalloc
import csv
import matplotlib.pyplot as plt


# ---------------------------------------------------
# MERGE SORT
# ---------------------------------------------------
def merge_sort(arr):
    """
    Sorts a list using the Merge Sort algorithm.
    Returns a new sorted list.
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    return merge(left_half, right_half)


def merge(left, right):
    """
    Merges two sorted lists into one sorted list.
    """
    merged = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # Add any remaining elements
    merged.extend(left[i:])
    merged.extend(right[j:])

    return merged


# ---------------------------------------------------
# QUICK SORT
# ---------------------------------------------------
def quick_sort(arr):
    """
    Sorts a list using the Quick Sort algorithm.
    Returns a new sorted list.
    """
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]

    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)


# ---------------------------------------------------
# DATA GENERATION FUNCTIONS
# ---------------------------------------------------
def generate_sorted_data(n):
    """
    Generates a sorted list of size n.
    """
    return list(range(n))


def generate_reverse_sorted_data(n):
    """
    Generates a reverse sorted list of size n.
    """
    return list(range(n, 0, -1))


def generate_random_data(n):
    """
    Generates a random list of size n.
    """
    return [random.randint(1, 100000) for _ in range(n)]


# ---------------------------------------------------
# PERFORMANCE MEASUREMENT FUNCTIONS
# ---------------------------------------------------
def measure_time(sort_function, data):
    """
    Measures execution time of a sorting function.
    Returns time in seconds.
    """
    data_copy = data.copy()
    start_time = time.perf_counter()
    sort_function(data_copy)
    end_time = time.perf_counter()
    return end_time - start_time


def measure_memory(sort_function, data):
    """
    Measures peak memory usage of a sorting function.
    Returns memory usage in bytes.
    """
    data_copy = data.copy()
    tracemalloc.start()
    sort_function(data_copy)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak


# ---------------------------------------------------
# EXPERIMENT FUNCTION
# ---------------------------------------------------
def run_experiments():
    """
    Runs performance tests on Merge Sort and Quick Sort
    using sorted, reverse sorted, and random datasets.
    """
    sizes = [1000, 5000, 10000]
    results = []

    for size in sizes:
        datasets = {
            "Sorted": generate_sorted_data(size),
            "Reverse Sorted": generate_reverse_sorted_data(size),
            "Random": generate_random_data(size)
        }

        for dataset_name, data in datasets.items():
            # Measure Merge Sort
            merge_time = measure_time(merge_sort, data)
            merge_memory = measure_memory(merge_sort, data)

            # Measure Quick Sort
            quick_time = measure_time(quick_sort, data)
            quick_memory = measure_memory(quick_sort, data)

            # Store results
            results.append({
                "Dataset Type": dataset_name,
                "Size": size,
                "Merge Sort Time (s)": merge_time,
                "Merge Sort Memory (bytes)": merge_memory,
                "Quick Sort Time (s)": quick_time,
                "Quick Sort Memory (bytes)": quick_memory
            })

            # Print results to console
            print(f"Dataset: {dataset_name}, Size: {size}")
            print(f"  Merge Sort -> Time: {merge_time:.6f}s, Memory: {merge_memory} bytes")
            print(f"  Quick Sort -> Time: {quick_time:.6f}s, Memory: {quick_memory} bytes")
            print("-" * 60)

    return results


# ---------------------------------------------------
# SAVE RESULTS TO CSV
# ---------------------------------------------------
def save_results_to_csv(results, filename="results.csv"):
    """
    Saves experiment results to a CSV file.
    """
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print("Results saved successfully.")


# ---------------------------------------------------
# PLOT RESULTS
# ---------------------------------------------------
def plot_results(results):
    """
    Plots execution time comparison for Merge Sort and Quick Sort.
    """
    dataset_types = ["Sorted", "Reverse Sorted", "Random"]

    for dataset_type in dataset_types:
        filtered = [r for r in results if r["Dataset Type"] == dataset_type]

        sizes = [r["Size"] for r in filtered]
        merge_times = [r["Merge Sort Time (s)"] for r in filtered]
        quick_times = [r["Quick Sort Time (s)"] for r in filtered]

        plt.figure(figsize=(8, 5))
        plt.plot(sizes, merge_times, marker='o', label='Merge Sort')
        plt.plot(sizes, quick_times, marker='o', label='Quick Sort')

        plt.title(f"Execution Time on {dataset_type} Data")
        plt.xlabel("Input Size")
        plt.ylabel("Time (seconds)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()


# ---------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------
if __name__ == "__main__":
    results = run_experiments()
    save_results_to_csv(results)
    plot_results(results)