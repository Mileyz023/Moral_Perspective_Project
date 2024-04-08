# This file is the final step of combining two datasets from different perspectives into one,
# adding a binary variable for perspective
import pandas as pd


def combine_and_write_csv(fp_path, tp_path, out_path):
    # Read CSV files into DataFrames
    df_first = pd.read_csv(fp_path, index_col='Ind')
    df_third = pd.read_csv(tp_path, index_col='Ind')

    df_first.reset_index(drop=True, inplace=True)
    df_third.reset_index(drop=True, inplace=True)

    # Add a new column to indicate the source
    df_first['Perspective'] = 1
    df_third['Perspective'] = 0

    # Concatenate both DataFrames
    combined_df = pd.concat([df_first, df_third])

    # Reset index to have continuous indices
    combined_df.reset_index(drop=True, inplace=True)

    # Save the combined DataFrame to a new CSV file
    combined_df.to_csv(out_path, index=False)


# Controlled variable case
# Generated from moral_perspective/data_filtering_and_processing/cross_prediction_analysis.py
fp_path = "moral_perspective/processed_data/fp_processed_selected.csv"
tp_path = "moral_perspective/processed_data/tp_processed_selected.csv"
out_path = "moral_perspective/processed_data/controlled_variable_combined_new(final).csv"


# Cross variable case (we did not consider those in our final analysis)
# Generated from moral_perspective/data_filtering_and_processing/cross_prediction_analysis.py
fp_path_cross = "moral_perspective/processed_data/fp_processed_selected_cross.csv"
tp_path_cross = "moral_perspective/processed_data/tp_processed_selected_cross.csv"
out_path_cross = "moral_perspective/processed_data/cross_variable_combined(final).csv"


# Store the data
combine_and_write_csv(fp_path, tp_path, out_path)
combine_and_write_csv(fp_path_cross, tp_path_cross, out_path_cross)