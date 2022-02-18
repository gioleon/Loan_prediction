import requests
import pickle
import pandas as pd
import streamlit as st
from fastapi import FastAPI

app = FastAPI()


# @app.post('/pred')
# def index(nombre: str):
#     return nombre

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

    return print(f'El resultado es: {pred[0]}')


# gender = 'Male'
# married = 'Yes'
# education = 'Graduate'
# credit = 1
# property_area = 'Urban'

# url = f'http://127.0.0.1:8000/make_pred?gender={gender}&married={married}&education={education}&credit={credit}&property_area={property_area}'
# url = url.replace(' ', '20')

# resp = requests.post(url)

# print(resp.content)
