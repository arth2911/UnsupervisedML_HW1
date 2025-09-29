import sys

def normalize_column(values, lower, upper):
    min_val = min(values)
    max_val = max(values)
    normalized = []
    for v in values:
        if max_val == min_val:
            # Avoid division by zero if all values are equal
            normalized.append(lower)
        else:
            norm = lower + (upper - lower) * (v - min_val) / (max_val - min_val)
            normalized.append(norm)
    return normalized

def main():
    if len(sys.argv) != 5:
        print("Usage: python normalize.py <file_path> <lower> <upper> <precision>")
        sys.exit(1)

    file_path = sys.argv[1]
    lower = float(sys.argv[2])
    upper = float(sys.argv[3])
    precision = int(sys.argv[4])

    # Read the file
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            if line.strip():
                row = [float(x) for x in line.strip().split()]
                data.append(row)

    # Transpose to normalize column-wise
    columns = list(zip(*data))
    normalized_columns = []
    for col in columns:
        normalized_columns.append(normalize_column(col, lower, upper))

    # Transpose back to row-wise
    normalized_data = list(zip(*normalized_columns))

    # Print normalized data
    fmt = f"{{:.{precision}f}}"
    for row in normalized_data:
        print(" ".join(fmt.format(x) for x in row))

if __name__ == "__main__":
    main()
