import streamlit as st
import os
import requests
import zipfile
import tempfile
from datetime import datetime, timedelta

@st.cache
def generate_dates(start_date, end_date):
    start_date_obj = datetime.strptime(start_date, "%d-%m-%Y")
    end_date_obj = datetime.strptime(end_date, "%d-%m-%Y")
    dates = []
    current_date = start_date_obj
    while current_date <= end_date_obj:
        dates.append(current_date.strftime("%d.%m.%y"))
        current_date += timedelta(days=1)
    return dates

def download_reports(start_date, end_date):
    base_url = "https://reporting.wrldc.in/dailyreports/GenOutage/2023/March/WRLDC_GenOutage_Report_"
    dates = generate_dates(start_date, end_date)

    with tempfile.TemporaryDirectory() as temp_dir:
        for date in dates:
            url = f"{base_url}{date}.pdf"
            filename = url.split('/')[-1]
            filepath = os.path.join(temp_dir, filename)
            response = requests.get(url)
            with open(filepath, 'wb') as f:
                f.write(response.content)
        
        # Create a zip file containing the downloaded reports
        zip_filename = "reports.zip"
        zip_filepath = os.path.join(temp_dir, zip_filename)
        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    zipf.write(os.path.join(root, file), file)

        # Provide download link for the zip file
        st.download_button(
            label="Download Reports",
            data=open(zip_filepath, "rb").read(),
            file_name=zip_filename
        )

def main():
    st.title("Report Downloader")
    start_date = st.text_input("Enter start date (DD-MM-YYYY)")
    end_date = st.text_input("Enter end date (DD-MM-YYYY)")
    if st.button("Download Reports"):
        if start_date and end_date:
            download_reports(start_date, end_date)
        else:
            st.warning("Please enter valid start and end dates.")

if __name__ == '__main__':
    main()
