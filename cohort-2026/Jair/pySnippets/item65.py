def process_data(file_path):
    file = None
    try:
        # 1. The Risky Code
        print("--- Entering 'try' block ---")
        file = open(file_path, "r")
        content = file.readline()
        number = int(content.strip())
        print("Read number from file:", number)
        result = 100 / number

    except FileNotFoundError:
        # 2. Executed if the file does not exist
        print("--- Entering 'except' block ---")
        print("Error: The specified file was not found.")

    except ZeroDivisionError:
        # 2. Executed if the file contains the number 0
        print("--- Entering 'except' block ---")
        print("Error: Cannot divide by zero.")

    except ValueError:
        # 2. Executed if the file contains text instead of an integer
        print("--- Entering 'except' block ---")
        print("Error: File content could not be converted to a number.")
        print("content", content)

    else:
        # 3. Executed ONLY if the try block succeeds without any errors
        print(f"Success! The calculated result is: {result}")

    finally:
        # 4. Executed ALWAYS, ensuring resources are freed up
        print("--- Entering 'finally' block ---")
        if file:
            file.close()
            print("File resource closed successfully.")


file = "data_item65.dat"  # Specify the path to your file here
process_data(file)

