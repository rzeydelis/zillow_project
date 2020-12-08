#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 10:49:02 2019

@author: Bobby
"""

# importing flask module fro
from flask import Flask, render_template,request
import delete

# initializing a variable of Flask
app = Flask(__name__)


# home page where you can click where you want to go on the web page
@app.route('/')
def home():
    return render_template('home.html')

# fill out the address and zip code to return information
@app.route('/form')
def index():
    return render_template('form.html')

@app.route('/output',  methods=['POST'])
def success():
    if request.method == 'POST':
        #email = request.form['email']
        #return render_template('success.html', email=email)
        address = request.form['address']
        zipcode = request.form['zipcode']
        zestimate, rent_zestimate, home_size, num_of_bedrooms, num_of_bathrooms, property_size, year_built = zillow_address_pull.zillow_info(address, zipcode)
        
        
        return render_template('success.html',
                               zestimate = zestimate,
                               rent_zestimate = rent_zestimate,
                               home_size = home_size,
                               num_of_bedrooms = num_of_bedrooms,
                               num_of_bathrooms = num_of_bathrooms,
                               property_size = property_size,
                               year_built = year_built).format()
    else:
        pass
 
@app.route('/random_output', methods=['POST'])
def random_output():
    if request.method == 'POST':
        rent_zestimate, full_address, home_size, last_sold_price, last_sold_date = zillow_address_pull.random_address()
        
        return render_template('random_success.html',
                               rent_zestimate = rent_zestimate,
                               full_address = full_address,
                               home_size = home_size,
                               last_sold_price = last_sold_price,
                               last_sold_date = last_sold_date).format()

if __name__ == "__main__":
    app.run()
