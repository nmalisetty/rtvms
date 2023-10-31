import time
import numpy as np
import random


def get_engine_coolant_temperature(cause):
    if cause == 'Engine overheating':
        return ',' + str(round(np.random.uniform(101, 130), 0))
    else:
        return ',' + str(round(np.random.uniform(20, 100), 0))


def get_engine_rpm(cause):
    if cause == 'Speeding':
        return ',' + str(round(np.random.uniform(5001, 7000), 0))
    elif cause == 'Engine overheating':
        return ',' + str(round(np.random.uniform(5001, 7000), 0))
    elif cause == 'Crash':
        return ',0'
    else:
        return ',' + str(round(np.random.uniform(1000, 5000), 0))


def get_vehicle_speed(cause):
    if cause == 'Speeding':
        return ',' + str(round(np.random.uniform(71, 120), 0))
    elif cause == 'Crash':
        return ',0'
    else:
        return ',' + str(round(np.random.uniform(1, 70), 0))


def get_outside_air_temperature(cause):
    if cause == 'Engine overheating':
        return ',' + str(round(np.random.uniform(101, 130), 0))
    elif cause == 'Poor weather condition':
        return ',' + str(round(np.random.uniform(0, 30), 0))
    else:
        return ',' + str(round(np.random.uniform(31, 100), 0))


def get_tire_pressure(cause):
    if cause == 'Pressure loss':
        return ',' + str(round(np.random.uniform(0, 20), 0))
    else:
        return ',' + str(round(np.random.uniform(21, 40), 0))


def get_brake_pad_thickness(cause):
    if cause == 'Brake failure':
        return ',' + str(round(np.random.uniform(0, 20), 0))
    else:
        return ',' + str(round(np.random.uniform(21, 50), 0))


def get_brake_rotor_thickness(cause):
    if cause == 'Brake failure':
        return ',' + str(round(np.random.uniform(0, 30), 0))
    else:
        return ',' + str(round(np.random.uniform(31, 100), 0))


def get_brake_fluid_level(cause):
    if cause == 'Brake failure':
        return ',' + str(round(np.random.uniform(0, 10), 0))
    else:
        return ',' + str(round(np.random.uniform(11, 100), 0))


def get_obstacle_collision(cause):
    if cause == 'Crash':
        return ',1'
    else:
        return ',0'


def get_airbag_deployed(cause):
    if cause == 'Crash':
        return ',1'
    else:
        return ',0'


def get_fuel_level(cause):
    if cause == 'No fuel':
        return ',' + str(round(np.random.uniform(0, 2), 1))
    else:
        return ',' + str(round(np.random.uniform(2, 20), 1))


def get_alert(cause):
    if cause == 'None':
        return ',0'
    else:
        return ',1'


def get(file_name):
    ranges = [
        'Engine Coolant Temperature [°F]',
        'Engine RPM [RPM]',
        'Vehicle Speed [mph]',
        'Outside Air Temperature [°F]',
        'Tire Pressure (Front Left) [kPa]',
        'Tire Pressure (Front Right) [kPa]',
        'Tire Pressure (Rear Left) [kPa]',
        'Tire Pressure (Rear Right) [kPa]',
        'Brake Pad Thickness [mm]',
        'Brake Rotor Thickness [mm]',
        'Brake Fluid Level [%]',
        'Obstacle Collision',
        'Airbag Deployed',
        'Fuel [gal]',
        'Alert'
    ]
    causes = ['None', 'Speeding', 'Poor weather condition',
              'Distracted driving', 'Brake failure',
              'Engine overheating', 'No fuel', 'Pressure loss', 'Crash']
    cause = str(random.choices(causes, weights=[0.76, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03])[0])
    result = ''
    result += file_name + ' ' + time.strftime('%H:%M:%S')
    for column in ranges:
        if column == 'Engine Coolant Temperature [°F]':
            result += get_engine_coolant_temperature(cause)
        elif column == 'Engine RPM [RPM]':
            result += get_engine_rpm(cause)
        elif column == 'Vehicle Speed [mph]':
            result += get_vehicle_speed(cause)
        elif column == 'Outside Air Temperature [°F]':
            result += get_outside_air_temperature(cause)
        elif column == 'Tire Pressure (Front Left) [kPa]':
            result += get_tire_pressure(cause)
        elif column == 'Tire Pressure (Front Right) [kPa]':
            result += get_tire_pressure(cause)
        elif column == 'Tire Pressure (Rear Left) [kPa]':
            result += get_tire_pressure(cause)
        elif column == 'Tire Pressure (Rear Right) [kPa]':
            result += get_tire_pressure(cause)
        elif column == 'Brake Pad Thickness [mm]':
            result += get_brake_pad_thickness(cause)
        elif column == 'Brake Rotor Thickness [mm]':
            result += get_brake_rotor_thickness(cause)
        elif column == 'Brake Fluid Level [%]':
            result += get_brake_fluid_level(cause)
        elif column == 'Obstacle Collision':
            result += get_obstacle_collision(cause)
        elif column == 'Airbag Deployed':
            result += get_airbag_deployed(cause)
        elif column == 'Fuel [gal]':
            result += get_fuel_level(cause)
        elif column == 'Alert':
            result += get_alert(cause)
    result += ',' + cause
    return result
