import sys
from collections import set

def main():
    if len(sys.argv) != 2:
        print("Usage: python itemsets2sparsearff.py <input_file>", file=sys.stderr)
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    try:
        # Read the input file and collect all unique items
        transactions = []
        all_items = set()
        
        with open(input_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line:  # Skip empty lines
                    items = line.split()
                    transactions.append(items)
                    all_items.update(items)
        
        # Sort items for consistent ordering
        sorted_items = sorted(all_items)
        
        # Generate sparse ARFF output
        print("@relation itemsets")
        print()
        
        # Output attribute declarations
        for item in sorted_items:
            print(f"@attribute {item} {{0,1}}")
        print()
        
        # Output data section
        print("@data")
        
        # Convert each transaction to sparse format
        for transaction in transactions:
            # Create sparse representation: {index value, index value, ...}
            sparse_items = []
            for i, item in enumerate(sorted_items):
                if item in transaction:
                    sparse_items.append(f"{i} 1")
            
            if sparse_items:
                print("{" + ", ".join(sparse_items) + "}")
            else:
                print("{}")  # Empty transaction
                
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()