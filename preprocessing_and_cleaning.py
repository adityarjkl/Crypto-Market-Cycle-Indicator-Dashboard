import pandas as pd
import re

# Load CSV with correct column names
df = pd.read_csv(
    'Crypto_Market_Cycle_Indicators_export.csv',
    header=None,
    skiprows=1,
    names=['ID', 'Indicator', 'Value', 'Percent', 'Reference_Value']
)

# Clean Value column and extract unit
def clean_value(val):
    if not isinstance(val, str):
        try:
            return float(val), 'Float'
        except:
            return val, 'Float'
    unit = (
        '$' if '$' in val else
        '%' if '%' in val else
        'Million' if 'M' in val else
        'Float'
    )
    val_clean = val.replace('$', '').replace(',', '').replace('%', '').replace('M', '')
    try:
        return float(val_clean), unit
    except:
        return val_clean, unit

df[['Current Value', 'Current Value Unit']] = df['Value'].apply(lambda x: pd.Series(clean_value(x)))



# Ref Value: strip symbols, keep as int/float if possible
def strip_symbols_and_convert(val):
    val_str = str(val)
    clean_val = re.sub(r'[><=$%,M≥≤]', '', val_str).replace(',', '').strip()
    try:
        num = float(clean_val)
        return int(num) if num.is_integer() else num
    except:
        return clean_val

df['Ref Value'] = df['Reference_Value'].apply(strip_symbols_and_convert)


# Ref Value Unit: extract unit from Reference_Value
def extract_unit(val):
    val_str = str(val)
    if '$' in val_str:
        return '$'
    if 'M' in val_str:
        return 'Million'
    if '%' in val_str:
        return '%'
    return 'Float'

df['Ref Value Unit'] = df['Reference_Value'].apply(extract_unit)

# Format Ref Value column to two decimal places if it's a number
df['Ref Value'] = df['Ref Value'].apply(lambda x: f"{x:.2f}" if isinstance(x, float) else x)


# Final column order
desired_order = [
    'ID', 'Indicator', 'Current Value', 'Current Value Unit',
    'Reference_Value', 'Ref Value', 'Ref Value Unit'
]
df = df[desired_order]

# Save cleaned data
df.to_csv('Cleaned_Crypto_Market_Cycle_Indicators.csv', index=False)