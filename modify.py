import streamlit as st
import mysql.connector
import pandas as pd

def app():
    st.title(":red[Modify the Extracted Business Card Data]")
    method = st.radio("Select the Method", [ "Preview", "Modify"])

    # Connect to the MySQL database once
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="Bizcard"
    )
    cursor = mydb.cursor()

    if method == "None":
        st.write("")

    elif method == "Preview":
        # Select query to preview all records
        select_query = "SELECT * FROM bizcard_details"
        cursor.execute(select_query)
        table = cursor.fetchall()
        table_df = pd.DataFrame(table, columns=("NAME", "DESIGNATION", "COMPANY_NAME", "CONTACT", "EMAIL", "WEBSITE",
                                                "ADDRESS", "PINCODE", "IMAGE"))
        st.dataframe(table_df)

    elif method == "Modify":
        # Select query to fetch all records for modification
        select_query = "SELECT * FROM bizcard_details"
        cursor.execute(select_query)
        table = cursor.fetchall()
        table_df = pd.DataFrame(table, columns=("NAME", "DESIGNATION", "COMPANY_NAME", "CONTACT", "EMAIL", "WEBSITE",
                                                "ADDRESS", "PINCODE", "IMAGE"))

        col1, col2 = st.columns(2)
        with col1:
            # Select a name for modification
            selected_name = st.selectbox("Select the name", table_df["NAME"])

            # Filter the DataFrame based on the selected name
            df_3 = table_df[table_df["NAME"] == selected_name]
            df_4 = df_3.copy()

        # Input fields for modification
        col1, col2 = st.columns(2)
        with col1:
            mo_name = st.text_input("Name", df_3["NAME"].iloc[0])
            mo_desi = st.text_input("Designation", df_3["DESIGNATION"].iloc[0])
            mo_com_name = st.text_input("Company Name", df_3["COMPANY_NAME"].iloc[0])
            mo_contact = st.text_input("Contact", df_3["CONTACT"].iloc[0])
            mo_email = st.text_input("Email", df_3["EMAIL"].iloc[0])

            # Update modified values
            df_4["NAME"] = mo_name
            df_4["DESIGNATION"] = mo_desi
            df_4["COMPANY_NAME"] = mo_com_name
            df_4["CONTACT"] = mo_contact
            df_4["EMAIL"] = mo_email

        with col2:
            mo_website = st.text_input("Website", df_3["WEBSITE"].iloc[0])
            mo_addre = st.text_input("Address", df_3["ADDRESS"].iloc[0])
            mo_pincode = st.text_input("Pincode", df_3["PINCODE"].iloc[0])

            # Binary data (e.g., IMAGE) handling; here we avoid displaying the image directly in a text field
            st.image(df_3["IMAGE"].iloc[0], caption="Business Card Image", use_container_width=True)
            df_4["WEBSITE"] = mo_website
            df_4["ADDRESS"] = mo_addre
            df_4["PINCODE"] = mo_pincode

        # Display modified data preview
        st.dataframe(df_4)

        # Button to confirm modification
        if st.button("Modify", use_container_width=True):
            with st.spinner("Updating database..."):
                # Delete the old record (parameterized query to prevent SQL injection)
                delete_query = "DELETE FROM bizcard_details WHERE NAME = %s"
                cursor.execute(delete_query, (selected_name,))
                mydb.commit()

                # Insert the modified data
                insert_query = '''INSERT INTO bizcard_details(
                                    NAME, DESIGNATION, COMPANY_NAME, CONTACT, EMAIL, WEBSITE, ADDRESS, PINCODE, IMAGE
                                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''

                datas = df_4.iloc[0].tolist()
                cursor.execute(insert_query, datas)
                mydb.commit()

                st.success("Modified successfully!")

    # Close the database connection at the end of the function
    cursor.close()
    mydb.close()
