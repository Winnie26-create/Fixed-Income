import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_parameters_and_save_image(csv_file_path, output_dir):

    data = pd.read_csv(csv_file_path)

    data['Date'] = pd.to_datetime(data['Date'], format='%Y%m%d')

    plt.figure(figsize=(14, 7))
    plt.plot(data['Date'], data['sigma_0'], label='sigma_0')
    plt.plot(data['Date'], data['alpha'], label='alpha')
    plt.plot(data['Date'], data['rho'], label='rho')

    plt.legend()

    plt.title('Parameter Time Series')
    plt.xlabel('Date')
    plt.ylabel('Parameter Value')

    plt.gcf().autofmt_xdate()

    file_name_without_extension = os.path.splitext(os.path.basename(csv_file_path))[0]

    image_file_path = os.path.join(output_dir, f"{file_name_without_extension}.jpg")
    plt.savefig(image_file_path)
    plt.close()  
    print(f"Image saved to {image_file_path}")


def process_csv_files_in_directory(directory):

    for file_name in os.listdir(directory):
        if file_name.endswith('.csv'):

            csv_file_path = os.path.join(directory, file_name)

            plot_parameters_and_save_image(csv_file_path, directory)


expiry_tenor_directory = '/Users/shuyuren/Desktop/data/dd/Expiry_Tenor(42)' 
process_csv_files_in_directory(expiry_tenor_directory)
