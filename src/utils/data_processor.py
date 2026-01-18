def load_and_process_csv(file):
    import pandas as pd

    # Load the CSV file
    df = pd.read_csv(file)

    # Data cleaning: Remove rows with missing values
    df.dropna(inplace=True)

    # Convert 'Date' column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Ensure 'Amount' is numeric
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')

    # Filter out any rows where 'Amount' could not be converted
    df.dropna(subset=['Amount'], inplace=True)

    return df

def generate_mock_data():
    import pandas as pd
    from datetime import datetime, timedelta
    import random

    # Generate a realistic 50-transaction dataset for Asian SMEs
    random.seed(42)  # For reproducible demo data
    
    # Realistic customer/vendor names for Asian SME context
    customers = ['Acme Corp SG', 'TechVision Ltd', 'Global Traders HK', 'Metro Solutions', 'Pacific Imports']
    vendors = ['Office Supplies Co', 'Cloud Services Inc', 'Utilities Provider', 'Marketing Agency', 'Logistics Partner']
    
    transactions = []
    base_date = datetime.now() - timedelta(days=90)
    
    for i in range(50):
        transaction_date = base_date + timedelta(days=random.randint(0, 90))
        
        # 60% inflows, 40% outflows (typical for healthy business)
        is_inflow = random.random() < 0.6
        
        if is_inflow:
            description = random.choice(customers)
            amount = round(random.uniform(2000, 15000), 2)
            trans_type = 'Inflow'
            # 70% paid, 30% pending for inflows
            status = 'Paid' if random.random() < 0.7 else 'Pending'
        else:
            description = random.choice(vendors)
            amount = -round(random.uniform(500, 5000), 2)
            trans_type = 'Outflow'
            # 90% paid, 10% pending for outflows
            status = 'Paid' if random.random() < 0.9 else 'Pending'
        
        transactions.append({
            'Date': transaction_date.strftime('%Y-%m-%d'),
            'Description': description,
            'Amount': amount,
            'Type': trans_type,
            'Status': status
        })
    
    # Sort by date
    mock_data = pd.DataFrame(transactions)
    mock_data = mock_data.sort_values('Date').reset_index(drop=True)
    
    return mock_data