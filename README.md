# Phishing Website Detection Using Machine Learning

## 1. Project Overview

Phishing is a cybersecurity threat in which attackers create deceptive websites or URLs to trick users into revealing sensitive information such as passwords, banking details, and personal data.

This project aims to detect phishing websites using Machine Learning classification algorithms. It analyzes URL-related features and predicts whether a website is **Legitimate** or **Phishing**.

The project includes dataset preprocessing, training and comparison of multiple machine learning models, performance evaluation, and an interactive web application developed using Streamlit.

## 2. Objectives

- Detect phishing websites using Machine Learning.
- Collect, clean, and preprocess a suitable dataset.
- Train and compare at least four classification models.
- Evaluate model performance using standard classification metrics.
- Develop an interactive web interface using Streamlit.
- Deploy the application for public access.
- Maintain clean, documented, and reproducible code on GitHub.

## 3. Technology Stack

- **Programming Language:** Python
- **Machine Learning:** Scikit-learn
- **Data Processing:** Pandas, NumPy
- **Model Serialization:** Joblib
- **User Interface:** Streamlit
- **Development Environment:** Google Colab and Visual Studio Code
- **Version Control:** Git and GitHub

## 4. Machine Learning Models

The project compares multiple classification algorithms. Update the list below to match the models actually implemented in your experiments.

- Logistic Regression
- Decision Tree
- Random Forest
- Extra Trees
- XGBoost

The models are evaluated using the following metrics:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC score

The final model is selected based on the evaluation results and the requirements of phishing detection.

## 5. Project Structure

```text
PhishingWebsiteDetection/
│
├── app.py
├── requirements.txt
├── phishing_model.joblib
├── README.md
├── .gitignore
```

*Note: The `results/` folder and image filenames are examples. Adjust the structure to match your actual project files.*

## 6. Installation and Setup

### Prerequisites

- Python 3.10 or a compatible Python version
- pip package manager
- Git (optional, for cloning the repository)

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd PhishingWebsiteDetection
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with the actual URL of your GitHub repository.

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment on Windows:

```cmd
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

## 7. How to Use the Application

1. Launch the Streamlit application.
2. Enter the URL you want to analyze.
3. Submit the URL for prediction.
4. View the predicted classification.
5. Interpret the result as a model-generated indication of whether the URL resembles a phishing or legitimate website.

**Important:** This application is a machine learning-based detection aid. Its predictions are not a guarantee that a website is safe or malicious.

## 8. Dataset and Preprocessing

### Dataset Source

The dataset used in this project was obtained from PhiUSIIL_Phishing_URL_Dataset.csv.

- **Dataset Name**: PhiUSIIL_Phishing_URL_Dataset.csv
- **Source**: Kaggle
- **Dataset Link**: https://www.kaggle.com/datasets/kaggleprollc/phishing-url-websites-dataset-phiusiil
- **Total Records**: 235795
- **Number of Features**: 56
- **Target Classes**: Phishing and Legitimate

### Data Preprocessing

The following preprocessing steps were performed:

- Examined the dataset structure and data types.
- Checked for missing values and duplicate records.
- Analyzed the distribution of phishing and legitimate samples.
- Separated input features from the target label.
- Applied encoding or feature scaling where required.
- Split the dataset into training and testing sets.

### Dataset Usage

The training dataset was used to train the machine learning models, while the testing dataset was used to evaluate their performance using accuracy, precision, recall, F1-score, and ROC-AUC.

## 9. Model Evaluation

The trained models are compared using a common test dataset and consistent evaluation procedures.

| Metric | Description |
|---|---|
| Accuracy | Proportion of all predictions that are correct |
| Precision | Proportion of predicted phishing cases that are actually phishing |
| Recall | Proportion of actual phishing cases correctly detected |
| F1-score | Harmonic mean of precision and recall |
| ROC-AUC | Measures discrimination between the two classes across thresholds |

Add the actual experimental results and figures to this section or to a separate results directory.

## 10. User Interface and Deployment

The application is developed using Streamlit to provide an interactive interface for URL classification.

- **Local execution:** Run the app using the command provided above.
- **Online deployment:** The application is deployed using Streamlit Community Cloud and is accessible through the following link.

**Live application:** https://phishingwebsitedetection-nihd5vfytcebr2dsbrzzr2.streamlit.app/

## 11. Limitations

- Prediction quality depends on the dataset and the features used during training.
- Previously unseen phishing techniques may not be detected accurately.
- A URL prediction alone cannot guarantee the safety of a website.
- Performance on real-world URLs may differ from performance on the test dataset.
- The model should be evaluated and updated as phishing techniques evolve.

## 12. Future Scope

- Integrate additional URL and domain-based features.
- Evaluate the model on newer, independently collected datasets.
- Improve detection of previously unseen phishing attacks.
- Add explainability to show which features influenced a prediction.
- Explore integration with browser security tools or real-time threat intelligence sources.

## 13. Team Members

| Student Name | Roll Number |
|---|---|
| Student 1 | Add roll number |
| Student 2 | Add roll number |
| Student 3 | Add roll number |

## 14. References

Add the research papers, dataset source, and official documentation used in this project.

- Scikit-learn Documentation: https://scikit-learn.org/stable/
- Streamlit Documentation: https://docs.streamlit.io/
- Pandas Documentation: https://pandas.pydata.org/docs/
- NumPy Documentation: https://numpy.org/doc/

## 15. License

Add the license applicable to your project and ensure that the dataset and any third-party resources are used according to their respective terms.
