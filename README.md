# Tardis: SNCF train delay prediction

> Built at **Epitech Rennes** · B-DAT-200 · Data · February 2026

## Overview

Analysis of historical SNCF train delay data to understand what causes delays and predict them. The project goes from raw data cleaning all the way to an interactive dashboard for travelers.

## Features

- `tardis_eda.ipynb`: cleaning, missing values handling and exploratory data analysis
- `tardis_model.ipynb`: machine learning model predicting delays
- `tardis_dashboard.py`: interactive Streamlit dashboard
- Code formatted with ruff

## Tech stack

`Python` · `pandas` · `NumPy` · `scikit-learn` · `Matplotlib / Seaborn` · `Streamlit`

---

## Technical documentation

### Project Overview

The objective of this project is to create a model that can predict train delays. To achieve this, the project is divided into three key stages:
In first, in tardis_eda notebook : Data cleaning and preprocessing Processing missing values and inconsistencies, and preparing the dataset for analysis.  Exploratory data analysis (EDA), Generating relevant visualizations to understand trends and correlations. All of this is done in the tardis_eda notebook.
Then, in the second stage, in the tardis_model notebook : Predictive modeling, Implementing a machine learning model to predict train delays.
And finally, in the tardis_dashboard.py: Dashboard development, Creation of an interactive web application using Streamlit to display information and enable
user interaction.

--- 
### Installation and Local Run

```
Clone the project:
git clone https://github.com/charly-2025/Tardis-Epitech.git
cd Tardis-Epitech
```

#### Prerequisites

Make sure you have have dataset like project_dataset.csv and installed all dependencies in requirement.txt
  
if not you can enter, at the root , this commmand :
```
pip install -r requirements.txt   
```

#### Running the Project

From the root of the repository, enter the command :

```
streamlit run tardis_dashboard.py
```
Once running you must enter an email address and the application will be accessible at:
    -Local URL: http://localhost:8501
    -Network URL: http://10.28.254.139:8501

---
### Commit Convention
```
Format of the commit message: KARMA GIT

  <type>(<scope>): <subject>
  <BLANK LINE>
  <body>

USEFUL <type> : 
  [FEAT] #For adding a new "feature" for the user.
  [FIX] #For fixing a "feature" relevant to the user.
  [RM] #For removing a "feature" relevant to the user.
  [REFACTOR] #For refactoring production code, e.g. renaming a variable.
  [DOCS] #For changes to the documentation/.md etc.
  [BUILD] #For updating build configuration, development tools or other changes irrelevant to the user.
  [TEST] #For adding missing tests, refactoring tests; no production code change.

USEFUL <scope>:
  - Init
  - Documentation (.md)
  - Deployment
  - Code development
  - Figma

```

---

More of my work on my [portfolio](https://charly-2025.github.io/myPortfolio/).
