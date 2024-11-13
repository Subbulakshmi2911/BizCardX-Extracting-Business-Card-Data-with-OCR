import streamlit as st

from streamlit_option_menu import option_menu
import os
# from dotenv import load_dotenv
# load_dotenv()


import home,upload,modify,delete
st.set_page_config(
        page_title="Bizcard",
)


class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):

        self.apps.append({
            "title": title,
            "function": func
        })

    def run():
        

        with st.sidebar:        
            app = option_menu(
                menu_title='Menu',
                options=['Home','Upload','Modify','Delete'],
                icons=["house", "cloud-upload","pencil","trash"],
                menu_icon='cast',
                #default_index=0,
                styles={
                    "container": {"height": '400px',"background-color":'block'},
        "icon": {"color": "white", "font-size": "23px"}, 
        "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "grey"},
        "nav-link-selected": {"background-color": "#02ab21"},}
                
                )

        if app == "Home":
            home.app()
        
        if app == "Upload":
            upload.app()    
        if app == "Modify":
            modify.app() 
        if app == "Delete":
            delete.app()  
    
        
        st.sidebar.markdown(
            """
            <style>
            [data-testid="stSidebar"] {
                background-color: blank;
                
            }
            .icon-bar {
                display: flex;
                justify-content: space-around;
                margin-top: 20px;
                padding: 10px;
            }
            .icon-bar a {
                
                color: #red;
                
                font-size: 30px;
            }
            .icon-bar a:hover {
                color: #1a73e8;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Add icon bar
        st.sidebar.markdown(
            """
            <div class="icon-bar">
                <a href="https://github.com" target="_blank" title="GitHub"><i class="fab fa-github"></i></a>
                <a href="https://linkedin.com" target="_blank" title="LinkedIn"><i class="fab fa-linkedin"></i></a>
              
                
            </div>
            """,
            unsafe_allow_html=True
        )

    
        st.markdown(
        """<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">""",
        unsafe_allow_html=True
        )    
        
             
          
             
    run()            
         