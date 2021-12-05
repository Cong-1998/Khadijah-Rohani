# import libraries
import streamlit as st
from streamlit_player import st_player
import re
import pandas as pd
from PIL import Image
from readability import Readability

# table of content
class Toc:
    def __init__(self):
        self._items = []
        self._placeholder = None
    
    def title(self, text):
        self._markdown(text, "h1")

    def header(self, text):
        self._markdown(text, "h2", " " * 2)

    def subheader(self, text):
        self._markdown(text, "h3", " " * 4)

    def placeholder(self, sidebar=True):
        self._placeholder = st.sidebar.empty() if sidebar else st.empty()

    def generate(self):
        if self._placeholder:
            self._placeholder.markdown("\n".join(self._items), unsafe_allow_html=True)
    
    def _markdown(self, text, level, space=""):
        key = "-".join(text.split()).lower()
        st.markdown(f"<{level} id='{key}'>{text}</{level}>", unsafe_allow_html=True)
        self._items.append(f"{space}* <a href='#{key}'>{text}</a>")

def cleaning(text):
    new_string = text.replace("\\n", "")
    new_string2 = new_string.replace("\\xa0", "")
    new_string3 = new_string2.replace("\\'", "")
    new_string4 = re.sub(r'www\S+', '', new_string3)
    new_string5 = new_string4.replace("Â", "")
    new_string6 = new_string5.replace("\\x9d", "")
    new_string7 = new_string6.replace("â€", "")
    new_string8 = new_string7.replace("â€œ", "")
    new_string9 = new_string8.replace("œ", "")
    new_string11 = re.sub(' +', ' ', new_string9).strip()
    new_string12 = new_string11.replace(". . .", "")
    new_string13 = re.sub(r'http\S+', '', new_string12)
    new_string14 = re.sub(r'[-+]?\d*\.\d+|\d+', '', new_string13)
    return new_string14

# hide menu bar
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

# set up layout
padding = 1
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)

# set up title
st.markdown("<h1 style='text-align: center;'>Ujian Kebolehbacaan Khadijah Rohani</h1>", unsafe_allow_html=True)
st.write('\n')

# set up sidebar
st.sidebar.header("Kandungan")
toc = Toc()
toc.placeholder()

# calculate single text
toc.header('Kalkulator Khadijah Rohani')
st.write("Apakah kebolehbacaan [Khadijah Rohani](#tahap-gred-khadijah-rohani)❓")

# input text
TextBox = st.text_area('Masukkan teks untuk menyemak kebolehbacaan', height=200)

# run the test
test = st.button("Kira Kebolehbacaan")

new_content = cleaning(TextBox)

if test:
    my_expander = st.expander(label='Teks yang Dibersihkan')
    with my_expander:
        st.write(new_content)
    r = Readability(new_content)
    kr = r.khadijah_rohani()
    statis = r.statistics()
    word = list(statis.items())[0][1]
    sentence = list(statis.items())[1][1]
    syllable = list(statis.items())[2][1]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Skor Khadijah Rohani", round(kr.score, 1))
    col2.metric("Jumlah Perkataan", word)
    col3.metric("Jumlah Ayat", sentence)
    col4.metric("Jumlah Suku Kata", syllable)
st.write('\n')
st.write('\n')

# upload file
toc.header("Muat naik fail csv")
st.write("Sila muat naik fail csv dan pastikan data anda berada dalam lajur pertama. Ia akan mengira skor KR dalam satu pas.")
file_upload = st.file_uploader("", type=["csv"])
if file_upload is not None:
    data = pd.read_csv(file_upload, encoding='unicode_escape')
    st.write(data)
    name = file_upload.name.replace('.csv', '')
    name = name+"_skor_kr.csv"

# run the program
result = st.button("Jalankan")
if result:
    st.write("Sabar, perlu tunggu 1 hingga 2 minit :smile:")
    df = data.iloc[:, 0]
    df.apply(str)
    list_data = df.tolist()

    # clean data
    new_content = []
    for string in list_data:
        new_content.append(cleaning(string))

    # Khadijah Rohani Score
    list_kr_score = []
    for i in range(len(new_content)):
        r = Readability(new_content[i])
        kr = r.khadijah_rohani()
        list_kr_score.append(round(kr.score, 1))

    # create new dataframe
    final_df = pd.DataFrame(
        {'Data': list_data,
         'Khadijah Rohani Score': list_kr_score,
        })

    # download labelled file
    st.write("Bawah ini ialah fail Skor Khadijah Rohani, klik butang untuk memuat turun.")
    csv = final_df.to_csv(index=False)
    st.download_button(
        label="Muat turun data sebagai CSV",
        data=csv,
        file_name=name,
        mime='text/csv',
    )
st.write('\n')

toc.header("Tahap Gred Khadijah Rohani")
st.write("Kebolehbacaan Khadijah Rohani ialah pengukuran kebolehbacaan sesuatu bahan untuk membolehkan para pendidik, ibu bapa dan para penulis cuba menyesuaikan kebolehan membaca murid-murid dengan bahan yang mereka baca.")
st.write("Dalam kalkulator ini,")
st.write(
    """    
- Kami mengalih keluar nombor termasuk perpuluhan.
- Kami mengalih keluar pautan url.
    """)
st.write("Had formula Khadijah Rohani,")
st.write(
    """    
- Teks perlu dalam 300 perkataan.
- Tetapi kami memperbaiki had ini dengan [formula ini](#kalkulator-khadijah-rohani-yang-diperbaikan).
    """)
image = Image.open('formula.jpg')
st.image(image, caption='Formula Tahap Gred Khadijah Rohani')
st.write("\n")
image2 = Image.open('table.jpg')
st.image(image2, caption='Jadual Tahap Gred Khadijah Rohani')
st.write("\n")

toc.header("Tukar kepada fail CSV")
st.write('Video ini akan mengajar anda cara menukar fail excel kepada fail csv.')
# Embed a youtube video
st_player("https://www.youtube.com/watch?v=IBbJzzj5r90")
st.write('\n')

# new formula
toc.header('Kalkulator Khadijah Rohani yang Diperbaikan')
st.write("Formula ini ditambank baik oleh kami dengan menambah pembolehuba malar yang baru.")
image = Image.open('formula2.jpg')
st.image(image, caption='Formula Tahap Gred Khadijah Rohani')
st.write("\n")
TextBox2 = st.text_area('Masukkan teks', height=200)
test2 = st.button("Kira")
new_content2 = cleaning(TextBox2)
if test2:
    my_expander = st.expander(label='Teks yang Dibersihkan')
    with my_expander:
        st.write(new_content2)
    r = Readability(new_content2)
    statis = r.statistics()
    word = list(statis.items())[0][1]
    sentence = list(statis.items())[1][1]
    syllable = list(statis.items())[2][1]

    score = (0.3793*word/sentence)+(0.0207*syllable*300/word)-13.988

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Skor Khadijah Rohani", round(score, 1))
    col2.metric("Jumlah Perkataan", word)
    col3.metric("Jumlah Ayat", sentence)
    col4.metric("Jumlah Suku Kata", syllable)
st.write('\n')

toc.generate()
