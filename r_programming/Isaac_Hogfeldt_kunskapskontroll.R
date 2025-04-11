library(ggplot2)
library(dplyr)
library(caret)
library(scales)
library(reshape2)

# Set working directory to where your CSV file is located
setwd("C:/Users/Isaac/Documents/GitHub/ec-data-science-24/r_programming")

# Load the data
data <- read.csv("blocket_volvo_data.csv", header = TRUE, sep = ",", stringsAsFactors = FALSE)
data <- subset(data, select = -c(Märke, Datum_i_trafik, Färg, Hästkrafter, Biltyp, Index))


# Step 1: Data Exploration and Cleaning
# Make numeric columns numeric
data <- data %>%
  mutate(
    Försäljningspris = as.numeric(gsub("[^0-9.]", "", Försäljningspris)),
    Miltal = as.numeric(gsub("[^0-9.]", "", Miltal)),
    Modellår = as.numeric(gsub("[^0-9.]", "", Modellår)),
    Motorstorlek = as.numeric(gsub("[^0-9.]", "", Motorstorlek))
  )
# Log transform miltal
data$Miltal <- log1p(data$Miltal)

# Convert categorical variables to factors
data <- data %>%
  mutate(across(c(Modell), as.factor))

# One-hot encode small level factor variables
data_encoded <- dummyVars("~ Bränsle + Växellåda + Säljare + Drivning", data = data) %>% predict(newdata = data) %>% as.data.frame() 
data <- cbind(data, data_encoded) %>%
  select(-Bränsle, -Växellåda, -Säljare, -Drivning)

# Remove rows with NA in critical columns
data <- na.omit(data)
colSums(is.na(data))

# Data after cleaning:
summary(data)
correlation_matrix <- cor(data %>% select_if(is.numeric), use = "complete.obs")
correlation_matrix_melted <- melt(correlation_matrix) # Convert matrix to a tidy data frame

ggplot(correlation_matrix_melted, aes(x = Var1, y = Var2, fill = value)) +
  geom_tile() +
  scale_fill_gradient2(low = "blue", mid = "white", high = "red", midpoint = 0) +
  labs(title = "Correlation Matrix Heatmap", x = "", y = "") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust = 1))

# Step 2: Split Data into Training and Testing Sets
set.seed(123) # For reproducibility
index <- createDataPartition(data$Försäljningspris, p = 0.8, list = FALSE)
train_data <- data[index, ]
test_data <- data[-index, ]

# Step 3: Linear Regression Model + k-cross validation
train_control <- trainControl(method = "cv", number = 4)
model <- train(Försäljningspris ~ ., data = train_data, method = "lm", trControl = train_control)


# Step 4: Evaluate Model Performance
summary(model)

# Make predictions on the test data
predictions <- predict(model, newdata = test_data)

# Calculate RMSE (Root Mean Squared Error) for model evaluation
rmse <- sqrt(mean((predictions - test_data$Försäljningspris)^2))
print(paste("RMSE:", rmse))

# Step 5: Visualize Results
ggplot(data.frame(Actual = test_data$Försäljningspris, Predicted = predictions), aes(x = Actual, y = Predicted)) +
  geom_point() +
  geom_abline(intercept = 0, slope = 1, color = "red") + # Perfect prediction line
  labs(title = "Actual vs. Predicted Försäljningspris", x = "Actual Försäljningspris", y = "Predicted Försäljningspris") +
  scale_x_continuous(labels = label_comma()) + # Format x-axis labels
  scale_y_continuous(labels = label_comma())   # Format y-axis labels


# Combine actual and predicted prices in a data frame
results <- data.frame(Actual = test_data$Försäljningspris, Predicted = predictions)




# -----------------------
negative_predictions <- results[results$Predicted < 0, ]
print(negative_predictions)

problematic_rows <- test_data[results$Predicted < 0, ]
print(problematic_rows)

varImp(model)


