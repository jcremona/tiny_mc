import csv


def save_log_info(log_info, fieldnames, path):
    # Save a results.csv file containing the results of the exploration
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(log_info)


def load_log_info(path):
    # Read a results.csv file and plot its content
    with open(path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)
