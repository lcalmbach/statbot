import openai
import streamlit as st
from streamlit_lottie import st_lottie
import requests

from statbot import StatBot
# Setting page title and header


__version__ = '0.0.2' 
__author__ = 'Lukas Calmbach'
__author_email__ = 'lcalmbach@gmail.com'
VERSION_DATE = '2023-04-17'
app_icon = "🤖"
app_name = 'St@tBot'
GIT_REPO = 'https://github.com/lcalmbach/statbot'
APP_INFO = f"""<div style="background-color:powderblue; padding: 10px;border-radius: 15px;">
    <small>App created by <a href="mailto:{__author_email__}">{__author__}</a><br>
    version: {__version__} ({VERSION_DATE})<br>
    <a href="{GIT_REPO}">git-repo</a>
    """
LOTTIE_URL = 'https://assets5.lottiefiles.com/packages/lf20_6e0qqtpa.json'

@st.cache_data()
def get_lottie():
    ok=True
    r=''
    try:
        r = requests.get(LOTTIE_URL).json()
    except:
        ok = False
    return r, ok

def show_impressum():
    cols = st.columns(2)
    with cols[0]:
        with st.expander("Impressum"):       
            st.markdown(APP_INFO, unsafe_allow_html=True)
            st.write("")

def main():
    st.set_page_config(
        page_title='St@tBot',
        page_icon=app_icon
    )
    lottie_search_names, ok = get_lottie()
    if ok:
        st_lottie(lottie_search_names, height=80, loop=20)
    else:
        pass
    st.markdown(f'<div style="text-align: center"><h3 style="color:blue">St@tBot</h3></div><br>', unsafe_allow_html=True)
    text = "Dein Freund und Helfer bei der Suche nach Statistik-Daten"
    st.markdown(f'<div style="text-align: center"><b>{text}</b></div><br>', unsafe_allow_html=True)
    if 'prompts' not in st.session_state:
        st.session_state['bot'] = StatBot()
    st.session_state['bot'].act()
    show_impressum()
    
if __name__ == '__main__':
    main()