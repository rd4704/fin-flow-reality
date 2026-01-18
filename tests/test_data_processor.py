import pandas as pd
import pytest
from src.utils.data_processor import process_transactions

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'Date': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'Description': ['Salary', 'Groceries', 'Utilities'],
        'Amount': [5000, -150, -100],
        'Type': ['Inflow', 'Outflow', 'Outflow'],
        'Status': ['Paid', 'Paid', 'Paid']
    })

def test_process_transactions(sample_data):
    processed_data = process_transactions(sample_data)
    assert processed_data is not None
    assert len(processed_data) == 3
    assert processed_data['Amount'].sum() == 4750  # 5000 - 150 - 100

def test_process_transactions_empty_data():
    empty_data = pd.DataFrame(columns=['Date', 'Description', 'Amount', 'Type', 'Status'])
    processed_data = process_transactions(empty_data)
    assert processed_data.empty

def test_process_transactions_invalid_data():
    invalid_data = pd.DataFrame({
        'Date': ['2023-01-01', '2023-01-02'],
        'Description': ['Salary', 'Groceries'],
        'Amount': ['5000', '-150'],  # Invalid types
        'Type': ['Inflow', 'Outflow'],
        'Status': ['Paid', 'Paid']
    })
    with pytest.raises(ValueError):
        process_transactions(invalid_data)