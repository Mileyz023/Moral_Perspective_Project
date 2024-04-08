# In this file, we separate controlled variable cases and cross variable cases from the first person dataset
# We perform two sets of analyses based on different traffic scenarios in the data: 
# (1) controlled variable case: one variable of victim traits, either gender or age, is being controlled in the scenario 
# (e.g. Oldwoman vs. Oldman, age is being controlled)

# (2) cross variable case: neither gender nor age is being controlled in the comparison
# (e.g. Girl vs. Oldman) 
# Note: we did not include the second case in our final analysis due to small sample size

import pandas as pd
import random


# Part 1: Identify scenarios where one variable is being controlled in the first person data
df_fp_complete = pd.read_csv("moral_perspective/processed_data/fp_processed.csv")

# Function to count occurrences where either age or gender values are the same
def count_same_values_fp(df):
    count = 0
    loop_count = 0
    indices = list()
    for i in range(0, len(df) - 1, 2):
        loop_count += 1
        if (df.at[i, 'Age'] == df.at[i+1, 'Age']) or (df.at[i, 'Gender'] == df.at[i+1, 'Gender']):
            count += 1
            indices.extend([i, i+1])
    
    pairs_df = df.iloc[list(set(indices))]
    pairs_cross_df = df.loc[~df.index.isin(indices)]
    return loop_count, count, pairs_df, pairs_cross_df

# Counting occurrences where either age or gender values are the same
loop_c, same_values_count, df_select, df_cross = count_same_values_fp(df_fp_complete)

df_select.set_index('Ind')
sorted_df = df_select.sort_index()

fp_processed_select_path = "moral_perspective/processed_data/fp_processed_selected.csv"
sorted_df.to_csv(fp_processed_select_path, index=False)



# Part 2: Identify cross variable scenarios from the first person cross data
df_cross.set_index('Ind')
sorted_df_cross = df_cross.sort_index()

# Randomly downsampled
range_ind = list(range(0, 908, 2))
sampled_ind = random.sample(range_ind, 49) # Match with number of third person cross variable cases below
new_ind = list()
for ind in sampled_ind:
        new_ind.extend([ind, ind+1])

sampled_df_cross = sorted_df_cross.iloc[list(set(new_ind))]

sampled_df_cross.set_index('Ind')
sampled_df = sampled_df_cross.sort_index()


fp_processed_cross_path = "moral_perspective/processed_data/fp_processed_selected_cross.csv"
sampled_df.to_csv(fp_processed_cross_path, index=False)




# Part 3: Randomly select from tp (in tp_processed.csv, all cases are controlled variable cases)
df_tp_complete = pd.read_csv("moral_perspective/processed_data/tp_processed.csv")

# Function to count occurrences where either age or gender values are the same
def count_same_values_tp(df):
    count = 0
    loop_count = 0
    indices = list()
    for i in range(0, len(df) - 1, 2):
        loop_count += 1
        if (df.at[i, 'Age'] == df.at[i+1, 'Age']) or (df.at[i, 'Gender'] == df.at[i+1, 'Gender']):
            count += 1
            indices.append(i)
    
    random_sample = random.sample(indices, 682)
    new_ind = list()
    for ind in random_sample:
        new_ind.extend([ind, ind+1])

    pairs_df = df.iloc[list(set(new_ind))]
    return new_ind, count, pairs_df


# Counting occurrences where either age or gender values are the same
ind, same_values_count, df_tp_selected = count_same_values_tp(df_tp_complete)

print("Number of pairs where either age or gender values are the same:", same_values_count)

df_tp_selected.set_index('Ind')
sorted_tp_df = df_tp_selected.sort_index()


tp_processed_select_path = "moral_perspective/processed_data/tp_processed_selected.csv"
sorted_tp_df.to_csv(tp_processed_select_path, index=False)




# Part 4: Identify cross variable scenarios from the third person cross data - random scnearios
df_random = pd.read_csv("moral_perspective/processed_data/tp_processed_random.csv")

# Function to count occurrences where either age or gender values are the same
def count_same_values_tp_cross(df):
    count = 0
    loop_count = 0
    indices = list()
    for i in range(0, len(df) - 1, 2):
        loop_count += 1
        if (df.at[i, 'Age'] == df.at[i+1, 'Age']) or (df.at[i, 'Gender'] == df.at[i+1, 'Gender']):
            count += 1
            indices.extend([i, i+1])
    
    pairs_df = df.loc[~df.index.isin(indices)]
    return indices, count, pairs_df

# Counting occurrences where either age or gender values are the same
ind, same_values_count, df_select_cross = count_same_values_tp_cross(df_random)
print("Number of pairs where either age or gender values are the same:", same_values_count)

df_select_cross.set_index('Ind')
sorted_df = df_select.sort_index()

tp_processed_cross_path = "moral_perspective/processed_data/tp_processed_selected_cross.csv"
sorted_df.to_csv(tp_processed_cross_path, index=False)