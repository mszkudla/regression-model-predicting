import pandas as pd
import os
import shutil


# Count the number of breaks (line breaks, spaces, or tabs) in a line
def count_breaks(line):
    return line.count(' ') + line.count('\t')


def split_and_save_data(input_file, output_file):
    try:
        with open(input_file, 'r') as file:
            # Read the first line to get the expected break count
            first_line = file.readline()
            expected_count = count_breaks(first_line)

            # Check if each line has the same break count as the first line
            for line in file:
                if count_breaks(line) != expected_count:
                    print(f"Missing data in '{input_file}'\n")
                    return

        df = pd.read_csv(input_file, sep='\t', na_values='(null)').fillna(0)

        # typo in FlownPassengers column name
        df = df.rename(columns={'FLownPassengers': 'FlownPassengers'})

        # convert strings to unique integers
        df['DepartureAirport'] = pd.factorize(df['DepartureAirport'])[0]
        df['ArrivalAirport'] = pd.factorize(df['ArrivalAirport'])[0]
        df['Route'] = pd.factorize(df['Route'])[0]
        df['DepartureDate'] = pd.factorize(df['DepartureDate'])[0]

        df.to_csv(output_file, index=False)
        print(f"Data has been successfully split and saved to {output_file}")

        directory = 'input_refactor'
        if not os.path.exists(directory):
            os.makedirs(directory)
            print("Directory 'input_refactor' created successfully.")

        destination_path = os.path.join(directory, output_file)
        shutil.move(output_file, destination_path)
        print(f"File '{output_file}' moved to the 'input_refactor' directory.")

    except FileNotFoundError:
        print(f"File not found: {input_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


split_and_save_data('input/training.csv', 'training_refactor.csv')
split_and_save_data('input/validation.csv', 'validation_refactor.csv')
