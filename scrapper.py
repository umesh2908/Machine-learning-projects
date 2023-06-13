import streamlit as st
import pandas as pd

# Function to scrape data and save Excel file
def scrape_and_save_data(dt):
    url = "https://oms.nrldc.in/outageReport/genUnitReport.php?start={}&dt={}&owner=&eltype=".format(dt, dt)

    df = pd.read_html(url, header=None)
    Planned = df[0].set_axis(['S.No.', 'Station', 'State', 'Owner', 'Unit No.', 'Cap.(MW)', 'Reasons', 'Outage', 'Time', 'Expected revival', 'Unnamed'], axis=1, inplace=False)
    Forced = df[1].set_axis(['S.No.', 'Station', 'State', 'Owner', 'Unit No.', 'Cap.(MW)', 'Reasons', 'Outage', 'Time', 'Expected revival'], axis=1, inplace=False)
    Planned.dropna(inplace=True)
    Forced.dropna(inplace=True)
    NRLDC = pd.concat([Planned, Forced])

    NRLDC.to_excel("NRLDC_{}.xlsx".format(dt), index=False)

# Streamlit app
def main():
    st.title("NRLDC Data Scraper")
    st.write("Enter a date in DD-MM-YYYY format to scrape data from the NRLDC website and save it as an Excel file.")

    # Date input
    dt = st.text_input("Enter a date (DD-MM-YYYY)")

    # Scrape and save data
    if st.button("Scrape and Save"):
        scrape_and_save_data(dt)
        st.success("Data scraped and saved successfully!")

if __name__ == "__main__":
    main()
