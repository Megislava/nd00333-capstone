# Heart Failure Prediction using Azure Machine Learning

This project demonstrates an end-to-end machine learning workflow in Azure Machine Learning for predicting mortality in heart failure patients. The workflow includes dataset management, automated model selection using AutoML, hyperparameter tuning using hyperparameter sweep (SDK v2), and deployment of the best-performing model as an online endpoint.

The main goal of the project is to compare Automated ML with manual hyperparameter tuning and to deploy a production-ready model that can be queried via a REST endpoint.

## Project Set Up and Installation
The project was implemented using Azure Machine Learning SDK v2 in a managed Azure ML Notebook environment.

Key components:

- Azure ML Workspace
- Compute cluster
- SDK v2
- Python 3.10
- Environment defined via conda_dependencies.yml

## Dataset

The Heart Failure Clinical Records Dataset contains medical records of heart failure patients. Each record includes demographic information, laboratory measurements, and clinical features.

The target variable is:

- `DEATH_EVENT` (binary classification)

The dataset is relatively small, which makes it suitable for experimentation with Automated ML and classical machine learning models. It is accessible from Kaggle: https://www.kaggle.com/datasets/andrewmvd/heart-failure-clinical-data

Heart Failure Dataset uploaded as MLTable:
<img width="572" height="267" alt="image" src="https://github.com/user-attachments/assets/90b3c5ad-42a0-4ff2-89bd-f770b5e92420" />

### Task
The task is a binary classification problem: predicting whether a patient will experience a death event based on clinical features.

The primary evaluation metric used is accuracy, with additional metrics such as AUC logged where applicable.

### Access
The dataset was uploaded to Azure Machine Learning and registered as a MLTable.
It was accessed in experiments using the Azure ML dataset reference:

```
azureml:<dataset-name>:<version>
```

This allows consistent reuse across AutoML runs, sweep jobs, and deployment.

## Automated ML
Automated ML was used to automatically train and evaluate multiple classification models using Azure ML’s AutoML functionality.

The AutoML experiment was configured with:
- Task: Classification
- Primary metric: Accuracy
- Compute target: CPU cluster
- Cross-validation enabled
- Early stopping enabled

### Results
The AutoML experiment trained multiple models and selected the best-performing model based on the primary metric.

The best model achieved strong performance and was automatically packaged as an MLflow model.

Job completed:
<img width="536" height="268" alt="image" src="https://github.com/user-attachments/assets/0dbc086f-53bc-4612-b520-8978a17a9f37" />

Model ranking:
<img width="536" height="263" alt="image" src="https://github.com/user-attachments/assets/3c0e2bfb-2da7-44d5-8a20-3cbba7e805ae" />

Best model deployment + enable logging:
<img width="557" height="256" alt="image" src="https://github.com/user-attachments/assets/e60716f1-0199-476e-a0fa-d400b565e741" />


<img width="533" height="266" alt="image" src="https://github.com/user-attachments/assets/bde6eab8-13b2-4e2b-888d-d5ba88e0ccd9" />
<img width="328" height="216" alt="image" src="https://github.com/user-attachments/assets/2528abc7-74c8-4bf0-8ee4-85c0a200d8e1" />
<img width="531" height="252" alt="image" src="https://github.com/user-attachments/assets/53cd1808-1d97-42bd-be62-1f444fe47b82" />



## Hyperparameter Tuning

### Model Choice

For hyperparameter tuning, Logistic Regression was selected as a baseline interpretable model suitable for medical data.

Logistic Regression offers:
- Interpretability
- Fast training
- Well-understood behavior in binary classification tasks

### Hyperparameter Search

Hyperparameter tuning was implemented using Azure ML hyperparameter sweep (SDK v2).

The following parameters were tuned:
- `C`: regularization strength (LogUniform distribution)
- `max_iter`: number of training iterations (discrete choices)

The sweep used:
- Random sampling
- Accuracy as the primary metric
- Multiple parallel child runs

<img width="535" height="263" alt="image" src="https://github.com/user-attachments/assets/57b8ddb8-781c-4e67-bc8e-5459d3bb1855" />

### Results
The hyperparameter sweep evaluated multiple configurations and identified the best-performing combination of parameters.

The sweep experiment improved model performance compared to the default configuration and provided insight into the sensitivity of the model to regularization and iteration count.

## Model Deployment

### Deployment Overview

The best-performing model was registered in Azure Machine Learning and deployed as a managed online endpoint.

Deployment configuration:
- Compute type: Azure Container Instance
- Authentication: Key-based authentication enabled
- Model format: MLflow model

<img width="536" height="264" alt="image" src="https://github.com/user-attachments/assets/3b7837cb-bca2-4c94-9315-82b0db2036ea" />
<img width="530" height="208" alt="image" src="https://github.com/user-attachments/assets/d971eb45-78d9-4f74-af62-bcfa7b13848a" />

### Endpoint Usage

The deployed endpoint accepts JSON input containing patient features and returns a prediction indicating the risk of death.


## Screen Recording
Due to company policy restrictions, screen recording is not permitted in the working environment. As a result, a video recording of the project execution cannot be provided. Instead, the project’s functionality and workflow are demonstrated through detailed screenshots and comprehensive step-by-step explanations included throughout this README.


## Standout Suggestions
To improve model accuracy performance, several approaches could be considered, including experimenting with additional feature engineering techniques or increasing the size of the training dataset. Deep learning was not enabled in this run in order to reduce execution time; however, it may be enabled in future runs to further explore potential performance gains.
