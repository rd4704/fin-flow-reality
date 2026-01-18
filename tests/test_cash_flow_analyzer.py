import pytest
from src.utils.cash_flow_analyzer import calculate_average_monthly_outflow, determine_liquidity_locked

def test_calculate_average_monthly_outflow():
    transactions = [
        {"Date": "2023-01-01", "Amount": 1000, "Type": "Inflow"},
        {"Date": "2023-01-15", "Amount": 500, "Type": "Outflow"},
        {"Date": "2023-02-01", "Amount": 1500, "Type": "Inflow"},
        {"Date": "2023-02-15", "Amount": 700, "Type": "Outflow"},
    ]
    average_outflow = calculate_average_monthly_outflow(transactions)
    assert average_outflow == 350  # (500 + 700) / 2

def test_determine_liquidity_locked():
    transactions = [
        {"Date": "2023-01-01", "Amount": 1000, "Type": "Inflow", "Status": "Paid"},
        {"Date": "2023-01-15", "Amount": 500, "Type": "Outflow", "Status": "Pending"},
        {"Date": "2023-02-01", "Amount": 1500, "Type": "Inflow", "Status": "Paid"},
        {"Date": "2023-02-15", "Amount": 700, "Type": "Outflow", "Status": "Pending"},
    ]
    liquidity_locked = determine_liquidity_locked(transactions)
    assert liquidity_locked == 1200  # 500 + 700 from Pending transactions