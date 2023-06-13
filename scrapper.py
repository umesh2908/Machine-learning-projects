import streamlit as st
import requests
import pandas as pd
import os

# Function to scrape data and save Excel file
def scrape_and_save_data(dt):
    url = "https://oms.nrldc.in/outageReport/genUnitReport.php?start={}&dt={}&owner=&eltype=".format(dt, dt)

    # create a directory to store the downloaded files
    directory = "NRLDC_daily_reports"
    if not os.path.exists(directory):
        os.makedirs(directory)

    df = pd.read_html(url, header=None)
    Planned = df[0].set_axis(['S.No.', 'Station', 'State', 'Owner', 'Unit No.', 'Cap.(MW)', 'Reasons', 'Outage', 'Time', 'Expected revival','Daily'], axis=1, inplace=False)
    Forced = df[1].set_axis(['S.No.', 'Station', 'State', 'Owner', 'Unit No.', 'Cap.(MW)', 'Reasons', 'Outage', 'Time', 'Expected revival'], axis=1, inplace=False)
    Planned.dropna(inplace=True)
    Forced.dropna(inplace=True)
    NRLDC = pd.concat([Planned, Forced])

    # Save NRLDC data in the NRLDC folder
    if not os.path.exists("NRLDC_daily_reports"):
        os.makedirs("NRLDC_daily_reports")

    # path to the new directory
    path = "NRLDC_daily_reports/"

    NRLDC.to_excel(os.path.join(path, "NRLDC_{}.xlsx".format(dt)), index=False)

# Streamlit app
def main():
    st.title("NRLDC Data Scraper")
    st.write("Select a date (DD-MM-YYYY) to scrape data from the NRLDC website and download the output Excel file.")

    # Date selection dropdown
    dt = st.text_input("Enter a date (DD-MM-YYYY)")

    # Scrape and save data
    if st.button("Scrape and Save"):
        if len(dt) == 10 and dt[2] == '-' and dt[5] == '-':
            scrape_and_save_data(dt)
            st.success("Data scraped and saved successfully!")
        else:
            st.error("Invalid date format. Please enter the date in DD-MM-YYYY format.")

    # Download button for the output file
    if os.path.exists("NRLDC_daily_reports"):
        files = os.listdir("NRLDC_daily_reports")
        if len(files) > 0:
            selected_file = st.selectbox("Select the Excel file to download", files)
            if st.button("Download"):
                with open(os.path.join("NRLDC_daily_reports", selected_file), "rb") as file:
                    data = file.read()
                    st.download_button(label="Download Excel", data=data, file_name=selected_file)

if __name__ == "__main__":
    main()

