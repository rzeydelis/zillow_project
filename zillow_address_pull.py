# This python file serves 2 purposes:
# 1. Support the random address function.
# 2. Pulling housing data from the Zillow API

import pandas as pd
from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults


# Pull a random address from the housing_data.csv file
def random_address():
    # import master dataset
    housing_data = pd.read_excel('housing_data.xlsx')

    # pick a random house from the dataset
    random_house_data = housing_data.sample()

    # assign the values to the variables
    rent_zestimate = random_house_data.iloc[0]['Rent_Zestimate']
    full_address = random_house_data.iloc[0]['full_Address']
    home_size = random_house_data.iloc[0]['home_size']
    last_sold_price = random_house_data.iloc[0]['last_sold_price']
    last_sold_date = random_house_data.iloc[0]['last_sold_date']

    return rent_zestimate, full_address, home_size, last_sold_price, last_sold_date


# Pull housing data from a user uploaded list of addresses. First it will check if the data already exists and if it does
# then it will take the data from the database. If the data doesn't exist in the database, then it will pull it from
# zillow.

def zillow_info_mass_upload():
    # upload dataset
    housing_df = pd.read_excel('/home/bobby/zillow_project/housing_data.xlsx')
    # upload addresses
    addresses_df = pd.read_excel('/home/bobby/zillow_project/single_test_address.xlsx')

    # make sure all addresses are capital for ease of mapping
    addresses_df['address'] = addresses_df['address'].str.upper()

    # merge the tables and see which ones are not in the table and which ones are
    merged_df = addresses_df.merge(housing_df, on=['address', 'zipcode'], how='outer', indicator='exists')

    # dataframe with info from internal database
    matched_addresses = merged_df[merged_df['exists'] == 'both']
    matched_addresses['full_address'] = matched_addresses['address'].astype(str) + matched_addresses['zipcode'].astype(
        str)

    # dataframe that needs to be pushed through Zillow's API
    not_matched_addresses = merged_df[merged_df['exists'] == 'left_only']


    if len(not_matched_addresses) > 0:
        # run the non_matched addresses through Zillow's API
        for i in range(len(not_matched_addresses)):

            try:
                address = str(not_matched_addresses['address'][i])
                zipcode = str(not_matched_addresses['zipcode'][i])
                full_address = str(not_matched_addresses['address'][i]) + " " + str(not_matched_addresses['zipcode'][i])

                # connect to Zillow API
                zillow_api = ZillowWrapper('X1-ZWz17hux7ivthn_9myga')
                deep_search_response = zillow_api.get_deep_search_results(address, zipcode)
                result = GetDeepSearchResults(deep_search_response)

                # pull all dimensions and measures from zillow api
                zestimate = result.zestimate_amount
                rent_zestimate = result.rentzestimate_amount
                zest_last_upd = result.zestimate_last_updated
                zest_value_chg = result.zestimate_value_change
                zestimate_percentile = result.zestimate_percentile
                home_type = result.home_type
                longitude = result.longitude
                latitude = result.latitude
                year_built = result.year_built
                property_size = result.property_size
                home_size = result.home_size
                num_of_bathrooms = result.bathrooms
                num_of_bedrooms = result.bedrooms
                tax_year = result.tax_year
                tax_value = result.tax_value
                last_sold_date = result.last_sold_date
                last_sold_price = result.last_sold_price

                # assign values
                values = [address, zipcode, zestimate, rent_zestimate, zest_last_upd, zest_value_chg,
                          zestimate_percentile, home_type, longitude, latitude, year_built, property_size,
                          home_size, num_of_bathrooms, num_of_bedrooms, tax_year, tax_value, last_sold_date,
                          last_sold_price, full_address]

                # transform dataset into a series to be able to append it to the dataset.
                a_series = pd.Series(values, index=housing_df.columns)
                housing_df = housing_df.append(a_series, ignore_index=True)
                print('GREAT SUCCESS')



            except:
                pass

        # concat the matched_addresses
        result = pd.concat([housing_df, matched_addresses], ignore_index=True, sort=False)
        result.rename(columns={"full_address_x": "full_address"})
        # result_new = result.drop(columns=['full_address_x', 'full_address_y', 'exists'], axis=1)
        result_new = result.drop(columns=['exists'], axis=1)
        result_new.to_excel('/home/bobby/zillow_project/housing_df.xlsx', index=False)

        zestimate = result['zestimate']
        return zestimate

    else:
        print('something')


# Pull housing data from the Zillow API for the single address input function on flask app
def zillow_info(address, zipcode):
    # import address list housing data, and neighborhood mapping
    housing_data = pd.read_csv('housing_data.xlsx')

    # for loop to push every address through Zillow. This will be useful when I only want to pull in data for houses that
    # not in my excel sheet.

    # for i,x in zip(address, zipcode):
    # log into Zillow deep search
    i = address
    x = zipcode
    full_address = str(i) + ' ' + str(x)
    #     if full_address in housing_data['full_Address']:
    #        pass
    #     else:
    #        continue

    # connect to Zillow API
    zillow_data = ZillowWrapper('Enter Your API Key')
    deep_search_response = zillow_data.get_deep_search_results(i, x)
    result = GetDeepSearchResults(deep_search_response)

    # pull all dimensions and measures from zillow api
    zestimate = result.zestimate_amount
    rent_zestimate = result.rentzestimate_amount
    zest_last_upd = result.zestimate_last_updated
    zest_value_chg = result.zestimate_value_change
    zestimate_valuation_range_high = result.zestimate_valuation_range_high
    zestimate_valuation_range_low = result.zestimate_valuationRange_low
    zestimate_percentile = result.zestimate_percentile
    home_type = result.home_type
    longitude = result.longitude
    latitude = result.latitude
    year_built = result.year_built
    property_size = result.property_size
    home_size = result.home_size
    num_of_bathrooms = result.bathrooms
    num_of_bedrooms = result.bedrooms
    tax_year = result.tax_year
    tax_value = result.tax_value
    last_sold_date = result.last_sold_date
    last_sold_price = result.last_sold_price

    # create variables for all the fields
    values = [[i, x, full_address, zestimate, rent_zestimate, property_size, home_size, zest_last_upd, zest_value_chg,
               zestimate_valuation_range_high, zestimate_valuation_range_low, zestimate_percentile,
               home_type, longitude, latitude, year_built, property_size, home_size, num_of_bathrooms,
               num_of_bedrooms, tax_year, tax_value, last_sold_date, last_sold_price]]

    # create the dataframe that will update the excel sheet. this will be a future update a database of housing data that I want to keep
    # to save the amount of times I call the Zillow API, since I only have a limited number of daily calls
    df = pd.DataFrame(values, columns=['address', 'zip_code', 'full_Address', 'Home_Value_Zestimate', 'Rent_Zestimate',
                                       'Property_Size_sqft', 'Home_Size_sqft', 'Zestimate_Last_Updated',
                                       'zest_value_chg', 'Zestimate_Valuation_Range_High',
                                       'zestimate_valuation_range_low', 'zestimate_percentile',
                                       'home_type', 'longitude', 'latitude', 'year_built',
                                       'property_size', 'home_size', 'num_of_bathrooms',
                                       'num_of_bedrooms', 'tax_year', 'tax_value', 'last_sold_date',
                                       'last_sold_price'])
    housing_data = housing_data.append(df)

    # add neighborhoods to df
    housing_data = pd.merge(
        housing_data
        # , neighborhood_mapping
        , left_on='zip_code'
        , right_on='zip_code'
        , how='left'
    )

    # return the values for the Flask App
    return zestimate, rent_zestimate, home_size, num_of_bedrooms, num_of_bathrooms, property_size, year_built, last_sold_date, last_sold_price
