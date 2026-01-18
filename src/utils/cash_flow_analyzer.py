import pandas as pd
from datetime import timedelta


def calculate_average_monthly_outflow(transactions):
    """
    Calculate the average monthly outflow from the transactions.

    Args:
        transactions (DataFrame): A DataFrame containing transaction data.

    Returns:
        float: The average monthly outflow (absolute value).
    """
    outflows = transactions[transactions['Type'] == 'Outflow'].copy()
    if len(outflows) == 0:
        return 0
    
    outflows['Date'] = pd.to_datetime(outflows['Date'])
    outflows.set_index('Date', inplace=True)
    monthly_outflows = outflows.resample('M').sum()
    average_monthly_outflow = abs(monthly_outflows['Amount'].mean())
    return average_monthly_outflow


def calculate_liquidity_locked(transactions):
    """
    Determine the potential liquidity locked based on pending INFLOW transactions.

    Args:
        transactions (DataFrame): A DataFrame containing transaction data.

    Returns:
        float: The total liquidity locked (positive value).
    """
    pending_inflows = transactions[(transactions['Type'] == 'Inflow') & (transactions['Status'] == 'Pending')]
    total_liquidity_locked = pending_inflows['Amount'].sum()
    return total_liquidity_locked


def get_top_offenders(transactions, top_n=5):
    """
    Identify customers with the most pending cash (liquidity locked).

    Args:
        transactions (DataFrame): A DataFrame containing transaction data.
        top_n (int): Number of top offenders to return.

    Returns:
        DataFrame: Top customers with pending amounts.
    """
    pending_inflows = transactions[(transactions['Type'] == 'Inflow') & (transactions['Status'] == 'Pending')]
    
    if len(pending_inflows) == 0:
        return pd.DataFrame(columns=['Customer', 'Locked Amount'])
    
    top_customers = pending_inflows.groupby('Description')['Amount'].sum().sort_values(ascending=False).head(top_n)
    
    result_df = pd.DataFrame({
        'Customer': top_customers.index,
        'Locked Amount': top_customers.values
    }).reset_index(drop=True)
    
    return result_df


def calculate_cumulative_cash_flow(transactions, delay_days=0, reality_mode=False):
    """
    Calculate cumulative cash flow with optional delay factor for pending inflows.

    Args:
        transactions (DataFrame): A DataFrame containing transaction data.
        delay_days (int): Number of days to delay pending inflows.
        reality_mode (bool): If True, apply delay to pending inflows.

    Returns:
        tuple: (dates, cumulative_balance) for plotting.
    """
    df = transactions.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Apply reality delay to pending inflows
    if reality_mode and delay_days > 0:
        pending_mask = (df['Type'] == 'Inflow') & (df['Status'] == 'Pending')
        df.loc[pending_mask, 'Date'] = df.loc[pending_mask, 'Date'] + timedelta(days=delay_days)
    
    # Sort by date and calculate cumulative sum
    df = df.sort_values('Date')
    df['Cumulative'] = df['Amount'].cumsum()
    
    return df['Date'], df['Cumulative']


def calculate_metrics(transactions, delay_days=0):
    """
    Calculate key metrics for the dashboard.

    Args:
        transactions (DataFrame): A DataFrame containing transaction data.
        delay_days (int): Customer delay factor in days.

    Returns:
        dict: Dictionary containing current balance, 30-day gap, and risk level.
    """
    # Current balance (all paid transactions)
    paid_transactions = transactions[transactions['Status'] == 'Paid']
    current_balance = paid_transactions['Amount'].sum()
    
    # Optimistic 30-day projection
    _, optimistic_flow = calculate_cumulative_cash_flow(transactions, delay_days=0, reality_mode=False)
    optimistic_30day = optimistic_flow.iloc[-1] if len(optimistic_flow) > 0 else current_balance
    
    # Reality 30-day projection
    _, reality_flow = calculate_cumulative_cash_flow(transactions, delay_days=delay_days, reality_mode=True)
    reality_30day = reality_flow.iloc[-1] if len(reality_flow) > 0 else current_balance
    
    # Gap and risk assessment
    projected_gap = optimistic_30day - reality_30day
    
    # Risk level based on reality projection
    if reality_30day < 0:
        risk_level = "🔴 High"
    elif reality_30day < 5000:
        risk_level = "🟡 Medium"
    else:
        risk_level = "🟢 Low"
    
    return {
        'current_balance': current_balance,
        'projected_gap': projected_gap,
        'risk_level': risk_level,
        'optimistic_30day': optimistic_30day,
        'reality_30day': reality_30day
    }


def analyze_cash_flow(transactions):
    """
    Analyze cash flow based on the provided transactions.

    Args:
        transactions (DataFrame): A DataFrame containing transaction data.

    Returns:
        dict: A dictionary containing analysis results.
    """
    average_outflow = calculate_average_monthly_outflow(transactions)
    liquidity_locked = calculate_liquidity_locked(transactions)
    
    analysis_results = {
        'average_monthly_outflow': average_outflow,
        'total_liquidity_locked': liquidity_locked
    }
    
    return analysis_results