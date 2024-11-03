# Taken from ONI wiki: https://oxygennotincluded.fandom.com/wiki/Metal_Volcano?so=search
# R = ratio to multiply the ejection amount by
# Safe range for self cooled turbines is 138-125=13
# Safe range for aquatuner cooled turbines is 275-125=150
# Formula: R = (SHC Metal * (Output Temp - Freezing Temp)) / (SHC Water * (Safe Range))
import gc

self_safe_range = 13
tuner_safe_range = 150
shc_water = 4.179
elements = {
    1: {'shc': 0.910, 'output_temp': 1726.85, 'freezing_temp': 660.30},  # Aluminum
    2: {'shc': 0.420, 'output_temp': 2626.85, 'freezing_temp': 1494.9},  # Cobalt
    3: {'shc': 0.386, 'output_temp': 2226.85, 'freezing_temp': 1083.85},  # Copper
    4: {'shc': 0.129, 'output_temp': 2626.85, 'freezing_temp': 1063.85},  # Gold
    5: {'shc': 0.449, 'output_temp': 2526.85, 'freezing_temp': 1534.85},  # Iron
    6: {'shc': 0.265, 'output_temp': 2726.85, 'freezing_temp': 2476.85},  # Niobium
    7: {'shc': 0.134, 'output_temp': 3726.85, 'freezing_temp': 3421.85},  # Tungsten
    8: {'shc': 1.690, 'output_temp': 2626.85, 'freezing_temp': 132.9},  # Uranium
}


class Metal:
    def __init__(self, element_num: int):
        element_entry = elements[element_num]
        self.shc = element_entry['shc']
        self.output_temp = element_entry['output_temp']
        self.freezing_temp = element_entry['freezing_temp']


def get_rs(element_num: int) -> list:
    try:
        metal = Metal(element_num)

        self_cooled_r = ((metal.shc * (metal.output_temp - metal.freezing_temp)) /
                         (shc_water * self_safe_range))

        tuner_cooled_r = ((metal.shc * (metal.output_temp - metal.freezing_temp)) /
                          (shc_water * tuner_safe_range))

        return [self_cooled_r, tuner_cooled_r]
    finally:
        del metal
        gc.collect()


if __name__ == '__main__':

    element = int(input(
        '***Please select the metal you are trying to tame***\n'
        '1. Aluminum\n'
        '2. Cobalt\n'
        '3. Copper\n'
        '4. Gold\n'
        '5. Iron\n'
        '6. Niobium\n'
        '7. Tungsten\n'
        '8. Uranium\n'
        '\n'
        'Choice: '
    ))

    ejection_mass = float(input(
        '\n***Please enter the mass ejected in kilograms per second during eruption***\n'
        'kg/s: '
    ))

    eruption_length = int(input(
        '\n***Please enter the time in seconds per eruption***\n'
        'Seconds: '
    ))

    ejected_mass = ejection_mass * eruption_length
    rs = get_rs(element)

    print(
        f"\nThe self cooled water buffer needed is {ejected_mass*rs[0]}kg\n"
        f"The tuner cooled water buffer needed is {ejected_mass * rs[1]}kg\n"
    )
