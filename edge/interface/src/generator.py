# Define a function that generates data as a dictionary
import time
import pandas as pd
import random


class GetDataFrame:
    __instance = None

    @classmethod
    def get_instance(cls, file_path, conditions):
        if cls.__instance is None:
            cls.__instance = cls(file_path=file_path, conditions=conditions)
        return cls.__instance

    def __init__(self, file_path, conditions):
        if GetDataFrame.__instance is not None:
            print("Singleton instance already exists. Skipping creation of new instance.")
            return

        # Get a list of all the fies in the directory
        df = pd.read_csv(file_path)
        self.df = df
        self.df.drop(columns=["Time"], inplace=True)
        self.df.fillna(0, inplace=True)
        self.columns = df.columns
        self.brake_fluid = conditions.get("Brake_fluid")
        self.brake_pad = conditions.get("Brake_pad")
        random_values = random.sample(range(28, 36), 4)

        self.df["Tire Pressure (Front Left) [kPa]"] = random_values[0]
        self.df["Tire Pressure (Front Right) [kPa]"] = random_values[1]
        self.df["Tire Pressure (Rear Left) [kPa]"] = random_values[2]
        self.df["Tire Pressure (Rear Right) [kPa]"] = random_values[3]

        if self.brake_fluid:
            self.df["Brake Fluid Level [%]"] = random.sample(range(20, 25), 1)[0]
        else:
            self.df["Brake Fluid Level [%]"] = random.sample(range(40, 100), 1)[0]

        if not self.brake_pad:
            self.df["Brake Pad Thickness [mm]"] = random.uniform(6.4, 7.9)
        else:
            self.df["Brake Pad Thickness [mm]"] = random.uniform(3.2, 6.4)

    def dataframe(self):
        return self.df, self.columns


def generate_data(df_iter, start_time, conditions, speed_i=0):
    # Get the next row from the DataFrame iterator

    try:
        row = next(df_iter)
    except StopIteration:
        # If there are no more rows, return None
        return None
    if conditions.get("Crash"):
        data = {'timestamp': [pd.Timestamp.now()]}
        data1 = {'timestamp': pd.Timestamp.now()}
        columns = ["_2", "_3", "_6", "_8", "_9"]

        for column in row._fields:
            if column != 'Index' and column != 'timestamp':
                if column in columns and time.time() - start_time > 10:
                    data[column] = [float(0)]
                    data1[column] = float(0)
                else:
                    data[column] = [float(getattr(row, column))]
                    data1[column] = float(getattr(row, column))
    else:
        # Convert the row to a dictionary
        data = {'timestamp': [pd.Timestamp.now()]}
        data1 = {'timestamp': pd.Timestamp.now()}
        for column in row._fields:
            if column != 'Index' and column != 'timestamp':
                if conditions.get("Engine_heating") and (time.time() - start_time) > 10 and column == "_0":
                    data[column] = [float(100)]
                    data1[column] = float(100)
                elif (conditions.get("Speeding") and (time.time() - start_time) > 10 and column == "_3" and (
                        time.time() - start_time) < 60):
                    data[column] = [float(getattr(row, column) + (speed_i * 10))]
                    data1[column] = float(getattr(row, column) + (speed_i * 10))
                else:
                    data[column] = [float(getattr(row, column))]
                    data1[column] = float(getattr(row, column))
    return data, data1
