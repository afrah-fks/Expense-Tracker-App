import pandas as pd

def clean_and_feature_engineer(df):
    """Cleans data and adds time-based features for analysis."""
    # Ensure Date is datetime objects
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Feature Engineering
    df['Month'] = df['Date'].dt.strftime('%b %Y')
    df['Month_Sort'] = df['Date'].dt.strftime('%Y%m') # For correct sorting
    df['Day_Name'] = df['Date'].dt.day_name()
    df['Is_Weekend'] = df['Day_Name'].isin(['Saturday', 'Sunday'])
    
    return df