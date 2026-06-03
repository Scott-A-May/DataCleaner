import pandas as pd
import numpy as np

# Creates a realistic messy dataset to test our cleaner on
data = {
    "  First Name  ": ["john", "JANE", "Bob", "john", "SARAH", "mike", None, "LISA", "tom", "KAREN"],
    "Last Name":      ["smith", "DOE", "Johnson", "smith", "Williams", "BROWN", "Davis", "WILSON", None, "moore"],
    "  State  ":      ["Minnesota", "WISCONSIN", "illinois", "Minnesota", "IOWA", "michigan", "Wisconsin", "ILLINOIS", "iowa", "minnesota"],
    "Income":         ["75000", "82000", "91000", "75000", "68000", "UNKNOWN", "77000", "95000", "71000", "88000"],
    "Home Value":     [250000, 310000, 275000, 250000, 198000, 225000, 289000, 415000, 210000, 330000],
    "  Zip Code  ":   ["55401", "53201", "60601", "55401", "50301", "48201", "53202", "60602", "50302", "55402"],
}

df = pd.DataFrame(data)
df.to_csv("messy_data.csv", index=False)
print("Messy test file created: messy_data.csv")