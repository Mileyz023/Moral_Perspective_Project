# This file processes the first person moral dataset
import csv

# condition| # Study 1 # 1 = desktop text, 2 = desktop image, 3 = vr text, 4 = vr image 
# Study 2 # 1 = VR text fast, 2 = VR text slow, 3 = VR image fast, 4 = VR image slow 
# we filter out two fast conditions: 1 and 4 in the VR data


# What does the end CSV looks like?
# y: spare (1) or not (0)
# pers: perspective of the respondent; gender: binary gender variable of the victim; age: binary age of the victim
# Gender: 1 - female, 0 - male; 
# Age: 2 - child (girl, boy), 1 - adult (female, male), 0 - elderly (oldwoman, oldman)


# We don't consider animals and nothing
DISCARDED_OBSTACLES = set([7, 8, 9, 10])
# 1 = girl, 2 = boy, 3 = woman, 4 = man, 5 = oldwoman, 6 = oldman
# finish lane: left = 1, right = 2


def determine_gender_and_age(obs):
    gender = 0
    age =  0

    if obs in {1, 3, 5}:
        gender = 1
        
    if obs in {3, 4}:
        age = 1
    if obs in {1, 2}:
        age = 2

    return gender, age


def determine_spare(row_fin):
    if row_fin == 1:
        return 0, 1
    else:
        return 1, 0


def process_row(row):
    obs_left = int(row['obstacle left'])
    obs_right = int(row['obstacle right'])
    row_fin = int(row['finish lane'])

    if obs_left not in DISCARDED_OBSTACLES and obs_right not in DISCARDED_OBSTACLES and obs_left != obs_right:
        gender_l, age_l = determine_gender_and_age(obs_left)
        gender_r, age_r = determine_gender_and_age(obs_right)

        spare_l, spare_r = determine_spare(row_fin)

        return (spare_l, gender_l, age_l), (spare_r, gender_r, age_r)
    else:
        return None
    

# Open the data file and process data
study_1_path = "moral_perspective/first-person/trialmatrix.csv"

fp_data_dict = dict()
ind = 1

with open(study_1_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    for row in csv_reader:
        result = process_row(row)
        if result:
            assert ind not in fp_data_dict
            fp_data_dict[ind] = result[0]
            fp_data_dict[ind+1] = result[1]
            ind += 2


print(len(fp_data_dict)) # 2272


# Writing the dictionary to a CSV file with a header
fp_processed_path = "moral_perspective/processed_data/fp_processed.csv"
with open(fp_processed_path, 'w', newline='') as csv_file:
    fieldnames = ['Ind', 'Spare', 'Gender', 'Age']
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write the header
    csv_writer.writeheader()

    # Write each item in the dictionary
    for key, values in fp_data_dict.items():
        csv_writer.writerow({'Ind': key, 'Spare': values[0], 'Gender': values[1], 'Age': values[2]})