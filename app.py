#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 10:49:02 2019

@author: Bobby
"""

# importing flask module fro
from flask import Flask, flash, request, redirect, render_template
import zillow_address_pull
import os
import urllib.request
from werkzeug.utils import secure_filename
import pandas as pd


# initializing a variable of Flask
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = '/home/bobby/zillow_project/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# home page
@app.route('/')
def home():
    return render_template('home.html')

# fill out the address and zip code to return information
@app.route('/form')
def index():
    return render_template('form.html')

# output after you fill out /form
@app.route('/output',  methods=['POST'])
def success():
    if request.method == 'POST':
        #email = request.form['email']
        #return render_template('success.html', email=email)

        address = request.form['address']
        zipcode = request.form['zipcode']

        zestimate, rent_zestimate, home_size, num_of_bedrooms, num_of_bathrooms, property_size, year_built, last_sold_price, \
        last_sold_date = zillow_address_pull.zillow_info(address, zipcode)
        
        
        return render_template('success.html',
                               zestimate = zestimate,
                               rent_zestimate = rent_zestimate,
                               home_size = home_size,
                               num_of_bedrooms = num_of_bedrooms,
                               num_of_bathrooms = num_of_bathrooms,
                               property_size = property_size,
                               year_built = year_built,
                               last_sold_price = last_sold_price,
                               last_sold_date = last_sold_date).format()
    else:
        pass

 # searching a random house
@app.route('/random_output', methods=['POST'])
def random_output():
    if request.method == 'POST':
        zestimate, rent_zestimate, full_address, home_size, last_sold_price, last_sold_date = zillow_address_pull.random_address()
        
        return render_template('random_success.html',
                               zestimate = zestimate,
                               rent_zestimate = rent_zestimate,
                               full_address = full_address,
                               home_size = home_size,
                               last_sold_price = last_sold_price,
                               last_sold_date = last_sold_date).format()

# excel upload
@app.route("/upload", methods = ['GET', 'POST'])
def upload():
  #user_file is the name value in input element
  if request.method == 'POST':
    f = request.files['file']
    f.save(secure_filename(f.filename))

    df = pd.read_excel('single_test_address.xlsx')
    address = df['address']
    zipcode = df['zipcode']

    zestimate = zillow_address_pull.zillow_info_mass_upload()

    return render_template('upload.html',
                           zestimate = zestimate).format()

# run app
if __name__ == "__main__":
    app.run(debug=True)
