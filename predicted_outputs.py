import pandas as pd

data = {
    "Province": [
        "Punjab", "Sindh", "Balochistan", "Khyber Pakhtunkhwa",
        "Islamabad", "Gilgit-Baltistan", "Azad Kashmir"
    ],
    "Predicted Turnout": [56.3, 52.1, 47.8, 60.4, 62.5, 50.2, 49.7]
}

df = pd.DataFrame(data)
df.to_csv("predicted_turnout.csv", index=False)
print("File saved: predicted_turnout.csv")
