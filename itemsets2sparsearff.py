import sys
import time

# Track execution time
start_time = time.perf_counter()

# Read CLI arguments and ensure they are correct
try:
    if len(sys.argv) != 2:
        print("Usage: python itemsets2sparsearff.py <input_file>")
        sys.exit(1)
    
    file_name = sys.argv[1]
    with open(file_name, 'r') as dat_file:
        lines = dat_file.readlines()
except FileNotFoundError:
    print(f"Error: File '{sys.argv[1] if len(sys.argv) > 1 else 'unknown'}' not found!")
    sys.exit(1)
except Exception as e:
    print(f"Error reading file: {e}")
    sys.exit(1)

# Create the ARFF file
arff_file_name = file_name.split('.')[0] + ".arff"

try:
    with open(arff_file_name, 'w') as arff_file:
        arff_file.write(f"@RELATION {file_name.split('.')[0]}\n\n")
        
        # Store ARFF data and track maximum column number
        arff_data = []
        total_cols = 0
        
        # Process each line from input file
        for line in lines:
            line = line.strip()
            if not line:  # Skip empty lines
                continue
                
            # Get unique values and convert to integers
            try:
                data = set(line.split())
                data = sorted([int(x) for x in data if x.isdigit()])
                
                if not data:  # Skip lines with no valid integers
                    arff_data.append("{}\n")
                    continue
                
                # Create ARFF line in sparse format
                arff_line = "{"
                for col in data:
                    arff_line += f"{col - 1} 1, "
                    total_cols = max(total_cols, col)
                
                # Remove trailing comma and space, then close brace
                arff_line = arff_line.rstrip(", ") + "}\n"
                arff_data.append(arff_line)
                
            except ValueError:
                print(f"Warning: Skipping line with invalid data: {line}")
                continue
        
        # Write attribute definitions
        for attribute in range(1, total_cols + 1):
            arff_file.write(f"@ATTRIBUTE i{attribute} {{0,1}}\n")
        
        arff_file.write("\n@DATA\n")
        
        # Write the data
        for line in arff_data:
            arff_file.write(line)

except Exception as e:
    print(f"Error writing ARFF file: {e}")
    sys.exit(1)

# Calculate and display runtime
end_time = time.perf_counter()
print(f"Successfully created '{arff_file_name}'")
print(f"Total attributes: {total_cols}")
print(f"Total transactions: {len(arff_data)}")
print(f"Execution time: {end_time - start_time:.4f} seconds")