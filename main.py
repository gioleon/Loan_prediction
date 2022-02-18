import requests
import pickle
import pandas as pd
import streamlit as st
from fastapi import FastAPI

# create app
app = FastAPI()

# Title
st.markdown("# Welcome to the Loan Predictor")

# information about app
st.text('Please select here your personal information and i wil tell you if you are able \nto receive a loan.')

# Information
gender = st.selectbox('Gender', ('Select yout Gender', 'Male', 'Female'))
married = st.selectbox('Married', ('Are you married?', 'Yes', 'No'))
education = st.selectbox(
    'Education', ('Select your education', 'Graduate', 'Not Graduate'))
credit = st.selectbox(
    'Credit History', ('Do you have credit history?', 'Yes', 'No'))
credit = 1 if credit == 'Yes' else 0
property_area = st.selectbox(
    'Property Area', ('Select your property area', 'Urban', 'Rural', 'Semiurban'))


# Create function to make predicts

@app.post('/make_pred')
def make_pred(gender: str, married: str, education: str, credit: int, property_area: str):

    # Load files
    model = pd.read_pickle('pickles/model.pkl')
    encoder = pd.read_pickle('pickles/encoder.pkl')

    # df
    df = pd.DataFrame([[gender, married, education, credit, property_area]],
                      columns=['Gender', 'Married', 'Education', 'Credit_History', 'Property_Area'])

    # OneHotEncoding
    encoded_features = pd.DataFrame(
        encoder.transform(df[['Gender', 'Married', 'Education', 'Property_Area']]).toarray(), columns=encoder.get_feature_names_out(['Gender',
                                                                                                                                     'Married',
                                                                                                                                     'Education',
                                                                                                                                     'Property_Area']))

    # Build final df

    df.drop(['Gender', 'Education', 'Married',
             'Property_Area'], axis=1, inplace=True)

    df2 = pd.concat([encoded_features, df], axis=1)

    pred = model.predict(df2)

    return pred[0]

# Button to make predicts


if gender == 'Select yout Gender' or married == 'Are you married?' or education == 'Are you graduated?' or credit == 'Do you have credit history' or property_area == 'Property Area':
    if st.button('Analyze'):
        st.error('PLEASE, FILL IN ALL CELLS.')
else:
    if st.button('Analyze'):
        resultado = make_pred(gender, married, education,
                              credit, property_area)
        if resultado == 0:
            st.error(f'lOAN DENIED')
        else:
            st.success('GRANTED LOAN')
