import argparse

from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split

from src.data_loader import load_data
from src.feature_engineering import prepare_features
from src.train import build_pipeline


def evaluate(data_path: str) -> dict[str, float]:
    features, target = prepare_features(load_data(data_path))
    x_train, x_test, y_train, y_test = train_test_split(features, target, test_size=0.2, stratify=target, random_state=42)
    model = build_pipeline().fit(x_train, y_train)
    probabilities = model.predict_proba(x_test)[:, 1]
    return {"accuracy": accuracy_score(y_test, probabilities >= 0.5), "roc_auc": roc_auc_score(y_test, probabilities)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/raw/processed.cleveland.data")
    print(evaluate(parser.parse_args().data))
