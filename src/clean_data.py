import pandas as pd

# Load raw data
df = pd.read_csv("data/election_dataset.csv")

# Step 1: Fill missing values forward within each constituency per year
df[['Registered Voters', 'Turnout N', 'Votes']] = (
    df.groupby(['Year', 'NA'])[['Registered Voters', 'Turnout N', 'Votes']].ffill()
)

# Step 2: Drop rows without registered voters or turnout
df = df.dropna(subset=['Registered Voters', 'Turnout N'])

# Step 3: Keep only one row per NA per year (to avoid overcounting)
df = df.drop_duplicates(subset=['Year', 'NA'])

# Step 4: Extract city name from Constituency
df['City'] = df['Constituency'].str.extract(r'NA-\d+\s*-\s*(.*)')
df['City'] = df['City'].str.strip()
df['City'] = df['City'].str.replace(r'\s+\d+$', '', regex=True).str.strip()


# Step 5: Rename and clean numeric columns
df = df.rename(columns={
    'Registered Voters': 'Registered_Voters',
    'Votes': 'Votes_Cast',
    'Turnout N': 'Turnout_Percent'
})
for col in ['Registered_Voters', 'Votes_Cast']:
    df[col] = df[col].astype(str).str.replace(",", "").astype(float)

# Step 6: Group by Year + City and calculate total votes & turnout
grouped = df.groupby(['Year', 'City', 'Province'], as_index=False).agg({
    'Registered_Voters': 'sum',
    'Votes_Cast': 'sum'
})
grouped['Turnout_Percent'] = (grouped['Votes_Cast'] / grouped['Registered_Voters']) * 100

# Step 7: Optional binary classification label
grouped['High_Turnout'] = (grouped['Turnout_Percent'] > 50).astype(int)

# Step 8: Save
grouped.to_csv("data/cleaned_elections.csv", index=False)
print("✅ Cleaned city-wise data saved to data/cleaned_elections.csv")
