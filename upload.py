import streamlit as st
import easyocr
from PIL import Image
import pandas as pd
import numpy as np
import re
import io
import mysql.connector 
from streamlit_option_menu import option_menu

def image_to_text(path):

  input_img= Image.open(path)

  #converting image to array formet
  image_arr= np.array(input_img)

  reader= easyocr.Reader(['en'])
  text= reader.readtext(image_arr, detail= 0)

  return text, input_img

def extracted_text(texts):
    extrd_dict = {
        "NAME": [], "DESIGNATION": [], "COMPANY_NAME": [], "CONTACT": [],
        "EMAIL": [], "WEBSITE": [], "ADDRESS": [], "PINCODE": []
    }

    # Assume the first two items are always name and designation
    extrd_dict["NAME"].append(texts[0])
    extrd_dict["DESIGNATION"].append(texts[1])

    for i in range(2, len(texts)):
        text = texts[i].strip()

        if text.startswith("+") or (text.replace("-", "").isdigit() and '-' in text):
            extrd_dict["CONTACT"].append(text)

        elif "@" in text and ".com" in text:
            extrd_dict["EMAIL"].append(text)

        elif "www" in text.lower() or text.lower().startswith("www") or "com" in text.lower():
            # Capture full domain if it’s split over two entries
            if extrd_dict["WEBSITE"]:
                extrd_dict["WEBSITE"][0] += text.lower()
            else:
                extrd_dict["WEBSITE"].append(text.lower())

        elif re.search(r'\b\d{6}\b', text):  # Detects 6-digit pincode
            extrd_dict["PINCODE"].append(re.search(r'\b\d{6}\b', text).group())

        elif re.match(r'^[A-Za-z]', text):
            extrd_dict["COMPANY_NAME"].append(text)

        else:
            clean_text = re.sub(r'[;,:]', '', text)  # Clean unwanted characters
            extrd_dict["ADDRESS"].append(clean_text)

    # Concatenate each list into a single string or mark as "NA" if empty
    for key, value in extrd_dict.items():
        extrd_dict[key] = [" ".join(value) if value else "NA"]

    return extrd_dict

def upload():
    st.title(":red[Extracting Business Card Data]")

    # File uploader to upload image files (png, jpg, jpeg)
    img = st.file_uploader("Upload the Image", type=["png", "jpg", "jpeg"])

    if img is not None:
        # Display the uploaded image
        st.image(img, width=300)

        # Processing image to extract text
        with st.spinner("Extracting text from image..."):
            text_image, input_img = image_to_text(img)

            # Extracting text
            text_dict = extracted_text(text_image)

            if text_dict:
                st.success("Text is extracted successfully!")

                # Convert the extracted text into a DataFrame
                df = pd.DataFrame([text_dict])
                

                # Converting image to bytes
                image_bytes = io.BytesIO()
                input_img.save(image_bytes, format="PNG")
                image_data = image_bytes.getvalue()

                # Create a new DataFrame for the image data
                image_data_dict = {"IMAGE": [image_data]}
                df_image = pd.DataFrame(image_data_dict)

                # Concatenate the text DataFrame and image DataFrame
                concat_df = pd.concat([df, df_image], axis=1)

                # Display the final concatenated DataFrame
                st.dataframe(concat_df)

                # Button to save data to the database
                if st.button("Save to Database"):
                    insert_bizcard_data(concat_df)
                    
            else:
                st.error("No text extracted from the image.")

    else:
        st.info("Please upload an image to extract data.")


def insert_bizcard_data(concat_df):
    try:
        # Establishing connection to the MySQL database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="Bizcard"
        )

        cursor = mydb.cursor()

        # Table creation
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS bizcard_details(
                NAME VARCHAR(225),
                DESIGNATION VARCHAR(225),
                COMPANY_NAME VARCHAR(225),
                CONTACT VARCHAR (225),
                EMAIL VARCHAR (225),
                WEBSITE TEXT,
                ADDRESS TEXT,
                PINCODE VARCHAR(225),
                IMAGE MEDIUMBLOB  -- BLOB type for binary image data
            )
        '''
        cursor.execute(create_table_query)
        mydb.commit()

        # Extract row data as a tuple and confirm types
        row_data = []
        for item in concat_df.iloc[0]:
            if isinstance(item, (list, tuple)):  # Flatten any list or tuple
                item = item[0] if item else None
            elif isinstance(item, pd.Series):  # Flatten pandas series
                item = item.iloc[0] if not item.empty else None
            row_data.append(item)

        # Ensure image data is in bytes format for BLOB storage
        row_data = tuple(row_data)  # Convert list to tuple for MySQL insertion

        # Insert query with %s placeholders
        insert_query = '''INSERT INTO bizcard_details(
                            NAME, DESIGNATION, COMPANY_NAME, CONTACT, EMAIL, WEBSITE, ADDRESS, PINCODE, IMAGE
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''

        # Execute the insert query
        cursor.execute(insert_query, row_data)
        mydb.commit()
        st.success("Data has been successfully saved to the database!")

    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
    finally:
        # Close the cursor and connection
        cursor.close()
        mydb.close()


def app():
    
    upload()
    


    

