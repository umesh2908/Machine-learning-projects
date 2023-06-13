import streamlit as st
import requests
import pandas as pd
import os

# Function to scrape data and save Excel file
def scrape_and_save_data(dt):
    url = "https://oms.nrldc.in/outageReport/genUnitReport.php?start={}&dt={}&owner=&eltype=".format(dt, dt)

    df = pd.read_html(url, header=None)
    Planned = df[0].set_axis(['S.No.', 'Station', 'State', 'Owner', 'Unit No.', 'Cap.(MW)', 'Reasons', 'Outage', 'Time', 'Expected revival', 'Daily'], axis=1, inplace=False)
    Forced = df[1].set_axis(['S.No.', 'Station', 'State', 'Owner', 'Unit No.', 'Cap.(MW)', 'Reasons', 'Outage', 'Time', 'Expected revival'], axis=1, inplace=False)
    Planned.dropna(inplace=True)
    Forced.dropna(inplace=True)
    NRLDC = pd.concat([Planned, Forced])

    NRLDC.to_excel("NRLDC_{}.xlsx".format(dt), index=False)

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
    
     selected_file = st.selectbox("Select the Excel file to download", NLDC)
     if st.button("Download"):
        st.download_button(label="Download Excel", file_name=selected_file)

if __name__ == "__main__":
    main()

