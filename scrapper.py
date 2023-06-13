# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 11:08:02 2023

@author: u56170
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 10:52:39 2023

@author: u56170
"""

import streamlit as st
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
    Planned = df[0].set_axis(['S.No.', 'Station', 'State', 'Owner', 'Unit No.', 'Cap.(MW)', 'Reasons', 'Outage', 'Time', 'Expected revival'], axis=1, inplace=False)
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
    st.write("Select a date to scrape data from the NRLDC website and download the output Excel file.")

    # Date selection dropdown
    dt = st.date_input("Select a date")

    # Scrape and save data
    if st.button("Scrape and Save"):
        scrape_and_save_data(dt.strftime("%d-%m-%Y"))
        st.success("Data scraped and saved successfully!")

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
