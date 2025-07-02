

import streamlit as st

st.title('BMI Calculator')

weight = st.number_input('Enter Weight ')
height = st.number_input('Enter Height ')

result = st.button('Calculate')

if (result):
    result = round(weight / height ** 2 * 10000)
    st.header(f'Your BMI Is: {result}')


