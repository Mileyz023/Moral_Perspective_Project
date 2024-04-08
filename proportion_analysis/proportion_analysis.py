# Main file for the proportion analysis
import pandas as pd
from scipy.stats import chi2_contingency
from scipy.stats.contingency import odds_ratio

controlled_df = pd.read_csv("/ais/hal9000/yuzhang/moral_perspective/processed_data/controlled_variable_combined_new(final).csv")


# All nine combinations of comparison in our case
CONTROLLED_SET = {((1, 2), (0, 2)),
              ((1, 2), (1, 1)),
              ((1, 1), (0, 1)),
              ((1, 2), (1, 0)),
              ((1, 1), (1, 0)),
              ((1, 0), (0, 0)),
              ((0, 2), (0, 1)),
              ((0, 2), (0, 0)),
              ((0, 1), (0, 0))}


CHARACTER_VALUE = {(1, 2), (1, 1), (1, 0), (0, 2), (0, 1), (0, 0)}


def create_character_mapping():
    mapping_dict = {t: None for t in CHARACTER_VALUE}
    for key in mapping_dict:
        if key[0] == 1:
            if key[1] == 2:
                mapping_dict[key] = 'Girl'
            elif key[1] == 1:
                mapping_dict[key] = 'Woman'
            elif key[1] == 0:
                mapping_dict[key] = 'OldWoman'
        else:
            if key[1] == 2:
                mapping_dict[key] = 'Boy'
            elif key[1] == 1:
                mapping_dict[key] = 'Man'
            elif key[1] == 0:
                mapping_dict[key] = 'OldMan'
    
    return mapping_dict


def load_cases_separate_pers(df, scne_set):
    df_first = df[df['Perspective'] == 1].reset_index(drop=True)
    df_third = df[df['Perspective'] == 0].reset_index(drop=True)
    
    count_f, case_dict_f = process_df(df_first, scne_set)
    count_t, case_dict_t = process_df(df_third, scne_set)

    return count_f, case_dict_f, count_t, case_dict_t


def process_df(df, scenario_set):
    loop_count = 0
    case_dict = {t: [0, 0, 0] for t in scenario_set}

    for i in range(0, len(df) - 1, 2):
        loop_count += 1
        first_vic = (df.at[i, "Gender"], df.at[i, "Age"])
        second_vic = (df.at[i+1, "Gender"], df.at[i+1, "Age"])

        first_vic_spare = df.at[i, "Spare"]
        second_vic_spare = df.at[i+1, "Spare"]

        if (first_vic, second_vic) in scenario_set:
            case_dict[(first_vic, second_vic)][0] += first_vic_spare
            case_dict[(first_vic, second_vic)][1] += second_vic_spare
            case_dict[(first_vic, second_vic)][2] += 1

        elif (second_vic, first_vic) in scenario_set:
            case_dict[(second_vic, first_vic)][0] += second_vic_spare
            case_dict[(second_vic, first_vic)][1] += first_vic_spare
            case_dict[(second_vic, first_vic)][2] += 1
    
    return loop_count, case_dict


count_f, case_dict_f, count_t, case_dict_t = load_cases_separate_pers(controlled_df, CONTROLLED_SET)

print((count_f, count_t))

print(case_dict_f)
print(case_dict_t)


# Chisq and odds ratio test for comparing the proportion of sparing between first-person and third-person
# Methods: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.contingency.odds_ratio.html
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2_contingency.html
chisq_test_lst = list()
CONTROLLED_LST = list(CONTROLLED_SET)

for case in CONTROLLED_LST:
    spare_case = [case_dict_t[case][0], case_dict_f[case][0]]
    non_spare_case = [case_dict_t[case][1], case_dict_f[case][1]]
    chisq_test_lst.append([spare_case, non_spare_case])

print(chisq_test_lst)


chisq_test_result = list()
for i in range(len(chisq_test_lst)):
    chi2_stat, p_val, _, _ = chi2_contingency(chisq_test_lst[i])
    res = odds_ratio(chisq_test_lst[i])
    chisq_test_result.append([CONTROLLED_LST[i], p_val, res.statistic, res.confidence_interval(confidence_level=0.95)])

print(chisq_test_result)



# Calculate proportion for each comparison
def calculate_proportion(case_dict):
    case_dict_prop = dict()
    for case, count in case_dict.items():
        assert case not in case_dict_prop
        prop_1 = count[0] / count[2]
        prop_2 = count[1] / count[2]
        case_dict_prop[case] = (prop_1, prop_2)
    
    return case_dict_prop


fp_prop = calculate_proportion(case_dict_f)
tp_prop = calculate_proportion(case_dict_t)


mapping_dict = create_character_mapping()


def map_character_with_val(mapping_dict, val_dict):
    character_dict = dict()
    for case, val in val_dict.items():
        case_by_character = (mapping_dict[case[0]], mapping_dict[case[1]])
        assert case_by_character not in character_dict
        character_dict[case_by_character] = val


    return character_dict

fp_character_prop = map_character_with_val(mapping_dict, fp_prop)
tp_character_prop = map_character_with_val(mapping_dict, tp_prop)


comparison_list = list()
prop_list_fp = list()
prop_list_tp = list()

for comparison, prop in fp_character_prop.items():
    comparison_list.append(comparison)
    prop_list_fp.append(prop[0])

for comp in comparison_list:
    prop_list_tp.append(tp_character_prop[comp][0])


print(comparison_list)
print(prop_list_fp)
print(prop_list_tp)
