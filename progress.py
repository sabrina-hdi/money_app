import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

class ProgressMonitor:
    def __init__(self):
        # Ensure session state variables are initialized
        if 'transactions' not in st.session_state:
            st.session_state.transactions = []
        if 'goal_amt' not in st.session_state:
            st.session_state.goal_amt = 0.0
        if 'goal_start' not in st.session_state:
            st.session_state.goal_start = datetime.today().date()  # Use date object
        if 'goal_end' not in st.session_state:
            st.session_state.goal_end = datetime.today().date()  # Use date object

    def load_data(self, file_path):
        """Load data from CSV file."""
        try:
            data = pd.read_csv(file_path)
            return data
        except FileNotFoundError:
            st.error("File not found.")
            return pd.DataFrame()

    def calculate_progress(self, data):
        """Calculate the progress towards the savings goal."""
        # Filter transactions within the goal period
        data['date'] = pd.to_datetime(data['date']).dt.date  # Convert to date
        goal_data = data[(data['date'] >= st.session_state.goal_start) & 
                         (data['date'] <= st.session_state.goal_end)]

        # Calculate total savings (total income minus total spending)
        total_income = goal_data[goal_data['amount'] > 0]['amount'].sum()
        total_spending = abs(goal_data[goal_data['amount'] < 0]['amount'].sum())
        total_savings = total_income - total_spending

        # Calculate progress percentage
        progress_percentage = (total_savings / st.session_state.goal_amt) * 100 if st.session_state.goal_amt > 0 else 0

        # Ensure all dates are date objects for compatibility
        today_date = datetime.today().date()  # Convert to date
        goal_start_date = st.session_state.goal_start
        goal_end_date = st.session_state.goal_end

        # Calculate time progress based on the current date
        days_passed = (today_date - goal_start_date).days
        total_days = (goal_end_date - goal_start_date).days
        time_progress = (days_passed / total_days) * 100 if total_days > 0 else 0

        return progress_percentage, time_progress

    def display_progress(self):
        """Displays the progress in the Streamlit app."""
        # Load the data from session state or CSV
        data = pd.DataFrame(st.session_state.transactions, columns=['date', 'genre', 'amount'])

        # Calculate the progress
        progress_percentage, time_progress = self.calculate_progress(data)

        # Display the progress
        st.write("貯金目標の進捗状況:")
        st.progress(progress_percentage / 100)  # Progress bar for savings goal
        st.write(f"進捗率: {progress_percentage:.2f}%")
        st.write(f"目標期間の進捗: {time_progress:.2f}% 経過")

def main():
    # Instantiate the progress monitor
    progress_monitor = ProgressMonitor()

    st.title("Savings Progress Monitor")

    # File uploader to load the CSV
    uploaded_file = st.file_uploader("Upload the transactions CSV", type=["csv"])

    if uploaded_file is not None:
        # Load data from the uploaded file
        data = pd.read_csv(uploaded_file)

        # Display raw data
        st.subheader("Raw Data")
        st.dataframe(data)

        # Save the data to session state for use in display_progress
        st.session_state.transactions = data.to_dict('records')

        # Display the progress
        progress_monitor.display_progress()

        # Provide a download button for the updated data if needed
        updated_csv = data.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="Download updated CSV",
            data=updated_csv,
            file_name="updated_transactions.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
