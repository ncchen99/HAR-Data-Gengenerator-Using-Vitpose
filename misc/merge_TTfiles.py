import os
import pandas as pd

def merge_info_files(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i in range(7):
        # Construct file names
        info_file_1 = os.path.join(input_folder, f"{i}+_info.csv")
        info_file_2 = os.path.join(input_folder, f"{i}-_info.csv")
        output_info_file = os.path.join(output_folder, f"{i}_info.csv")

        # Read and merge info files
        if os.path.exists(info_file_1) and os.path.exists(info_file_2):
            df_info_1 = pd.read_csv(info_file_1, header=None)
            df_info_2 = pd.read_csv(info_file_2, header=None)
            df_merged_info = pd.concat([df_info_1, df_info_2], ignore_index=True)
            df_merged_info.to_csv(output_info_file, index=False, header=False)
            print(f"Info files merged for index {i}: {output_info_file}")

def merge_data_files(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i in range(7):
        # Construct file names
        data_file_1 = os.path.join(input_folder, f"{i}+_data.csv")
        data_file_2 = os.path.join(input_folder, f"{i}-_data.csv")
        output_data_file = os.path.join(output_folder, f"{i}_data.csv")

        # Read and merge data files
        if os.path.exists(data_file_1) and os.path.exists(data_file_2):
            df_data_1 = pd.read_csv(data_file_1)
            df_data_2 = pd.read_csv(data_file_2, header=None, skiprows=1)
            # tmp_df['Category'] = category  # Add category column for identification
            df_data_2.columns = df_data_1.columns
            df_merged_data = pd.concat([df_data_1, df_data_2], ignore_index=True)
            df_merged_data.to_csv(output_data_file, index=False)
            print(f"Data files merged for index {i}: {output_data_file}")

def main():
    # Define input and output folders for train and test
    base_folder = 'data'  # Change this to your base folder path
    folders = ['train', 'test']
    
    for folder in folders:
        input_folder = os.path.join(base_folder, folder)
        output_folder = os.path.join(base_folder, f"{folder}_merged")

        # Merge info and data files
        merge_info_files(input_folder, output_folder)
        merge_data_files(input_folder, output_folder)

if __name__ == "__main__":
    main()
