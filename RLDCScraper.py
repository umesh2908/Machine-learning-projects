import streamlit as st
import os
import requests
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
    folder_name = "reports"
    dates = generate_dates(start_date, end_date)
    os.makedirs(folder_name, exist_ok=True)
    for date in dates:
        url = f"{base_url}{date}.pdf"
        filename = url.split('/')[-1]
        filepath = os.path.join(folder_name, filename)
        if os.path.exists(filepath):
            st.write(f'The file {filename} already exists in the {folder_name} directory.')
        else:
            response = requests.get(url)
            with open(filepath, 'wb') as f:
                f.write(response.content)
                st.write(f'The file {filename} has been downloaded and saved in the {folder_name} directory.')

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
