import pandas as pd
import streamlit as st
from utils.data_processor import load_and_process_csv, generate_mock_data


def upload_file():
    """
    Handle CSV file upload and return processed DataFrame.
    
    Returns:
        DataFrame or None: Processed transaction data.
    """
    st.sidebar.header("📊 Data Source")
    
    uploaded_file = st.sidebar.file_uploader("Upload Transaction CSV", type="csv")
    
    if uploaded_file is not None:
        try:
            df = load_and_process_csv(uploaded_file)
            st.sidebar.success(f"✅ Loaded {len(df)} transactions")
            return df
        except Exception as e:
            st.sidebar.error(f"Error loading file: {str(e)}")
            return None
    
    # Sample data button
    if st.sidebar.button("🎲 Load Sample Data (50 Transactions)"):
        sample_data = generate_mock_data()
        st.sidebar.success(f"✅ Loaded {len(sample_data)} sample transactions")
        return sample_data
    
    return None