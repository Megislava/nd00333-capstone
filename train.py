from sklearn.linear_model import LogisticRegression
import argparse
import os
import joblib
from sklearn.model_selection import train_test_split
from azureml.core import Workspace, Dataset, Run
import numpy as np

def clean_data(data):

    x_df = data.to_pandas_dataframe().dropna()
    y_df = x_df.pop("DEATH_EVENT")

    return x_df, y_df

def main():
    # Add arguments to script
    parser = argparse.ArgumentParser()

    parser.add_argument("--C", default=1.0, help="Inversion of regulation strength. Default 1.0")
    parser.add_argument("--max_iter", type=int, default=100, help="Maximum iterations. Default 100")
    
    args = parser.parse_args()

    run = Run.get_context()

    ws = run.experiment.workspace
    dataset_name = "heart-failure-dataset"
    ds = Dataset.get_by_name(ws, name=dataset_name)

    x, y = clean_data(ds) 
    x_train, x_test, y_train, y_test = train_test_split(x, y)

    model = LogisticRegression(C=args.C, max_iter=args.max_iter).fit(x_train, y_train)

    accuracy = model.score(x_test, y_test)
    run.log("Accuracy", float(accuracy))

    # save model
    os.makedirs('outputs', exist_ok=True)
    joblib.dump(model,'outputs/model')

if __name__ == '__main__':
    main()