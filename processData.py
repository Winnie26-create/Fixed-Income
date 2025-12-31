import pandas as pd
import os
import re


class ATMDataProcessor:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.data_dict = {}
        self.output_df_dict = {}

    def read_data(self):
        files = [os.path.join(self.folder_path, file) for file in os.listdir(
            self.folder_path) if file.endswith('.csv')]
        for file in files:
            match = re.search(r'(ATM[-+]?[0-9]*)', os.path.basename(file))
            if match:
                key = match.group(1)
            else:
                raise ValueError('ATM number not found in file name')

            data = pd.read_csv(file, header=[0], nrows=14)
            data = data.iloc[:, :8]
            self.data_dict[key] = data

    def process_data(self):
        columns = ['F0', 'ATM-50', 'ATM-25', 'ATM-5',
                   'ATM', 'ATM+5', 'ATM+25', 'ATM+50']
        year_index = ['1Yr', '2Yr', '3Yr', '4Yr', '5Yr', '7Yr']

        for key in self.data_dict:
            for row_idx in [0, 2, 4, 6, 8, 10, 12]:
                if row_idx in self.data_dict[key].index:
                    expiry_key = self.data_dict[key].loc[row_idx, 'Expiry']
                    if expiry_key not in self.output_df_dict:
                        self.output_df_dict[expiry_key] = pd.DataFrame( index=year_index, columns=columns)
                    for year in year_index:
                        if year in self.data_dict[key].columns:
                            self.output_df_dict[expiry_key].loc[year, key] = self.data_dict[key].loc[row_idx, year]
                            if key == 'ATM':
                                self.output_df_dict[expiry_key].loc[year,'F0'] = self.data_dict[key].loc[row_idx + 1, year]

    def save_data(self):
        output_dir = os.path.join(self.folder_path, 'output')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for key, df in self.output_df_dict.items():
            output_path = os.path.join(output_dir, f"{key}.csv")
            df.to_csv(output_path, header=True, index_label='Tenor')


base_folder = '/Users/shuyuren/Desktop/data/dd/202004'

for folder_name in os.listdir(base_folder):
    folder_path = os.path.join(base_folder, folder_name)
    if os.path.isdir(folder_path):
        print(f"Processing data in folder: {folder_path}")
        processor = ATMDataProcessor(folder_path)
        processor.read_data()
        processor.process_data()
        processor.save_data()