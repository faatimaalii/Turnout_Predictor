import matplotlib.pyplot as plt
import pandas as pd

df=pd.read_csv("data/cleaned_elections.csv")
df["Year"] = df["Year"].astype(int)
df["Turnout_Percent"] = df["Turnout_Percent"].astype(float)

# Group by Year to get average turnout
yearly_avg = df.groupby("Year")["Turnout_Percent"].mean().reset_index()

# Create subplots
fig, ax = plt.subplots(figsize=(10, 5))

# Scatter individual constituency turnout (optional)
ax.scatter(df["Year"], df["Turnout_Percent"], alpha=0.3, label="Constituencies", color="gray")

# Line for average turnout per year
ax.plot(yearly_avg["Year"], yearly_avg["Turnout_Percent"], marker='o', color="blue", label="Avg Turnout")

# Customize
ax.set_title("Voter Turnout Trends in Pakistan (1970–2024)", fontsize=14)
ax.set_xlabel("Election Year")
ax.set_ylabel("Turnout (%)")
ax.legend()
ax.grid(True)

# Show plot
plt.tight_layout()
#plt.show()


df["Year"] = df["Year"].astype(int)
df["Turnout_Percent"] = df["Turnout_Percent"].astype(float)

# Get list of unique provinces
provinces = df["Province"].dropna().unique()

# Create subplot grid (2 columns, adjust rows based on number of provinces)
n = len(provinces)
cols = 2
rows = (n + 1) // cols

fig, axes = plt.subplots(rows, cols, figsize=(12, 4 * rows), sharey=True)
axes = axes.flatten()  # Flatten in case of single row

# Loop over provinces and plot
for i, province in enumerate(provinces):
    ax = axes[i]
    
    province_data = df[df["Province"] == province]
    yearly_avg = province_data.groupby("Year")["Turnout_Percent"].mean().reset_index()
    
    ax.plot(yearly_avg["Year"], yearly_avg["Turnout_Percent"], marker='o', color="teal")
    ax.set_title(f"{province} - Turnout Over Time")
    ax.set_xlabel("Year")
    ax.set_ylabel("Turnout (%)")
    ax.grid(True)

# Remove any unused subplots
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

# Final layout
plt.tight_layout()
plt.suptitle("Voter Turnout Trends by Province (1970–2024)", fontsize=16, y=1.02)
plt.show()
fig.savefig("plots/province-vise-turnout.png")
