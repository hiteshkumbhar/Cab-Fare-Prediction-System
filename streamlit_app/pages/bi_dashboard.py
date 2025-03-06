import streamlit as st

import streamlit as st

def bi_dashboard_page():
    st.subheader("Business Intelligence Dashboard")
    st.write("Insights on Cab Fare Trends.")

    # Power BI Report Embed URL
    
    power_bi_url = "https://app.powerbi.com/view?r=eyJrIjoiODA2NzAwNGUtMGNkNC00OTkwLWI5Y2YtZDMzZWJiZDdkOWU2IiwidCI6IjNjYjkxMTI3LTkyNDMtNGQ1Yy04NWJiLTM2Zjc4YTIwMDA2MiJ9"

    # Embed Power BI report using iframe
    st.components.v1.iframe(power_bi_url, width=900, height=600)

# Call the function if running the script directly
if __name__ == "__main__":
    bi_dashboard_page()
