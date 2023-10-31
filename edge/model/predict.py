import pandas as pd


class DetectiveModel:
    __instance = None

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def __init__(self):
        if DetectiveModel.__instance is not None:
            print("Singleton instance already exists. Skipping creation of new model instance.")
            return

        self.beacon = False
        self.alert = None
        self.ideal_brake_pad = 6.4
        self.ideal_brake_fluid_level = 25
        self.ideal_engine_temp_low = 10
        self.ideal_engine_temp_high = 100
        self.ideal_pressure = 28

    def check_tire_pressure(self, df):
        max_val = df[['Tire Pressure (Front Left) [kPa]',
                      'Tire Pressure (Front Right) [kPa]',
                      'Tire Pressure (Rear Left) [kPa]',
                      'Tire Pressure (Rear Right) [kPa]', ]].min().min()
        if max_val < self.ideal_pressure:
            return "Tire pressure is low"
        return None

    def check_brake(self, df):
        brake_fluid_level = min(df["Brake Fluid Level [%]"].tolist())
        brake_pad = min(df["Brake Pad Thickness [mm]"].tolist())
        if brake_fluid_level <= self.ideal_brake_fluid_level and brake_pad <= self.ideal_brake_pad:
            return "Critical Brake failure possible"
        elif brake_fluid_level <= self.ideal_brake_fluid_level and brake_pad > self.ideal_brake_pad:
            return "Chance of brake failure"
        elif brake_fluid_level > self.ideal_brake_fluid_level and brake_pad <= self.ideal_brake_pad:
            return "Chance of break failure"
        else:
            return None

    def check_engine_temperature(self, df):
        engine_temperature = df['Engine Coolant Temperature [C]'].tolist()
        engine_temperature = max(engine_temperature)
        if engine_temperature >= self.ideal_engine_temp_high:
            return "Engine temperature is too high, Possible engine failure"
        if engine_temperature <= self.ideal_engine_temp_low:
            return "Engine temperature is too low"
        return None

    def check_airbag(self, deployed=False):
        if deployed:
            return "Vehicle crashed, airbags deployed"
        return None

    def check_fuel(self, fuel):
        if fuel <= 10:
            return "Fuel low"

    def check_speed(self, df):
        start = df["Vehicle Speed Sensor [km/h]"].iloc[0]
        end = df["Vehicle Speed Sensor [km/h]"].iloc[-1]
        if abs(start - end) > 50:
            return "Speeding"
        return None

    def investigate(self, crash, data):
        df = pd.DataFrame(data)
        df.drop(columns=["timestamp"], inplace=True)
        if crash:
            return {"Beacon": True, "Message": "Crash Happened"}
        engine = self.check_engine_temperature(df)
        brake = self.check_brake(df)
        tire_pressure = self.check_tire_pressure(df)
        speeding = self.check_speed(df)
        if engine:
            return {"Beacon": False, "Message": engine}
        if brake:
            return {"Beacon": False, "Message": brake}
        if tire_pressure:
            return {"Beacon": False, "Message": tire_pressure}
        if speeding:
            return {"Beacon": False, "Message": speeding}
        return None
