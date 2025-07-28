#!/usr/bin/env python3
"""
Train linear‑regression models for voter‑turnout prediction
at two geographic levels:
    • province  – one model file: models/linreg_province_model.pkl
    • city      – one model file: models/linreg_city_model.pkl
"""
import os
import joblib
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score

DATA_PATH = "data/cleaned_elections.csv"
MODEL_DIR = "models"


def aggregate_for_province(df: pd.DataFrame) -> pd.DataFrame:
    """Return a province‑level table from the city‑level file."""
    grouped = (
        df.groupby(["Year", "Province"], as_index=False)
          .agg({"Registered_Voters": "sum",
                "Votes_Cast": "sum"})
    )
    grouped["Turnout_Percent"] = (
        grouped["Votes_Cast"] / grouped["Registered_Voters"] * 100
    )
    return grouped


def build_pipeline(cat_feature: str) -> Pipeline:
    """Return a preprocessing + LinearRegression pipeline."""
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), [cat_feature])
        ],
        remainder="passthrough"      # numeric cols untouched
    )
    return Pipeline([("prep", preprocessor),
                     ("reg",  LinearRegression())])


def train_model(level: str) -> None:
    """Train model for given level ('province' or 'city') and save it."""
    df = pd.read_csv(DATA_PATH)

    # ---------- choose feature set ----------
    if level == "province":
        df_lvl = aggregate_for_province(df)
        X = df_lvl[["Year", "Province", "Registered_Voters"]]
        y = df_lvl["Turnout_Percent"]
        cat_col = "Province"

    elif level == "city":
        # already city‑level in cleaned file
        X = df[["Year", "City", "Registered_Voters"]]
        y = df["Turnout_Percent"]
        cat_col = "City"
    else:
        raise ValueError("level must be 'province' or 'city'")

    # ---------- train / test split ----------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # ---------- pipeline ----------
    pipe = build_pipeline(cat_col)
    pipe.fit(X_train, y_train)

    # ---------- evaluation ----------
    y_pred = pipe.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2  = r2_score(y_test, y_pred)
    print(f"[{level}]  MSE: {mse:.2f}   R²: {r2:.2f}")

    # ---------- save ----------
    os.makedirs(MODEL_DIR, exist_ok=True)
    fname = f"{MODEL_DIR}/linreg_{level}_model.pkl"
    joblib.dump(pipe, fname)
    print(f"✅ saved {fname}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train province‑ and/or city‑level turnout models.")
    parser.add_argument("--level", choices=["province", "city", "both"],
                        default="both", help="model granularity to train")
    args = parser.parse_args()

    if args.level in ("province", "both"):
        train_model("province")
    if args.level in ("city", "both"):
        train_model("city")
