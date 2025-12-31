import pandas as pd
import os

def collect_and_save_data(base_dir, target_filename, row_index):
    collected_data = []
    dates = []

    for year_month in sorted(os.listdir(base_dir)):
        year_month_path = os.path.join(base_dir, year_month)
        if not os.path.isdir(year_month_path):  
            continue
        
        for day in sorted(os.listdir(year_month_path)):
            day_path = os.path.join(year_month_path, day)
            if not os.path.isdir(day_path): 
                continue
            
            file_path = os.path.join(day_path, 'output', 'parameter', target_filename)
            if os.path.isfile(file_path):  

                data = pd.read_csv(file_path, header=None, skiprows=row_index, nrows=1).iloc[:, 1:]
                collected_data.append(data)
                dates.append(day)

    if not collected_data:
        print("No data was collected.")
        return pd.DataFrame()
    
    data_df = pd.concat(collected_data, ignore_index=True)
    data_df.insert(0, 'Date', dates)
    
    columns = ['Date', 'sigma_0', 'alpha', 'rho', 'beta']
    final_df = pd.DataFrame(data_df.values, columns=columns)
    return final_df

if __name__ == "__main__":
    base_dir = '/Users/shuyuren/Desktop/data/dd' 
    target_filename = 'Best_parameter_3_yr.csv'
    
    for i in range(1, 7):  
        result_df = collect_and_save_data(base_dir, target_filename, i)  
        
        if not result_df.empty:
            tenor_number = i + 1 if i == 6 else i
            output_file_name = f'Expiry3yr_Tenor{tenor_number}yr.csv'
            output_file_path = os.path.join(base_dir, output_file_name)
            result_df.to_csv(output_file_path, index=False, sep=',', encoding='utf-8', header=True)
            print(f"Data saved to {output_file_path}")
        else:
            print(f"No data to save for Tenor {i}.")
