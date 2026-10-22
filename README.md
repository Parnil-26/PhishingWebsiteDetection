# 🛡️ PhishGuard — Phishing URL Detection Using Machine Learning

PhishGuard is a machine-learning web application that classifies a submitted URL as **Phishing** or **Legitimate**. The Streamlit application extracts lexical and structural features from the URL and passes those features to a trained Random Forest classifier.

> **Disclaimer:** This is an academic machine-learning project. A prediction is not a guarantee that a website is safe or malicious.

## 1. Project Objectives

- Detect potentially phishing URLs using machine learning.
- Inspect and clean a labelled URL-feature dataset.
- Compare several classification models using consistent metrics.
- Select and save a final model for use by the application.
- Provide an interactive Streamlit interface for URL prediction.
- Document local setup and deployment/update steps.

## 2. Technology Stack

- **Language:** Python
- **Data handling:** Pandas, NumPy
- **Machine learning:** scikit-learn
- **Model serialization:** Joblib (`phishguard_model.pkl`)
- **Web interface:** Streamlit
- **Notebook environment:** Google Colab / Jupyter
- **Version control and hosting:** GitHub and Streamlit Community Cloud

## 3. Dataset

The training notebook reads the dataset file named **`url_features_extracted1.csv`**. It contains URL records, extracted URL characteristics, and the target column `ClassLabel`.

### Dataset structure recorded in the notebook

| Item | Value |
|---|---:|
| Rows before cleaning | 101,219 |
| Columns before cleaning | 18 |
| URL text column | `URL` |
| Target column | `ClassLabel` |
| Rows after cleaning | 100,872 |
| Columns after cleaning | 18 |
| Input features used for training | 16 |

The dataset includes the original URL column, 16 engineered URL features, and the target label. The original `URL` string is excluded from the final model input; the application calculates the 16 engineered features from the URL entered by the user.

### Target labels

The notebook's application code interprets **`ClassLabel = 0` as Phishing** and **`ClassLabel = 1` as Legitimate**. The cleaned class counts recorded in the notebook are:

| ClassLabel | Interpretation | Records after cleaning |
|---:|---|---:|
| 0 | Phishing | 63,492 |
| 1 | Legitimate | 37,380 |
| **Total** |  | **100,872** |

**Dataset source:** https://data.mendeley.com/datasets/hx4m73v2sf/2

## 4. Data Cleaning and Preprocessing

The preprocessing steps documented in the training notebook are:

1. **Load the CSV:** Read `url_features_extracted1.csv` using Pandas.
2. **Inspect the data:** Check dataset dimensions, column types, non-null counts, duplicate rows, and class distribution.
3. **Inspect class balance:** Count the records for each `ClassLabel` and plot the class distribution.
4. **Remove rows with missing target labels:** Drop records where `ClassLabel` is missing. The notebook reported one missing target value in the original data.
5. **Remove duplicate rows:** Drop duplicate records. The notebook reported 346 duplicate rows before cleaning.
6. **Verify the cleaned data:** Check that no missing values or duplicate rows remain. The resulting dataset has 100,872 rows.
7. **Separate features and target:** Use `ClassLabel` as the target. Exclude both `ClassLabel` and the raw `URL` column from the final model features.
8. **Split the dataset:** Use an 80% training / 20% testing split with `random_state=42` and `stratify=y`, preserving the approximate class proportions in each split.
9. **Extract the same features at prediction time:** The Streamlit application applies the same feature definitions to a user-entered URL and arranges the values in the model's expected feature order.

The notebook also performs exploratory analysis, including class-distribution plots, a correlation heatmap, URL-length and entropy distributions, digit-count analysis, box plots, and class-wise feature means.

## 5. URL Features Used by the Model

The final classifier uses these 16 features in the following order:

1. `url_length` — total length of the URL
2. `has_ip_address` — whether the host is represented as an IPv4 address
3. `dot_count` — number of dots in the URL
4. `https_flag` — whether the URL uses HTTPS
5. `url_entropy` — character-distribution entropy of the URL
6. `token_count` — number of tokens after splitting on URL separators
7. `subdomain_count` — estimated number of subdomains
8. `query_param_count` — number of query parameters
9. `tld_length` — length of the top-level domain text
10. `path_length` — length of the URL path
11. `has_hyphen_in_domain` — whether the domain contains a hyphen
12. `number_of_digits` — number of digits in the URL
13. `tld_popularity` — whether the TLD is in the notebook's predefined common-TLD list
14. `suspicious_file_extension` — whether the path ends with one of the predefined suspicious file extensions
15. `domain_name_length` — length of the host/domain text after removing a port
16. `percentage_numeric_chars` — percentage of URL characters that are digits

The feature extraction logic in `app.py` must remain consistent with the logic used during model training. If the features or their order change, retrain and save the model and update the application together.

## 6. Models Compared and Evaluation

The training notebook compares five classifiers on the same held-out test split:

- Logistic Regression
- Decision Tree
- Random Forest
- Support Vector Machine (SVM)
- XGBoost

The notebook reports the following metrics. Values below are copied from the notebook's model-comparison output; they are experimental results for that notebook split, not a guarantee of real-world performance.

| Model | Accuracy | Precision | Recall | F1-score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.997026 | 0.993873 | 0.998127 | 0.995996 | 0.999895 |
| Decision Tree | 0.999405 | 0.999465 | 0.998930 | 0.999197 | 0.999307 |
| Random Forest | 0.999554 | 0.999866 | 0.998930 | 0.999398 | 0.999997 |
| SVM | 0.998563 | 0.996798 | 0.999331 | 0.998063 | 0.999952 |
| XGBoost | 0.999405 | 0.999465 | 0.998930 | 0.999197 | 0.999997 |

Random Forest was selected as the final model in the notebook and saved as `phishguard_model.pkl`. Metrics depend on the dataset, labels, feature extraction, and split. For a rigorous evaluation, check for duplicate or near-duplicate URLs across data partitions and evaluate on a newer independent dataset where possible.

## 7. Application and Prediction Workflow

1. A user enters a URL in the Streamlit interface.
2. The app normalizes the URL by adding `http://` when no scheme is provided.
3. The feature extraction function calculates the 16 URL features.
4. The features are placed into a DataFrame using the expected column names and order.
5. The saved Random Forest model predicts the class and provides class probabilities.
6. The interface displays a phishing or legitimate result and the corresponding probability.

A model result is only a machine-learning classification. Do not use it as the sole basis for entering credentials or deciding whether a website is trustworthy.

## 8. Project Structure

```text
PhishingWebsiteDetection/
├── app.py
├── phishguard_model.pkl
├── requirements.txt
├── README.md
├── PhishGuard.ipynb              # optional training notebook
└── url_features_extracted1.csv   # training dataset; not required to run the deployed app
```

Your actual folder may contain additional files. Do not upload the virtual environment (`venv/`) to GitHub.

## 9. Local Installation and Run Instructions

### Prerequisites

- Python compatible with the versions listed in `requirements.txt`
- pip
- Git (optional, for cloning the repository)

### 1. Clone the repository

Replace the placeholder with your actual repository URL:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd PhishingWebsiteDetection
```

### 2. Create and activate a virtual environment (Windows)

```bat
python -m venv venv
venv\Scriptsctivate.bat
```

### 3. Install dependencies

```bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Start the application

```bat
python -m streamlit run app.py
```

Open the local URL shown in the terminal, usually `http://localhost:8501`.

## 10. Online Deployment

The application can be deployed using Streamlit Community Cloud from the GitHub repository.

**Live application:** https://phishingwebsitedetection-nihd5vfytcebr2dsbrzzr2.streamlit.app/

For an update to an existing deployment:

1. Replace `app.py`, `phishguard_model.pkl`, and/or `requirements.txt` as needed.
2. Test locally using the commands above.
3. Commit and push the updated files to the GitHub branch connected to Streamlit Community Cloud.
4. Wait for the deployment to finish, then test the public URL.

The deployed app needs `app.py`, `phishguard_model.pkl`, and `requirements.txt`. The training CSV and notebook are not required at runtime unless the app is changed to read them.

## 11. Limitations and Future Work

- The model only uses the 16 engineered URL features described above.
- URL-only classification cannot guarantee that a website is safe or malicious.
- Newly developed phishing techniques and changes in URL patterns may reduce accuracy.
- The high test metrics should be validated on independent, recent data.
- Future work could include domain registration information, reputation feeds, explainability, monitoring, and repeated evaluation on newer datasets.

## 12. Team Members

| Student Name | Roll Number |
|---|---|
| Student 1 | Add roll number |
| Student 2 | Add roll number |
| Student 3 | Add roll number |

## 13. References and Documentation

- scikit-learn documentation: https://scikit-learn.org/stable/
- Streamlit documentation: https://docs.streamlit.io/
- Pandas documentation: https://pandas.pydata.org/docs/
- NumPy documentation: https://numpy.org/doc/
- XGBoost documentation: https://xgboost.readthedocs.io/

Add the original dataset citation and any research papers used in your report once their bibliographic details and dataset licensing have been verified.

## 14. License

Add a project license if you intend to distribute this code. Confirm that the dataset and any third-party resources may be redistributed under their respective terms before publishing them.
