import re
import os
import pandas as pd
import numpy as np
from scipy.optimize import minimize
from scipy.optimize import Bounds

class VolatilityModel:
    def __init__(self, file_path):
        self.file_path = file_path
        self.expiry_data = None
        self.F0_matrix = None
        self.K_matrix = None
        self.best_parameters = None
        self.T_vector = None
        self.initialize_model()

    def initialize_model(self):
        match = re.search(r'(\d+)(mo|yr)\.csv', self.file_path, re.IGNORECASE)   
        if match:
            a = int(match.group(1))
            unit = match.group(2).lower()
            if unit == "mo":
                x = a
            elif unit == "yr":
                x = 12 * a
            else:
                raise ValueError("Orz.")
            self.T_vector = np.ones(7) * (x / 12)
            print("x == ", x)

        else:
            raise ValueError("Orz.")

    def load_and_prepare_data(self):
        self.expiry_data = pd.read_csv(self.file_path)
        self.expiry_data = self.expiry_data.iloc[:12, :9]
        print(self.expiry_data)
        self.expiry_data['Tenor'] = self.expiry_data['Tenor'].str.replace(
            'Yr', '').astype(int)
        self.expiry_data['F0'] = self.expiry_data['F0'] / 100
        self.expiry_data[['ATM-50', 'ATM-25', 'ATM-5', 'ATM', 'ATM+5', 'ATM+25', 'ATM+50']] = \
            self.expiry_data[['ATM-50', 'ATM-25', 'ATM-5',
                              'ATM', 'ATM+5', 'ATM+25', 'ATM+50']] / 10000

    def calculate_matrices(self):
        F0_ATM_column = self.expiry_data['F0'].values
        self.F0_matrix = np.tile(F0_ATM_column, (7, 1)).T
        difference = np.array([-50, -25, -5, 0, 5, 25, 50]) / 10000
        difference_matrix = np.tile(difference, (len(self.expiry_data), 1))
        self.K_matrix = self.F0_matrix + difference_matrix

    def sigma_n(self, T, K, F0, sigma0, alpha, rho, beta=0.5):
        F_mid = (F0 + K) / 2
        C_F_mid = F_mid ** beta
        C_1_derivative = beta * (F_mid ** (beta - 1))
        C_2_derivative = beta * (beta - 1) * (F_mid ** (beta - 2))
        gamma_1 = C_1_derivative / C_F_mid
        gamma_2 = C_2_derivative / C_F_mid
        xi = (alpha / (sigma0 * (1 - beta))) * \
            (F0 ** (1 - beta) - K ** (1 - beta))
        epsilon = T * (alpha ** 2)
        delta = np.log(
            (np.sqrt(1 - 2 * rho * xi + xi ** 2) + xi - rho) / (1 - rho))
        sigma_n = alpha * ((F0 - K) / delta) * (1 + epsilon * (((2 * gamma_2 - gamma_1 ** 2) / 24) *
                                                               ((sigma0 * C_F_mid / alpha) ** 2) + ((rho * gamma_1) / 4) * (sigma0 * C_F_mid / alpha) + (2 - 3 * rho ** 2) / 24))
        return sigma_n

    def optimize_parameters(self):
        market_volatility = self.expiry_data[[
            'ATM-50', 'ATM-25', 'ATM-5', 'ATM', 'ATM+5', 'ATM+25', 'ATM+50']]
        best_parameters = []
        bounds = Bounds([0.001, 0.001, -0.99], [0.99, 0.99, 0.99])  
        for i in range(len(self.expiry_data['Tenor'])):
            def minimize_error(parameter):
                sigma0, alpha, rho = parameter
                errors = self.sigma_n(self.T_vector, self.K_matrix[i, :], self.F0_matrix[i, :],
                                      sigma0, alpha, rho) - market_volatility.iloc[i, :]
                return np.sum(errors**2)

            start_parameter = np.array([0.2, 0.2, 0])  
            result = minimize(minimize_error, start_parameter, bounds=bounds)
            best_parameters.append(result.x)

        self.best_parameters = pd.DataFrame(
            data=best_parameters, columns=['sigma0', 'alpha', 'rho'])
        self.best_parameters.insert(0, 'Tenor', self.expiry_data['Tenor'])
        self.best_parameters['beta'] = 0.5

    def save_parameters_to_csv(self, output_file):
        self.best_parameters.to_csv(output_file, index=False)

    def generate_output_filename(self):
        match = re.search(r'(\d+)(mo|yr)\.csv', self.file_path, re.IGNORECASE)
        if match:
            a = match.group(1)
            unit = match.group(2).lower()
            return f"Best_parameter_{a}_{unit}.csv"
        else:
            raise ValueError("Orz.")

    def run(self):
        self.load_and_prepare_data()
        self.calculate_matrices()
        self.optimize_parameters()
        output_file = self.generate_output_filename()
        self.save_parameters_to_csv(output_file)

def process_folder(base_folder):
    for root, dirs, files in os.walk(base_folder):
        if 'output' in dirs:
            output_path = os.path.join(root, 'output')
            parameter_path = os.path.join(output_path, 'parameter')
            os.makedirs(parameter_path, exist_ok=True)
            process_output_folder(output_path, parameter_path)

def process_output_folder(output_path, parameter_path):
    for filename in os.listdir(output_path):
        if re.match(r'(\d+)(mo|yr)\.csv', filename, re.IGNORECASE):
            file_path = os.path.join(output_path, filename)
            model = VolatilityModel(file_path)
            model.run()
            output_file = model.generate_output_filename()
            model.save_parameters_to_csv(os.path.join(parameter_path, output_file))
        else:
            print(f"Skipped: {filename} (File does not match pattern)")


if __name__ == "__main__":
    base_folder = '/Users/shuyuren/Desktop/data/dd/' 
    process_folder(base_folder)