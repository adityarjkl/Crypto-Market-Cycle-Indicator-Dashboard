import pandas as pd
import re

df = pd.read_csv('Crypto_Market_Cycle_Indicators_export.csv', header=None, skiprows=1,
    names=['ID', 'Indicator', 'Value', 'Percent', 'Target'])

# Clean Value column (currency)
def clean_value(val):
    if isinstance(val, str):
        unit = ''
        if '$' in val:
            unit = '$'
        elif '%' in val:
            unit = '%'
        elif 'M' in val:
            unit = 'Million'
        val = val.replace('$', '').replace(',', '').replace('%', '').replace('M', '')
        try:
            return float(val), unit
        except:
            return val, unit
    else:
        try:
            return float(val), ''
        except:
            return val, ''


df[['Value', 'Value_Unit']] = df['Value'].apply(lambda x: pd.Series(clean_value(x)))

# Replace empty Value_Unit cells with "Float"
df['Value_Unit'] = df['Value_Unit'].replace('', 'Float')



# Clean Target column (extract comparator, value, unit)
def clean_target(tgt):
    m = re.match(r"^\s*(>=|<=|>|<|=)?\s*\$?([\d,\.]+)", str(tgt))
    unit = '$' if '$' in str(tgt) else ''
    if m:
        comp = m.group(1) if m.group(1) else "="
        val = float(m.group(2).replace(',',''))
        return comp, val, unit
    else:
        return '=', tgt, ''
df[['Target_Comparator', 'Target_Value', 'Target_Unit']] = df['Target'].apply(lambda x: pd.Series(clean_target(x)))

# Drop the Percent column
df = df.drop(columns=['Percent'])

# Reorder columns to keep Value_Unit right after Value
desired_order = ['ID', 'Indicator', 'Value', 'Value_Unit', 'Target', 'Target_Comparator', 'Target_Value', 'Target_Unit']
df = df[desired_order]

# Save cleaned data
df.to_csv('Cleaned_Crypto_Market_Cycle_Indicators.csv',index=False)