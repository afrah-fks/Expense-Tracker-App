import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_synthetic_data(n_rows=500):
    """Generates a synthetic financial dataset."""
    np.random.seed(42)
    categories = ['Food', 'Transport', 'Rent', 'Entertainment', 'Utilities', 'Shopping', 'Healthcare']
    payment_methods = ['Credit Card', 'Debit Card', 'Cash', 'UPI']
    
    # Generate dates over the last 6 months
    start_date = datetime.now() - timedelta(days=180)
    dates = [start_date + timedelta(days=np.random.randint(0, 180)) for _ in range(n_rows)]
    
    data = {
        'Date': dates,
        'Category': np.random.choice(categories, n_rows),
        'Amount': np.round(np.random.uniform(5, 500), 2),
        'Payment_Method': np.random.choice(payment_methods, n_rows)
    }
    
    df = pd.DataFrame(data)
    
    # Logic: Rent is always high and occurs once a month
    df.loc[df['Category'] == 'Rent', 'Amount'] = np.random.uniform(1000, 1200)
    
    return df.sort_values(by='Date')