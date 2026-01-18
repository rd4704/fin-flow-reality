# FinFlow Reality

FinFlow Reality is a Streamlit application designed to help users visualize their cash flow differences by analyzing transaction data. Users can upload their transaction CSV files and gain insights into their financial health through interactive visualizations.

## Features

- **CSV File Upload**: Users can upload their transaction data in CSV format.
- **Data Visualization**: Interactive charts to visualize cash flow trends and identify cash crunch areas.
- **Data Processing**: The application processes and cleans the uploaded data for accurate analysis.
- **Sample Data**: Users can load sample transaction data for testing and demonstration purposes.

## Project Structure

```
finflow-reality
├── src
│   ├── app.py
│   ├── components
│   │   ├── __init__.py
│   │   ├── file_upload.py
│   │   └── visualizations.py
│   ├── utils
│   │   ├── __init__.py
│   │   ├── data_processor.py
│   │   └── cash_flow_analyzer.py
│   └── config
│       ├── __init__.py
│       └── settings.py
├── tests
│   ├── __init__.py
│   ├── test_data_processor.py
│   └── test_cash_flow_analyzer.py
├── data
│   └── sample_transactions.csv
├── requirements.txt
├── .streamlit
│   └── config.toml
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/finflow-reality.git
   cd finflow-reality
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit application:
   ```
   streamlit run src/app.py
   ```

2. Open your web browser and navigate to `http://localhost:8501` to access the application.

3. Upload your CSV file containing transaction data or use the sample data provided.

4. Explore the visualizations to analyze your cash flow.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.