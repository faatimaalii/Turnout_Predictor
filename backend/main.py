from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use wildcard for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model after CORS
model_city = joblib.load("models/linreg_city_model.pkl")
model_province = joblib.load("models/linreg_province_model.pkl")

# Load clean dataset once
df_clean = pd.read_csv("../data/cleaned_elections.csv")  # Adjust path if needed

df_clean['City'] = df_clean['City'].str.strip()
df_clean['City'] = df_clean['City'].str.replace(r'\s+\d+$', '', regex=True).str.strip()

# 🆕 Get unique cities and provinces
@app.get("/locations")
def get_locations():
    provinces = sorted(df_clean["Province"].dropna().unique().tolist())
    cities = sorted(df_clean["City"].dropna().unique().tolist())
    return {"provinces": provinces, "cities": cities}
# Request format
class PredictRequest(BaseModel):
    level: str
    name: str
    year: int
    voters: int

@app.post("/predict")
@app.post("/predict")
def predict(req: PredictRequest):
    # Construct DataFrame correctly
    if req.level == "city":
        df = pd.DataFrame([{
            "Year": req.year,
            "City": req.name,
            "Registered_Voters": req.voters
        }])
        print("\n🧾 City-level input to model:\n", df)  # 👈 Debug print here
        turnout = model_city.predict(df)[0]
    else:
        df = pd.DataFrame([{
            "Year": req.year,
            "Province": req.name,
            "Registered_Voters": req.voters
        }])
        print("\n🧾 Province-level input to model:\n", df)  # 👈 Debug print here
        turnout = model_province.predict(df)[0]

    return {
        "turnout": round(turnout, 2),
        "high_turnout": bool(turnout >= 50)
    }

