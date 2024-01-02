
###################################### libraries ################################################################

from datetime import datetime
import streamlit as st



from datetime import datetime
import numpy as np
import pandas as pd


from PIL import Image
import requests


import odf
###############################################################################################################





########################################## Page features#######################################################
st.set_page_config(
    page_title="Ödenek Sorgulama",
    page_icon="bayrak.png",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={

        'About': "Made by Fuat YAHŞİ"
    }
)
################################################################################################################

import streamlit as st





img = Image.open("AFAD_page-0001.jpg")

st.sidebar.title('Ödenek Sorgulama')


html_temp = """
<div style="background-color:red;padding:3px">
<h4 style="color:white;text-align:center;">Acil Yardım Ödenek Sorgulama </h4>
</div>"""

st.markdown(html_temp, unsafe_allow_html=True)
st.markdown(" ")
st.image(img, caption="BARINMA VE YAPIM İŞLERİ GENEL MÜDÜRLÜĞÜ",clamp=False)






############################################## Data Source #################################################
files = ["/Fatura Takibi.ods","/Ödenek Talepleri.ods"]

url_head = "https://dosya.afad.gov.tr/remote.php/webdav"


fatura_takibi =  url_head+files[0]
odenek_talepleri = url_head+files[1]

############################################################################################################





################################# Kullanıcı adı ve parola doğrulama ########################################



with st.sidebar:
    st.markdown("#### Kullanıcı Bilgileri")
    with st.form("my_form", border=True):
        
        username = st.text_input("Kullanıcı Adı", placeholder="örnek(fuat.yahsi)",key = 1)
        password = st.text_input("Kullanıcı Şifresi", placeholder="*********", type="password",key=2)
        login_button = st.form_submit_button("Login")
   







############################### Data Streaming ###########################################################

url = "https://dosya.afad.gov.tr/remote.php/webdav/Ödenek Talepleri.ods"
file_name = 'Ödenek Talepleri.ods'

if username and password:
    with open(file_name, 'wb') as out_file:
        content = requests.get(url=odenek_talepleri, stream=True,auth=(username,password)).content
        out_file.write(content)


    df = pd.read_excel(file_name,engine="odf",sheet_name="18 AFET İLİ")
#########################################################################################################




    df["EVRAK SAYISI"] = df["EVRAK TARİHİ/SAYISI"].apply(lambda x : (x[x.find("/")+1:]).strip() if (type(x) == type("fuat") and x.__contains__("/")) else x).apply(lambda x : (x[x.find("-")+1:]).strip() if (type(x) == type("fuat") and x.__contains__("-")) else x)


        # In[325]:


    df["EVRAK TARİHİ"] = df["EVRAK TARİHİ/SAYISI"].apply(lambda x : (x[:x.find("/"):]).strip() if (type(x) == type("fuat") and x.__contains__("/")) else x).apply(lambda x : (x[:x.find("-"):]).strip() if (type(x) == type("fuat") and x.__contains__("-")) else x)


        # In[326]:


    df["EVRAK TARİHİ"] = df["EVRAK TARİHİ"].apply(lambda x : x.replace("..",".") if type(x) != type(3.1) else x)





    df.drop("EVRAK TARİHİ/SAYISI",axis = 1, inplace=True)

    df["EVRAK TARİHİ"] = df[df.columns[-1]].apply(lambda x : x.split(".") if type(x) != type(3.1) else x).apply(lambda x : datetime(int(x[2]),int(x[1]),int(x[0])) if type(x) != type(3.1) else x).dt.strftime("%d.%m.%Y")


    evrak_tarihi =""

    selection  = st.sidebar.radio(label = "Evrağın hangi özelliğiyle sorgu yapmak istiyorsunuz ?",options = ["EVRAK SAYISI","EVRAK TARİHİ"])
    if selection == "EVRAK SAYISI":
        evrak_sayı = st.sidebar.text_input(label = "Evrak sayısını giriniz",key = 4)
        querry = st.sidebar.button("SORGULA")
        if querry:
                st.table(df[df["EVRAK SAYISI"] == evrak_sayı].set_index("EVRAK SAYISI").reset_index().T)
    elif selection == "EVRAK TARİHİ" :
        evrak_tarihi = st.sidebar.date_input(label = "Evrak tarihini giriniz",value=None,format="DD.MM.YYYY",key = 5)
        querry = st.sidebar.button("SORGULA")
        if querry: 
            st.table(df[df["EVRAK TARİHİ"] == evrak_tarihi.strftime("%d.%m.%Y")].set_index("EVRAK TARİHİ").reset_index().T)

        












