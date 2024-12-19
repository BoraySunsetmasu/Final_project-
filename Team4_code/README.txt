# Stock Analysis and AI Consultation Application

This application is designed for stock data analysis and AI consultation. It provides a user-friendly interface for users to analyze stock trends, compare strategies, and interact with an AI assistant for deeper insights. The system consists of both a frontend (GUI) and backend (API server) that work together seamlessly.

---

## Features

### Frontend
- **Stock Data Query**: Input stock ID, start date, and end date to analyze stock trends.
- **Chart Display**: Visualize stock trends and strategy comparisons with dynamically generated charts.
- **AI Consultation**: Ask the AI assistant questions based on stock data and receive responses.
- **Export Analysis Report**: Download the analysis results as an Excel file.

### Backend
- **Stock Data Analysis**: Fetch and analyze stock data based on user input.
- **Visualization**: Generate charts for stock trends and strategy comparisons.
- **AI Integration**: Use OpenAI's GPT model to answer user queries based on stock data.
- **Excel Report Generation**: Export the analyzed data to an Excel file.

---

## System Architecture

1. **Frontend**: A Python-based GUI built with Tkinter, allowing users to interact with the system.
2. **Backend**: A Flask API server to handle stock analysis requests, data visualization, AI interactions, and file generation.

---

## Installation Guide

### Prerequisites
- Python 3.9 or above
- Required libraries: Flask, pandas, matplotlib, requests, Pillow, tkinter, scikit-learn, openpyxl, and OpenAI's API.

### Backend Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Install required libraries:
   ```bash
   pip install flask pandas matplotlib scikit-learn openpyxl openai
   ```
3. Run the Flask server:
   ```bash
   python server.py
   ```

### Frontend Setup
1. Ensure the backend server is running at `http://127.0.0.1:5000`.
2. Run the Tkinter GUI:
   ```bash
   python frontend.py
   ```

---

## Usage Instructions

### Frontend Application
1. Launch the application by running `Frontend.py`.
2. Enter the required fields:
   - **Stock Number**: Enter the stock ID to analyze.
   - **Start Date**: Input the analysis start date (format: YYYY-MM-DD).
   - **End Date**: Input the analysis end date (format: YYYY-MM-DD).
3. Use the following features:
   - **Start Query**: Fetch stock data and display analysis charts.
   - **Strategy Comparison**: Compare different investment strategies.
   - **Ask AI Advisor**: Input questions for AI consultation.
   - **Download Results**: Export analysis as an Excel file.

### Backend Endpoints
1. **Analyze Stock Data**
   - **Endpoint**: `/api/analyze_data`
   - **Method**: POST
   - **Payload**:
     ```json
     {
       "stock": "2330",
       "start": "2024-01-01",
       "end": "2024-12-01"
     }
     ```
   - **Response**: JSON with data and chart paths.

2. **Strategy Comparison**
   - **Endpoint**: `/api/strategy_comparison`
   - **Method**: POST
   - **Payload**:
     ```json
     {
       "stock": "2330",
       "start": "2024-01-01",
       "end": "2024-12-01"
     }
     ```
   - **Response**: JSON with strategy comparison chart path.

3. **AI Consultation**
   - **Endpoint**: `/api/send_to_gpt`
   - **Method**: POST
   - **Payload**:
     ```json
     {
       "image_paths": ["chart1.png", "chart2.png"],
       "question": "What are the key takeaways from the stock performance?"
     }
     ```
   - **Response**: AI-generated textual analysis.

4. **Download Excel Report**
   - **Endpoint**: `/api/download_excel`
   - **Method**: GET
   - **Query Parameters**: `file_path=path_to_excel_file`
   - **Response**: Excel file content.

---


## Key Modules

### Frontend (Frontend.py)
- **Operation Class**:
  - Handles user input, communicates with the backend, and updates the GUI.
  - Key methods:
    - `submit_form`: Sends stock query to the backend and displays charts.
    - `strategy_comparison`: Displays strategy comparison chart.
    - `gpt_response`: Sends user question to the AI and displays the response.
    - `download_excel`: Downloads the Excel report from the backend.

### Backend (Server.py)
- **Endpoints**:
  - `/api/analyze_data`: Processes stock data and generates charts.
  - `/api/strategy_comparison`: Compares different strategies.
  - `/api/send_to_gpt`: Integrates with OpenAI's GPT for AI consultation.
  - `/api/download_excel`: Exports data to an Excel file.
- **Core Libraries**:
  - `pandas` and `matplotlib` for data processing and visualization.
  - `openpyxl` for Excel generation.

---

## Known Issues
- Ensure the backend server is running before starting the frontend.
- API keys for OpenAI must be correctly configured in `server.py`.
- The application is currently designed for local use; deployment for production requires additional configuration.

---