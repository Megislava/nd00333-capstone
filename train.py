import argparse
import glob
import os
import joblib
import pandas as pd
import mlflow

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score

def find_csv(data_path: str) -> str:
    csvs = glob.glob(os.path.join(data_path, "**", "*.csv"), recursive=True)
    if not csvs:
        raise FileNotFoundError(f"No CSV found under: {data_path}")
    return csvs[0]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--training_data", type=str, required=True)
    parser.add_argument("--label_col", type=str, default="DEATH_EVENT")
    parser.add_argument("--C", type=float, default=1.0)
    parser.add_argument("--max_iter", type=int, default=100)
    args = parser.parse_args()

    csv_path = find_csv(args.training_data)
    df = pd.read_csv(csv_path).dropna()

    y = df[args.label_col]
    X = df.drop(columns=[args.label_col])

    x_train, x_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = LogisticRegression(C=args.C, max_iter=args.max_iter, solver="liblinear")
    model.fit(x_train, y_train)

    preds = model.predict(x_test)
    acc = accuracy_score(y_test, preds)
    print("tracking uri:", mlflow.get_tracking_uri())
    mlflow.log_metric("accuracy", float(acc))

    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(x_test)[:, 1]
        auc = roc_auc_score(y_test, proba)
        mlflow.log_metric("auc", float(auc))

    os.makedirs("outputs", exist_ok=True)
    joblib.dump(model, "outputs/model.pkl")

if __name__ == "__main__":
    main()