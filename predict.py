#!/usr/bin/env python3
"""
Predict turnout % for a future election
with either province‑ or city‑level model.
Example:
  python src/predict_turnout.py --level city \
         --name "Peshawar" --year 2029 --voters 350000
"""
import joblib
import argparse
import pandas as pd

MODEL_DIR = "models"


def load_model(level: str):
    fname = f"{MODEL_DIR}/linreg_{level}_model.pkl"
    try:
        return joblib.load(fname)
    except FileNotFoundError:
        raise SystemExit(f"❌ model '{fname}' not found. Train it first.")


def build_df(level: str, name: str, year: int, voters: int) -> pd.DataFrame:
    if level == "province":
        return pd.DataFrame({
            "Year": [year],
            "Province": [name],
            "Registered_Voters": [voters]
        })
    else:  # city
        return pd.DataFrame({
            "Year": [year],
            "City": [name],
            "Registered_Voters": [voters]
        })


def main():
    parser = argparse.ArgumentParser(
        description="Predict voter‑turnout percentage.")
    parser.add_argument("--level", choices=["province", "city"], required=True,
                        help="prediction granularity")
    parser.add_argument("--name", required=True,
                        help="Province or City name (must match training data)")
    parser.add_argument("--year", type=int, required=True,
                        help="Election year to predict (e.g., 2029)")
    parser.add_argument("--voters", type=int, required=True,
                        help="Registered voter count")
    parser.add_argument("--threshold", type=float, default=50.0,
                        help="High/Low cutoff (default 50%)")
    args = parser.parse_args()

    VALID_PROVINCES = ["Punjab", "Sindh", "Balochistan", "Khyber Pakhtunkhwa"]
    VALID_CITIES = ["Lahore", "Karachi", "Peshawar", "Quetta", "Rawalpindi", "Islamabad"]

    if args.level == "province" and args.name not in VALID_PROVINCES:
        raise SystemExit(f"❌ Invalid province name: '{args.name}'\n"
                         f"   → Must be one of: {', '.join(VALID_PROVINCES)}")
    if args.level == "city" and args.name not in VALID_CITIES:
        raise SystemExit(f"❌ Invalid city name: '{args.name}'\n"
                         f"   → Must be one of: {', '.join(VALID_CITIES)}")


    model = load_model(args.level)
    X_new = build_df(args.level, args.name, args.year, args.voters)
    print("\n🧾 Input DataFrame passed to model:\n", X_new)
    turnout = model.predict(X_new)[0]

    print(f"Predicted turnout for {args.name} in {args.year}: {turnout:.2f}%")
    if turnout >= args.threshold:
        print("🟢 High turnout expected.")
    else:
        print("🔴 Low turnout expected.")


if __name__ == "__main__":
    main()
