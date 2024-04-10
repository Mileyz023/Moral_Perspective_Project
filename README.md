# Moral_Perspective_Project

This repository contains the code for the moral perspective project, our final project for COG403: Seminar in Cognitive Science.

## Report Abstract

Perspective is a multifaceted factor influencing our judgements. This study aims to understand how perspective influences moral decision-making in traffic dilemma. Specifically, we examined the impact of perspective and how it interacts with victim’s traits like gender and age to affect respondent’s moral judgements. The analysis revealed that viewing the moral dilemma from a first-person perspective reduces the likelihood of sparing pedestrians overall. Further examination on the effect of perspective on moral preference indicates that moral decision-making from the first-person perspective increases the probability of sparing certain group of pedestrians (i.e. younger and female). These findings shed light on human moral cognition influenced by different viewing perspectives and have implications for ethical considerations in the development of autonomous vehicles.


## Repository Structure


### Data
1. [data_filtering_and_processing](data_filtering_and_processing/): this directory contains code for how we extracted, filtered, matched and downsampled data from both the data of [the first-person moral dilemma study](https://doi.org/10.1371/journal.pone.0223108) and that of [the third-person moral machine study](https://www.nature.com/articles/s41586-018-0637-6#MOESM1).

      *Suggested Order of viewing:*
      (1) first_person_processing.py; (2) third_person_data_extraction.py; (3) third_person_processing.py; (4) cross_prediction_analysis.py; (5) data_combination.py


2. [processed_data](processed_data): this directory contains all the processed data prepared for the main analysis.


### Method

1. [Logistic_Regression_Analysis.ipynb](Logistic_Regression_Analysis.ipynb): this file is for fitting the logistic regression model, validating the performance and obtaining the results.

2. [amce.R](amce.R): this file includes the computation of the Average Marginal Component Effects (AMCEs) as a comparison to the results from the logistic model.

3. [proportion_analysis.py](proportion_analysis.py): this file is for our extended analysis on the effect of perspective on the favoured group of pedestrians (i.e. younger, female).

