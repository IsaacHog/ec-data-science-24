# Load required libraries
library(ggplot2) # Visualization
library(dplyr)   # Data manipulation
library(caret)   # Model training and evaluation

# Set working directory to where your CSV file is located
setwd("C:/Users/Isaac/Documents/GitHub/ec-data-science-24/r_programming")

# Load the data
data <- read.csv("blocket_volvo_data.csv", header = TRUE, sep = ",", stringsAsFactors = FALSE)
data <- subset(data, select = -c(Märke, Datum_i_trafik, Motorstorlek, Färg, Hästkrafter, Drivning, Biltyp, Index))


# Step 1: Data Exploration and Cleaning
summary(data)

# Make numeric columns numeric
data$Pris <- gsub("[^0-9.]", "", data$Pris)
data$Pris <- as.numeric(data$Pris)
data$Miltal <- gsub("[^0-9.]", "", data$Miltal)
data$Miltal <- as.numeric(data$Miltal)
data$Modellår <- gsub("[^0-9.]", "", data$Modellår)
data$Modellår <- as.numeric(data$Modellår)

# Remove rows with NA in critical columns
data <- na.omit(data)
data <- subset(data, Modell != "" & Växellåda != "")

# Convert categorical variables to factors
data$Säljare <- as.factor(data$Säljare)
data$Bränsle <- as.factor(data$Bränsle)
data$Växellåda <- as.factor(data$Växellåda)
data$Modell <- as.factor(data$Modell)

# Step 2: Split Data into Training and Testing Sets
set.seed(123) # For reproducibility
index <- createDataPartition(data$Pris, p = 0.8, list = FALSE)
train_data <- data[index, ]
test_data <- data[-index, ]
sapply(train_data, function(x) if (is.factor(x)) levels(x))


# Step 3: Linear Regression Model
model <- lm(Pris ~ ., data = train_data)

# Step 4: Evaluate Model Performance
summary(model)

# Make predictions on the test data
predictions <- predict(model, newdata = test_data)

# Calculate RMSE (Root Mean Squared Error) for model evaluation
rmse <- sqrt(mean((predictions - test_data$Pris)^2))
print(paste("RMSE:", rmse))

# Step 5: Visualize Results
ggplot(data.frame(Actual = test_data$Pris, Predicted = predictions), aes(x = Actual, y = Predicted)) +
  geom_point() +
  geom_abline(intercept = 0, slope = 1, color = "red") + # Perfect prediction line
  labs(title = "Actual vs. Predicted Priss", x = "Actual Pris", y = "Predicted Pris")

