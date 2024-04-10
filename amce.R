# install.packages("cjoint")
# install.packages("dplyr")
library(dplyr)

# Define working directory
# wdir <- # set working directory
setwd(wdir)

library(cjoint)

dat1 <- read.csv("amce_data.csv")

# Run AMCE estimator using all attributes in the design
results <- amce(Spare ~ Gender + Age_1 + Age_2 + Perspective + Gender:Perspective +
                Age_1:Perspective + Age_2:Perspective, data=dat1,cluster=TRUE, respondent.id="Pair_ID")

# Print summary
summary(results)
plot.amce(results, xlab = "Difference in the Probability of Sparing")
