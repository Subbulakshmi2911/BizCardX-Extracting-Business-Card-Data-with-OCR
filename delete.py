import streamlit as st
import mysql.connector
import pandas as pd

def app():
    st.title(":red[Delete Data from Database]")

    # Connect to the MySQL database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="Bizcard"
    )
    cursor = mydb.cursor()

    # Fetch names from the database for selection
    cursor.execute("SELECT DISTINCT NAME FROM bizcard_details")
    names = [row[0] for row in cursor.fetchall()]

    col1, col2 = st.columns(2)

    with col1:
        # Dropdown to select a name
        name_select = st.selectbox("Select the Name", names)

    if name_select:
        # Fetch designations based on the selected name
        cursor.execute("SELECT DESIGNATION FROM bizcard_details WHERE NAME = %s", (name_select,))
        designations = [row[0] for row in cursor.fetchall()]

        with col2:
            # Dropdown to select a designation based on the selected name
            designation_select = st.selectbox("Select the Designation", options=designations)

        if designation_select:
            col1, col2, col3 = st.columns(3)

            with col1:
                st.write(f"Selected Name: **{name_select}**")
                st.write(f"Selected Designation: **{designation_select}**")

            with col2:
                # Button to delete the selected record
                if st.button("Delete", use_container_width=True):
                    # Use parameterized query for secure deletion
                    delete_query = "DELETE FROM bizcard_details WHERE NAME = %s AND DESIGNATION = %s"
                    cursor.execute(delete_query, (name_select, designation_select))
                    mydb.commit()

                    st.warning("Record deleted successfully!")

    # Close the cursor and database connection
    cursor.close()
    mydb.close()
