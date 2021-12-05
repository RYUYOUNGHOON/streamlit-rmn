# from IPython.display import Image
import cv2
from streamlit import uploaded_file_manager
from rmn import RMN
#streamlit library
import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import matplotlib.pyplot as plt
from ast import literal_eval


#제목   
st.title('Emotion Control')
hour_to_filter = st.slider('Person Number', 1, 3, 1)
checkbox_btn5 = st.checkbox("Image Upload")
if checkbox_btn5:
    #이미지 업로더
    uploaded_file = st.file_uploader("Choose Images",type=["jpg","jpeg","png"],accept_multiple_files= True)
    
checkbox_btn = st.checkbox("Show your Data")
if checkbox_btn: 
    #캡쳐 이미지 출력
    from PIL import Image   
    image = Image.open(uploaded_file[0])
    image2 = Image.open(uploaded_file[1])
    image3 = Image.open(uploaded_file[2])
    st.image(image)
    st.image(image2)
    st.image(image3)

    # Image('image.jpg', width=400)

    m = RMN()
    n = RMN()
    k = RMN()
    
    
    image = cv2.imread('1.jpg')
    image2 = cv2.imread('2.jpg')
    image3 = cv2.imread('3.jpg')

    results = m.detect_emotion_for_single_frame(image)
    results2 = n.detect_emotion_for_single_frame(image2)
    results3 = k.detect_emotion_for_single_frame(image3)
    
    personList = []
    person1 = results[0]
    person2 = results2[0]
    person3 = results3[0]

    print(personList)
    personList.append(person1)
    personList.append(person2)
    personList.append(person3)
        


    neutralCount = 0
    angryCount = 0
    disgustCount = 0
    fearCount = 0
    happyCount = 0
    sadCount = 0
    surpriseCount = 0
    understandCount = 0
    misunderstandCount = 0

    for person in personList:
        if person['emo_label'] == "neutral":
            neutralCount += 1
            understandCount += 1
        elif person['emo_label'] == "angry":
            angryCount += 1
            misunderstandCount += 1
        elif person['emo_label'] == "disgust":
            disgustCount += 1
            misunderstandCount += 1
        elif person['emo_label'] == "fear":
            fearCount += 1
            misunderstandCount += 1
        elif person['emo_label'] == "happy":
            happyCount += 1
            understandCount += 1
        elif person['emo_label'] == "sad":
            sadCount += 1
            misunderstandCount += 1
        elif person['emo_label'] == "surprise":
            surpriseCount += 1
            understandCount += 1
        else: break

    #감정
    data1 = pd.DataFrame({
    'emotion': ['neutral', 'angry', 'disgust', 'fear', 'happy', 'sad', 'surprise'],
    'amount': [neutralCount, angryCount, disgustCount, fearCount, happyCount, sadCount, surpriseCount],
    })
    #멤버별 
    data2 = pd.DataFrame({
    'person': ['1', '2','3'],
    'emotion': [person1['emo_label'],person2['emo_label'],person3['emo_label']]
    })

    #이해도
    data3 = pd.DataFrame({
        'comprehension':['Understanding','Misunderstanding'],'amount':[understandCount,misunderstandCount]
    })
    checkbox_btn2 = st.checkbox("View emotion")
    if checkbox_btn2:
        st.write(data1) 
        st.write(alt.Chart(data1,width=7,height=6).mark_bar().encode(
        x=alt.X('emotion', sort=None),
        y='amount',
        ))
    checkbox_btn3 = st.checkbox("View member")
    if checkbox_btn3:
        st.write(data2) 
        st.write(alt.Chart(data2,width=7,height=2).mark_bar().encode(
        x=alt.X('person', sort=None),
        y='emotion',
        ))
    checkbox_btn4 = st.checkbox("View comprehension")
    if checkbox_btn4:    
        st.write(data3) 
        st.write(alt.Chart(data3,width=2,height=6).mark_bar().encode(
        x=alt.X('comprehension', sort=None),
        y='amount',
        ))