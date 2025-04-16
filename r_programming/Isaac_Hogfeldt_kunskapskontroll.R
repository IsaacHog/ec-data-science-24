library(ggplot2)
library(dplyr)
library(caret)
library(scales)
library(reshape2)

# Set working directory to where your CSV file is located
setwd("C:/Users/Isaac/Documents/GitHub/ec-data-science-24/r_programming")

load_data <- function(file_path) {
  data <- read.csv(file_path, header = TRUE, sep = ",", stringsAsFactors = FALSE)
  data <- subset(data, select = -c(Märke, Datum_i_trafik, Färg, Hästkrafter, Biltyp, Index))
  return(data)
}

clean_data <- function(data) {
  # Assign numeric and factor types to columns
  data <- data %>%
    mutate(
      Försäljningspris = as.numeric(gsub("[^0-9.]", "", Försäljningspris)),
      Miltal = as.numeric(gsub("[^0-9.]", "", Miltal)),
      Modellår = as.numeric(gsub("[^0-9.]", "", Modellår)),
      Motorstorlek = as.numeric(gsub("[^0-9.]", "", Motorstorlek))
    )
  data <- data %>%
    mutate(across(c(Modell), as.factor))
  
  # Remove extreme cases
  data <- data %>%
    filter(Miltal > 2000 & Miltal < 50000 & Försäljningspris < 600000 )
  
  # One-hot encode small level factor variables
  data_encoded <- dummyVars("~ Bränsle + Växellåda + Säljare + Drivning", data = data) %>% predict(newdata = data) %>% as.data.frame() 
  data <- cbind(data, data_encoded) %>%
    select(-Bränsle, -Växellåda, -Säljare, -Drivning)
  
  # Remove rows with NA in critical columns
  data <- na.omit(data)
  
  return(data)
}

visualise_corr_matrix <- function(data) {
  correlation_matrix <- cor(data %>% select_if(is.numeric), use = "complete.obs")
  correlation_matrix_melted <- melt(correlation_matrix)
  
  plot_obj <- ggplot(correlation_matrix_melted, aes(x = Var1, y = Var2, fill = value)) +
    geom_tile() +
    scale_fill_gradient2(low = "blue", mid = "white", high = "red", midpoint = 0) +
    labs(title = "Correlation Matrix Heatmap", x = "", y = "") +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust = 1))
  
  print(plot_obj)
}

train_model <- function(data) {
  set.seed(123)
  index <- createDataPartition(data$Försäljningspris, p = 0.8, list = FALSE)
  train_data <- data[index, ]
  test_data <- data[-index, ]
  
  train_control <- trainControl(method = "cv", number = 4)
  model <- train(Försäljningspris ~ ., data = train_data, method = "glm",
                 family = poisson(link = "log"), trControl = train_control)
  
 return(list(model = model, test_data = test_data, data = data))
}

evalute_model <- function(model, test_data) {
  summary(model)
  predictions <- predict(model, newdata = test_data)
  rmse <- sqrt(mean((predictions - test_data$Försäljningspris)^2))
  print(paste("RMSE:", rmse))
  varImp(model)
  
  plot_obj <- ggplot(data.frame(Actual = test_data$Försäljningspris, Predicted = predictions), 
                     aes(x = Actual, y = Predicted)) +
    geom_point() +
    geom_abline(intercept = 0, slope = 1, color = "red") + # Perfect prediction line
    labs(title = "Actual vs. Predicted Försäljningspris", x = "Actual Försäljningspris", y = "Predicted Försäljningspris") +
    scale_x_continuous(labels = label_comma()) + # Format x-axis labels
    scale_y_continuous(labels = label_comma())   # Format y-axis labels
  
  print(plot_obj)
  
  results <- data.frame(Actual = test_data$Försäljningspris, Predicted = predictions)
  print("Done")
  return(results) 
}

create_model <- function() {
  data = load_data(file_path = "blocket_volvo_data.csv")
  data = clean_data(data = data)
  model_object = train_model(data)
  return(model_object)
}

model_object = create_model()
visualise_corr_matrix(data = model_object$data)
results = evalute_model(model = model_object$model, test_data = model_object$test_data)




