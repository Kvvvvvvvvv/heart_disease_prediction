# Import necessary libraries for exploratory data analysis (EDA) and plotting
import numpy as np  # Shortened to np
import pandas as pd  # Shortened to pd
import matplotlib.pyplot as plt
import seaborn as sns  # Shortened to sns

# Ensure plots appear in the notebook


## Machine learning models
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

## Model evaluation tools
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.metrics import precision_score, recall_score, f1_score
# Note: In Scikit-Learn 1.2+, "plot_roc_curve" was changed to "RocCurveDisplay"
from sklearn.metrics import RocCurveDisplay

# Print last updated timestamp
import time
print(f"Last updated: {time.asctime()}")

# ===== CELL SEPARATOR =====

df = pd.read_csv("data/heart-disease-UCI.csv")
# df.shape
df

# ===== CELL SEPARATOR =====

# Let's see how many positive (1) and negative (0) samples we have in our dataframe
df.target.value_counts()

# ===== CELL SEPARATOR =====

# Normalized value counts
df.target.value_counts(normalize=True)

# ===== CELL SEPARATOR =====

# Plot the value counts with a bar graph
df.target.value_counts().plot(kind="bar", color=["salmon", "lightblue"]);

# ===== CELL SEPARATOR =====

df.info()

# ===== CELL SEPARATOR =====

df.describe()

# ===== CELL SEPARATOR =====

df.sex.value_counts()

# ===== CELL SEPARATOR =====

#Comparison of Target Column with Sex Column
pd.crosstab(df.target, df.sex)

# ===== CELL SEPARATOR =====

# Create a plot
pd.crosstab(df.target, df.sex).plot(kind="bar", 
                                    figsize=(10,6), 
                                    color=["salmon", "lightblue"]);

# ===== CELL SEPARATOR =====

# Create a plot
pd.crosstab(df.target, df.sex).plot(kind="bar", figsize=(10,6), color=["salmon", "lightblue"])

# Add some attributes to it
plt.title("Heart Disease Frequency for Sex")
plt.xlabel("0 = No Disease, 1 = Disease")
plt.ylabel("Amount")
plt.legend(["Female", "Male"])
plt.xticks(rotation=0); # keep the labels on the x-axis vertical

# ===== CELL SEPARATOR =====

# Create another figure
plt.figure(figsize=(10,6))

# Start with positve examples
plt.scatter(df.age[df.target==1], 
            df.thalach[df.target==1], 
            c="salmon") # define it as a scatter figure

# Now for negative examples, we want them on the same plot, so we call plt again
plt.scatter(df.age[df.target==0], 
            df.thalach[df.target==0], 
            c="lightblue") # axis always come as (x, y)

# Add some helpful info
plt.title("Heart Disease in function of Age and Max Heart Rate")
plt.xlabel("Age")
plt.legend(["Disease", "No Disease"])
plt.ylabel("Max Heart Rate");

# ===== CELL SEPARATOR =====

# Histograms are a great way to check the distribution of a variable
df.age.plot.hist();

# ===== CELL SEPARATOR =====

pd.crosstab(df.cp, df.target)

# ===== CELL SEPARATOR =====

# Create a new crosstab and base plot
pd.crosstab(df.cp, df.target).plot(kind="bar", 
                                   figsize=(10,6), 
                                   color=["lightblue", "salmon"])

# Add attributes to the plot to make it more readable
plt.title("Heart Disease Frequency Per Chest Pain Type")
plt.xlabel("Chest Pain Type")
plt.ylabel("Frequency")
plt.legend(["No Disease", "Disease"])
plt.xticks(rotation = 0);

# ===== CELL SEPARATOR =====

# Find the correlation between our independent variables
corr_matrix = df.corr()
corr_matrix 

# ===== CELL SEPARATOR =====

# Let's make it look a little prettier
corr_matrix = df.corr()
plt.figure(figsize=(15, 10))
sns.heatmap(corr_matrix, 
            annot=True, 
            linewidths=0.5, 
            fmt= ".2f", 
            cmap="YlGnBu");

# ===== CELL SEPARATOR =====

df.head()

# ===== CELL SEPARATOR =====

# Everything except target variable
X = df.drop("target", axis=1)

# Target variable
y = df.target.values

# ===== CELL SEPARATOR =====

# Independent variables (no target column)
X.head()

# ===== CELL SEPARATOR =====

# Targets
y

# ===== CELL SEPARATOR =====

# Random seed for reproducibility
np.random.seed(42)

# Split into train & test set
X_train, X_test, y_train, y_test = train_test_split(X, # independent variables 
                                                    y, # dependent variable
                                                    test_size = 0.2) # percentage of data to use for test set

# ===== CELL SEPARATOR =====

X_train.head()

# ===== CELL SEPARATOR =====

y_train, len(y_train)

# ===== CELL SEPARATOR =====

X_test.head()

# ===== CELL SEPARATOR =====

y_test, len(y_test)

# ===== CELL SEPARATOR =====

# Put models in a dictionary
models = {"KNN": KNeighborsClassifier(),
          "Logistic Regression": LogisticRegression(), 
          "Random Forest": RandomForestClassifier()}

# Create function to fit and score models
def fit_and_score(models, X_train, X_test, y_train, y_test):
    """
    Fits and evaluates given machine learning models.
    models : a dict of different Scikit-Learn machine learning models
    X_train : training data
    X_test : testing data
    y_train : labels assosciated with training data
    y_test : labels assosciated with test data
    """
    # Random seed for reproducible results
    np.random.seed(42)
    # Make a list to keep model scores
    model_scores = {}
    # Loop through models
    for name, model in models.items():
        # Fit the model to the data
        model.fit(X_train, y_train)
        # Evaluate the model and append its score to model_scores
        model_scores[name] = model.score(X_test, y_test)
    return model_scores

# ===== CELL SEPARATOR =====

model_scores = fit_and_score(models=models,
                             X_train=X_train,
                             X_test=X_test,
                             y_train=y_train,
                             y_test=y_test)
model_scores

# ===== CELL SEPARATOR =====

model_compare = pd.DataFrame(model_scores, index=['accuracy'])
model_compare.T.plot.bar();

# ===== CELL SEPARATOR =====

model_compare = pd.DataFrame(model_scores, index=["accuracy"])
model_compare.plot.bar()

# ===== CELL SEPARATOR =====

# Create a list of train scores
train_scores = []

# Create a list of test scores
test_scores = []

# Create a list of different values for n_neighbors
neighbors = range(1, 21) # 1 to 20

# Setup algorithm
knn = KNeighborsClassifier()

# Loop through different neighbors values
for i in neighbors:
    knn.set_params(n_neighbors = i) # set neighbors value
    
    # Fit the algorithm
    knn.fit(X_train, y_train)
    
    # Update the training scores
    train_scores.append(knn.score(X_train, y_train))
    
    # Update the test scores
    test_scores.append(knn.score(X_test, y_test))

# ===== CELL SEPARATOR =====

train_scores

# ===== CELL SEPARATOR =====

plt.plot(neighbors, train_scores, label="Train score")
plt.plot(neighbors, test_scores, label="Test score")
plt.xticks(np.arange(1, 21, 1))
plt.xlabel("Number of neighbors")
plt.ylabel("Model score")
plt.legend()

print(f"Maximum KNN score on the test data: {max(test_scores)*100:.2f}%")

# ===== CELL SEPARATOR =====

# Different LogisticRegression hyperparameters
log_reg_grid = {"C": np.logspace(-4, 4, 20),
                "solver": ["liblinear"]}

# Different RandomForestClassifier hyperparameters
rf_grid = {"n_estimators": np.arange(10, 1000, 50),
           "max_depth": [None, 3, 5, 10],
           "min_samples_split": np.arange(2, 20, 2),
           "min_samples_leaf": np.arange(1, 20, 2)}

# ===== CELL SEPARATOR =====

# Setup random seed
np.random.seed(42)

# Setup random hyperparameter search for LogisticRegression
rs_log_reg = RandomizedSearchCV(LogisticRegression(),
                                param_distributions=log_reg_grid,
                                cv=5,
                                n_iter=20,
                                verbose=True)

# Fit random hyperparameter search model
rs_log_reg.fit(X_train, y_train);

# ===== CELL SEPARATOR =====

rs_log_reg.best_params_

# ===== CELL SEPARATOR =====

rs_log_reg.score(X_test, y_test)


# ===== CELL SEPARATOR =====

# Setup random seed
np.random.seed(42)

# Setup random hyperparameter search for RandomForestClassifier
rs_rf = RandomizedSearchCV(RandomForestClassifier(),
                           param_distributions=rf_grid,
                           cv=5,
                           n_iter=20,
                           verbose=True)

# Fit random hyperparameter search model
rs_rf.fit(X_train, y_train);

# ===== CELL SEPARATOR =====

# Find the best parameters
rs_rf.best_params_

# ===== CELL SEPARATOR =====

# Evaluate the randomized search random forest model
rs_rf.score(X_test, y_test)

# ===== CELL SEPARATOR =====

# Different LogisticRegression hyperparameters
log_reg_grid = {"C": np.logspace(-4, 4, 20),
                "solver": ["liblinear"]}

# Setup grid hyperparameter search for LogisticRegression
gs_log_reg = GridSearchCV(LogisticRegression(),
                          param_grid=log_reg_grid,
                          cv=5,
                          verbose=True)

# Fit grid hyperparameter search model
gs_log_reg.fit(X_train, y_train);

# ===== CELL SEPARATOR =====

# Check the best parameters
gs_log_reg.best_params_

# ===== CELL SEPARATOR =====

# Evaluate the model
gs_log_reg.score(X_test, y_test)

# ===== CELL SEPARATOR =====

# Make preidctions on test data
y_preds = gs_log_reg.predict(X_test)
y_preds

# ===== CELL SEPARATOR =====

y_test

# ===== CELL SEPARATOR =====

# Before Scikit-Learn 1.2.0 (will error with versions 1.2+)
# from sklearn.metrics import plot_roc_curve 
# plot_roc_curve(gs_log_reg, X_test, y_test);

# Scikit-Learn 1.2.0 or later
from sklearn.metrics import RocCurveDisplay 

# from_estimator() = use a model to plot ROC curve on data
RocCurveDisplay.from_estimator(estimator=gs_log_reg, 
                               X=X_test, 
                               y=y_test); 

# ===== CELL SEPARATOR =====

# Display confusion matrix
print(confusion_matrix(y_test, y_preds))

# ===== CELL SEPARATOR =====

# Import Seaborn
import seaborn as sns
sns.set(font_scale=1.5) # Increase font size

def plot_conf_mat(y_test, y_preds):
    """
    Plots a confusion matrix using Seaborn's heatmap().
    """
    fig, ax = plt.subplots(figsize=(3, 3))
    ax = sns.heatmap(confusion_matrix(y_test, y_preds),
                     annot=True, # Annotate the boxes
                     cbar=False)
    plt.xlabel("true label")
    plt.ylabel("predicted label")
    
plot_conf_mat(y_test, y_preds)

# ===== CELL SEPARATOR =====

# Show classification report
print(classification_report(y_test, y_preds))

# ===== CELL SEPARATOR =====

# Check best hyperparameters
gs_log_reg.best_params_

# ===== CELL SEPARATOR =====

# Import cross_val_score
from sklearn.model_selection import cross_val_score

# Instantiate best model with best hyperparameters (found with GridSearchCV)
clf = LogisticRegression(C=0.23357214690901212,
                         solver="liblinear")

# ===== CELL SEPARATOR =====

# Cross-validated accuracy score
cv_acc = cross_val_score(clf,
                         X,
                         y,
                         cv=5, # 5-fold cross-validation
                         scoring="accuracy") # accuracy as scoring
cv_acc

# ===== CELL SEPARATOR =====

cv_acc = np.mean(cv_acc)
cv_acc

# ===== CELL SEPARATOR =====

# Cross-validated precision score
cv_precision = np.mean(cross_val_score(clf,
                                       X,
                                       y,
                                       cv=5, # 5-fold cross-validation
                                       scoring="precision")) # precision as scoring
cv_precision

# ===== CELL SEPARATOR =====

# Cross-validated recall score
cv_recall = np.mean(cross_val_score(clf,
                                    X,
                                    y,
                                    cv=5, # 5-fold cross-validation
                                    scoring="recall")) # recall as scoring
cv_recall

# ===== CELL SEPARATOR =====

# Cross-validated F1 score
cv_f1 = np.mean(cross_val_score(clf,
                                X,
                                y,
                                cv=5, # 5-fold cross-validation
                                scoring="f1")) # f1 as scoring
cv_f1

# ===== CELL SEPARATOR =====

# Visualizing cross-validated metrics
cv_metrics = pd.DataFrame({"Accuracy": cv_acc,
                            "Precision": cv_precision,
                            "Recall": cv_recall,
                            "F1": cv_f1},
                          index=[0])
cv_metrics.T.plot.bar(title="Cross-Validated Metrics", legend=False);

# ===== CELL SEPARATOR =====

# Fit an instance of LogisticRegression (taken from above)
clf.fit(X_train, y_train);

# ===== CELL SEPARATOR =====

# Check coef_
clf.coef_

# ===== CELL SEPARATOR =====

# Match features to columns
features_dict = dict(zip(df.columns, list(clf.coef_[0])))
features_dict

# ===== CELL SEPARATOR =====

# Visualize feature importance
features_df = pd.DataFrame(features_dict, index=[0])
features_df.T.plot.bar(title="Feature Importance", legend=False);

# ===== CELL SEPARATOR =====

pd.crosstab(df["sex"], df["target"])

# ===== CELL SEPARATOR =====

# Contrast slope (positive coefficient) with target
pd.crosstab(df["slope"], df["target"])