#Importing necessary libraries
import numpy as np
import pandas as pd
import statistics
import matplotlib.pyplot as plt

print("Project Code: Snake venoms - Behaviour and Toxicity")

#Refer to the CSV file used before
df = pd.read_csv("Project/Venomous Snakes.csv")
#Get the names of the columns in the dataset and remove spaces around the column names to use them accurately in the code (debugging)
df.columns = df.columns.str.strip()
print(df.columns)

#Question 1 analysis
#Calculate the skewness of the LD50 (toxicity) data
ld50_data = pd.to_numeric(
    df["LD50 (mg/kg, SC)"].astype(str).str.extract(r"(\d+(?:\.\d+)?)")[0],
    errors="coerce"
).dropna() #Extract the numerical value only of the dataset in LD50
skewness = ld50_data.skew()
print(f"Skewness of LD50 data: {skewness}")

#Calculate the kurtosis of the LD50 data
kurtosis = ld50_data.kurtosis()
print(f"Kurtosis of LD50 data: {kurtosis}")

#Plot the histogram of the LD50 data
plt.hist(ld50_data, bins=20, color='green', edgecolor='black')
plt.xlabel("LD50 (mg/kg, SC)")
plt.ylabel("Frequency")
plt.title("The Distribution of Toxicity (LD50) in venomous snakes")
#Save the figure as a PNG file with high resolution and tight layout
plt.savefig('venom_toxicity_distribution.png', dpi=300, bbox_inches='tight')
plt.show()


#Question 2 analysis
#Transform qualitative description of behaviour into a quantitative score scale from 0 until 5
def agression_score(behaviour):
    #Check any missing values in Behaviour column first
    if pd.isna(behaviour):
        return np.nan
    #Because of a misspeling of agression in the dataset, all "aggressive" with be put to the same
    behaviour = behaviour.lower().replace("agressive", "aggressive")
    #Score assignment
    #Most agressive behaviour has a 5
    if "very aggressive" in behaviour or "extremely aggressive" in behaviour or "highly aggressive" in behaviour:
        return 5
    #Still highly agressive behaviour has a 4
    elif "highly defensive" in behaviour or "very defensive" in behaviour or "extremely defensive" in behaviour:
        return 4
    #Agressive behaviour when triggered has a 3
    elif "aggressive" in behaviour and ("threatened" in behaviour or "disturbed" in behaviour or "provoked" in behaviour):
        return 3
    #Defensive behaviour has a 2
    elif "defensive" in behaviour or "will defend if cornered" in behaviour or "threat display" in behaviour or "rattle" in behaviour or "hiss" in behaviour or "puffs" in behaviour or "spits venom" in behaviour:
        return 2
    #Avoids or barelly behaviour has a 1
    elif "typically avoids confrontation" in behaviour or "cautious" in behaviour or "avoids confrontation" in behaviour or "shy" in behaviour or "reclusive" in behaviour or "secretive" in behaviour or "evasive" in behaviour or "elusive" in behaviour:
        return 1
    #Passive behaviour has a 0
    elif "passive" in behaviour or "not aggressive" in behaviour or "calm" in behaviour or "docile" in behaviour:
        return 0
    #Not actual information about their behaviour
    else:
        return None


#Statistical analysis
#Make the agression score column with LD50 values
df["Agression score"] = df["Behaviour"].apply(agression_score)

#Mean and uncertainty of LD50 (toxicity) for each score
means = []
scores = []
stdevs = []
for score in range(6):
    data = df[df["Agression score"] == score] ["LD50 (mg/kg, SC)"]
    data = pd.to_numeric(
        data.astype(str).str.extract(r"(\d+(?:\.\d+)?)")[0],
        errors="coerce"
    ).dropna() #Extract the numerical value only of the dataset in LD50
   
    mean = statistics.mean(data)
    stdev = statistics.stdev(data)

    #Save the data calculated
    means.append(mean)
    scores.append(score)
    stdevs.append(stdev)

    print(f"Score {score}:")
    print(f"Mean LD50 = {mean}") 
    print(f"Uncertainty = {stdev}")

#Calculate the correlation coefficient (r) between the agression score and mean LD50
r = np.corrcoef(scores, means)[0, 1]
print(f"Correlation coefficient (r) = {r:.2f}")

#Relationship graph of agressive score over toxicity LD50
plt.scatter(scores, means, color='darkblue', label='Mean LD50 (toxicity) per agression score')
plt.xlim(1, 5)
#Calculate the trendline of the data
coefficients = np.polyfit(scores, means, 1)
trendline = np.poly1d(coefficients)
plt.plot(scores, trendline(scores), color='green', linestyle='-', label='Trendline')
#Add error bars to the data points
plt.errorbar(scores, means, yerr=stdevs, fmt='o', color='blue', ecolor='red', capsize=5, label='Uncertainty of mean LD50')
#Add labels and title to the graph
plt.xlabel("Agression score")
plt.ylabel("Mean LD50 (in mg/kg, SC)")
plt.title("Relationship between Behaviour and Toxicity (LD50) in venomous Snakes")
plt.legend()
#Save the figure as a PNG file with high resolution and tight layout
plt.savefig('behaviour_toxicity_relationship.png', dpi=300, bbox_inches='tight')
plt.show()
