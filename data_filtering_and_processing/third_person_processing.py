# This file performs further filtering on the third person moral machine scenarios that we extracted from the original dataset
import csv
from io import StringIO
import random


# Characters we do not consider, in order to match with the other dataset
CHARACTER_IGNORE = ['Stroller', 'Pregnant', 'LargeWoman', 'LargeMan', 'Criminal', 'MaleExecutive', 'FemaleExecutive', 'FemaleAthlete', 'MaleAthlete', 'FemaleDoctor', 'MaleDoctor', 'Dog', 'Cat', 'Homeless']

input_gender_age = "moral_perspective/third-person/scenario_gender_age.csv"
input_random = "moral_perspective/third-person/scenario_random.csv"


def zero_values(row, keys):
    # Iterate over the list of keys
    for key in keys:
        # Check if the key exists in the dictionary and if its value is not '0'
        if row[key] != '0':
            # If any value is not '0', return False
            return False
    # If all values are '0', return True
    return True


def process_data_further(input_path, scenario):

    filtered_dict = dict()

    with open(input_path, "r", newline="") as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:

            # save only ped vs. ped cases, all legal crossing, and some additional verifications
            if row['PedPed'] == '1' and row['Barrier'] == '0' and row['CrossingSignal'] in {'0', '1'} \
                and row['ScenarioType'] in scenario and row['DiffNumberOFCharacters'] == '0':

                if row['ResponseID'] == 'TdF6BNdfN2K749pxv':
                    print(row)

                if zero_values(row, CHARACTER_IGNORE):

                    if row['ResponseID'] not in filtered_dict:
                        # Info we need: 'ScenarioType', 'Saved', 'AttributeLevel', 'Man', 'Woman', 'OldMan', 'OldWoman', 'Boy', 'Girl'
                        response_dict = dict()
                        response_dict['Scenario_Type'] = row['ScenarioTypeStrict']
                        response_dict['Saved'] = [int(float(row['Saved']))]
                        response_dict['AttributeLevel'] = [row['AttributeLevel']]
                        
                        response_dict['Man'] = [int(float(row['Man']))]
                        response_dict['Woman'] = [int(float(row['Woman']))]
                        response_dict['OldMan'] = [int(float(row['OldMan']))]
                        response_dict['OldWoman'] = [int(float(row['OldWoman']))]
                        response_dict['Boy'] = [int(float(row['Boy']))]
                        response_dict['Girl'] = [int(float(row['Girl']))]


                        filtered_dict[row['ResponseID']] = response_dict

                    else:
                        assert filtered_dict[row['ResponseID']]['Scenario_Type'] == row['ScenarioTypeStrict']
                        filtered_dict[row['ResponseID']]['Saved'].append(int(float(row['Saved'])))
                        filtered_dict[row['ResponseID']]['AttributeLevel'].append(row['AttributeLevel'])

                        filtered_dict[row['ResponseID']]['Man'].append(int(float(row['Man'])))
                        filtered_dict[row['ResponseID']]['Woman'].append(int(float(row['Woman'])))
                        filtered_dict[row['ResponseID']]['OldMan'].append(int(float(row['OldMan'])))
                        filtered_dict[row['ResponseID']]['OldWoman'].append(int(float(row['OldWoman'])))
                        filtered_dict[row['ResponseID']]['Boy'].append(int(float(row['Boy'])))
                        filtered_dict[row['ResponseID']]['Girl'].append(int(float(row['Girl'])))

    return filtered_dict


filtered_random = process_data_further(input_random, {'Random'})
filtered_g_a = process_data_further(input_gender_age, {'Age', 'Gender'})

print(len(filtered_g_a)) # 3205377
print(len(filtered_random)) # random: 6297


def find_single_comparison(filtered_dict):

    single_comparison = dict()
    victim_traits = ['Man', 'Woman', 'OldMan', 'OldWoman', 'Boy', 'Girl']

    pedped_count = 0

    for id, info_dict in filtered_dict.items():
        if len(info_dict['Saved']) == 2:
            pedped_count += 1
            val_lst = [info_dict[key] for key in victim_traits]
            non_zero_count = sum(sum(val) != 0 for val in val_lst)
            
            if non_zero_count == 2:
                assert id not in single_comparison
                single_comparison[id] = info_dict

        return single_comparison, pedped_count


single_comp_ga, count_ga = find_single_comparison(filtered_g_a)
single_comp_random, count_random = find_single_comparison(filtered_random)

print(len(single_comp_ga)) # 441172
print(len(single_comp_random)) # random: 55

print(count_ga) # 1540931
print(count_random) # random: 93


# For the gender and age scenario (controlled), randomly downsampled to match the sample size with first person dataset
random_samples = random.sample(list(single_comp_ga.keys()), 1136)
ga_downsampled_dict = {key: single_comp_ga[key] for key in random_samples if key in single_comp_ga}

print(len(ga_downsampled_dict))

# Remove one special case from random scenario
del single_comp_random['TdF6BNdfN2K749pxv']



# Helper for transform_data_structure
def process_scenario(scenario):
    # Define gender and age mappings
    gender_mapping = {'Boy': 0, 'Girl': 1, 'Man': 0, 'Woman': 1, 'OldMan': 0, 'OldWoman': 1}
    age_mapping = {'Boy': 2, 'Girl': 2, 'Man': 1, 'Woman': 1, 'OldMan': 0, 'OldWoman': 0}

    saved = scenario['Saved']
    gender_age_tuples = []

    for key, value in scenario.items():
        if key in gender_mapping:
            gender = gender_mapping[key]
            age = age_mapping[key]
            for i, count in enumerate(value):
                if count > 0:
                    gender_age_tuples.append((saved[i], gender, age))


    return gender_age_tuples


# Prepare data for fitting the logistic regression model
def transform_data_structure(single_comparison):
    tp_data_dict = dict()
    ind = 1

    for response, info_dict in single_comparison.items():
        assert ind not in tp_data_dict
        tup_lst = process_scenario(info_dict)
        assert len(tup_lst) == 2
        tp_data_dict[ind] = tup_lst[0]
        tp_data_dict[ind+1] = tup_lst[1]
        ind += 2

    return tp_data_dict


tp_controlled_var_dict = transform_data_structure(ga_downsampled_dict)
tp_cross_var_dict = transform_data_structure(single_comp_random)

tp_controlled_var_path = "moral_perspective/processed_data/fp_processed.csv"
tp_cross_var_path = "moral_perspective/processed_data/tp_processed_random.csv"


def write_data_to_csv(data_dict, path):
# Writing the dictionary to a CSV file with a header
    with open(path, 'w', newline='') as csv_file:
        fieldnames = ['Ind', 'Spare', 'Gender', 'Age']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write the header
        csv_writer.writeheader()

        # Write each item in the dictionary
        for key, values in data_dict.items():
            csv_writer.writerow({'Ind': key, 'Spare': values[0], 'Gender': values[1], 'Age': values[2]})


# Store transformed data into csv
write_data_to_csv(tp_controlled_var_dict, tp_controlled_var_path)
write_data_to_csv(tp_cross_var_dict, tp_cross_var_path)




# # Store filtered dictionary
# output_file = "/ais/hal9000/yuzhang/403_data_process/third-person/filtered_random_new.csv"

# fieldnames = ['ResponseID', 'Scenario_Type', 'Saved', 'AttributeLevel', 'Man', 'Woman', 'OldMan', 'OldWoman', 'Boy', 'Girl']

# # Open the output CSV file in write mode
# with open(output_file, "w", newline="") as f:
#     # Create a DictWriter object with the fieldnames and specify the delimiter
#     writer = csv.DictWriter(f, fieldnames=fieldnames)

#     # Write the header row
#     writer.writeheader()

#     # Write each dictionary as a row in the CSV file
#     for id, info_dict in filtered_dict.items():
#         row_dict = info_dict
#         row_dict['ResponseID'] = id
#         writer.writerow(row_dict)



# # Restore the dictionary for further processing
# restored_dict = dict()

# #  filter further for single comparison cases, to match with the first-person dataset
# filtered_further = "/hal9000/yuzhang/403_data_process/third-person/filtered_further.csv"
# with open(filtered_further, "r", newline="") as f:
#     csv_reader = csv.DictReader(f)
#     for row in csv_reader:
#         assert row['ResponseID'] not in restored_dict
#         info_dict = {'Scenario_Type': row['Scenario_Type'], 'Saved': ast.literal_eval(row['Saved']), 'AttributeLevel': ast.literal_eval(row['AttributeLevel']), \
#                      'Man': ast.literal_eval(row['Man']), 'Woman': ast.literal_eval(row['Woman']), 'OldMan': ast.literal_eval(row['OldMan']), \
#                         'OldWoman': ast.literal_eval(row['OldWoman']), 'Boy': ast.literal_eval(row['Boy']), 'Girl': ast.literal_eval(row['Girl'])}
#         restored_dict[row['ResponseID']] = info_dict

# print(len(restored_dict))
