# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 08:22:49 2023

@author: Dell
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import json

app = FastAPI()

origins = ["*"]

app.add_middleware(CORSMiddleware,
                   allow_origins = origins,
                   allow_credentials = True,
                   allow_methods = ["*"],
                   allow_headers = ["*"],)

class model_input(BaseModel):
    Pregnancies : int
    Glucose : int 
    BloodPressure : int 
    SkinThickness : int 
    Insulin : int 
    BMI : float
    DiabetesPedigreeFunction : float 
    Age : int
    


# loading the mdel 

diabetes_model = pickle.load(open("trained_model.sav","rb"))


# creating a api

@app.post("/diabetes_prediction")

def diabetes_pred(input_parameters : model_input):
    
    # input data is posted to the api in the form of json
    input_data =input_parameters.json() 
    
    # convert the json in to dictionary
    input_dictionary = json.loads(input_data)
    
   
    # extracting the information (featues) from the dictionary
    
    preg = input_dictionary['Pregnancies']
    glu = input_dictionary['Glucose']
    bp = input_dictionary['BloodPressure']
    skin = input_dictionary['SkinThickness']
    insulin = input_dictionary['Insulin']
    bmi = input_dictionary['BMI']
    dpf = input_dictionary['DiabetesPedigreeFunction']
    age = input_dictionary['Age']
    
    # converting the dictionary into list or tuple
    input_list = [preg,glu,bp,skin,insulin,bmi,dpf,age]
    
    # call the predicting method
    prediction = diabetes_model.predict([input_list])
    # insted of doning reshape put input list inside a list
    
    if prediction[0] == 0:
        return "person has not diabetes"
    else:
        return "person has diabetes"
    
    
    