def process_numbers(filename):
    total = 0
    count = 0

    try:
        with open(filename, "r") as file:
            for line in file:
                try:
                    number = int(line.strip())
                    total += number
                    count += 1
                except ValueError:
                    print(f"Skipping invalid number: {line.strip()}")

    except FileNotFoundError:
        print(f"Error: {filename} was not found.")

    finally:
        print(f"Sum: {total}")
        print(f"Valid numbers: {count}")

process_numbers("data_item66.dat")  # Specify the path to your file here    
