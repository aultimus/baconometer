#!/usr/bin/env python3

import csv
from collections import Counter


def check_csv_duplicates(csv_path):
    counts = Counter()
    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Clean and normalize
            name = row["name"].strip().lower()
            counts[name] += 1

    # Filter for duplicates
    duplicates = {name: count for name, count in counts.items() if count > 1}

    if duplicates:
        print("Duplicates found (sorted by count descending):")
        # Sort by count descending
        sorted_dupes = sorted(duplicates.items(), key=lambda x: x[1], reverse=True)
        for name, count in sorted_dupes:
            print(f"'{name}' occurs {count} times.")
    else:
        print("No duplicates found.")


if __name__ == "__main__":
    check_csv_duplicates("actors.csv")
