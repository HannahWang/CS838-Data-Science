#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 20:02:45 2018

Common attributes:
    name,
    category_1,
    category_2,
    address,
    city,
    zipcode,
    phone,
    price, (number of dollar)
    rating,
    review_count,
    hours_sun_open,(format: HHMM 0 hour is 2400)
    hours_sun_close,
    hours_mon_open,
    hours_mon_close,
    hours_tue_open,
    hours_tue_close,
    ...

@author: kangyanghui
"""

import pandas as pd

def trip_phone(num):
    if(pd.isnull(num)):
        return None;
    num = int(num)
    if(num > 10**10 and num < 10**11):
        phone = num - 10**10
    else:
        if(num < 10**10):
            phone = None
        else:
            phone = num
    return phone

def get_hour(timestr):
    if(pd.isnull(timestr)):
        return None
    time = int(timestr.split(' ')[0].replace(':',''));
    ampm = timestr.split(' ')[1]
    if(ampm == 'PM'):
        hours = time + 1200;
    else:
        hours = time
    return hours

# process "yelp_small" data
yelp0 = pd.read_csv("yelp_full_small.csv");

# check duplicated rows
yelp0['duplicated'] = yelp0.duplicated(subset = ['id','location/address1'],keep='first')
yelp = yelp0[yelp0['duplicated'] == False]

# yelp = yelp[yelp['review_count'] > 300];
# yelp = yelp.dropna(subset = ['location/zip_code'])

# dict
pricedict_yelp = {'$':1, '$$':2, '$$$':3, '$$$$':4}

# clean yelp dataset
yelp_clean = pd.DataFrame();
yelp_clean['name'] = yelp['name'];
yelp_clean['category_1'] = yelp['categories/0/title'].str.lower()
yelp_clean['category_2'] = yelp['categories/1/title'].str.lower()
# yelp_clean['address'] = yelp['location/address1'].str.cat(yelp['location/address2'], sep = ' ', na_rep = '').str.cat(yelp['location/address3'], sep = ' ', na_rep='')
yelp_clean['address'] = yelp['location/address1']
yelp_clean['city'] = yelp['location/city']
yelp_clean['zipcode'] = yelp['location/zip_code'].str.extract('(\d\d\d\d\d)')
# yelp_clean['phone'] = yelp['phone'] - 10**10
yelp_clean['phone'] = yelp['display_phone'].str.replace('[+() -]','').apply(pd.to_numeric, errors = 'coerce')
yelp_clean['price'] = yelp['price'].map(pricedict_yelp)
yelp_clean['rating'] = yelp['rating']
yelp_clean['review_count'] = yelp['review_count']
yelp_clean['hours_sun_open'] = yelp['hours/0/open/0/start']
yelp_clean['hours_sun_close'] = yelp['hours/0/open/0/end']
yelp_clean['hours_mon_open'] = yelp['hours/0/open/1/start']
yelp_clean['hours_mon_close'] = yelp['hours/0/open/1/end']
yelp_clean['hours_tue_open'] = yelp['hours/0/open/2/start']
yelp_clean['hours_tue_close'] = yelp['hours/0/open/2/end']
yelp_clean['hours_wed_open'] = yelp['hours/0/open/3/start']
yelp_clean['hours_wed_close'] = yelp['hours/0/open/3/end']
yelp_clean['hours_thu_open'] = yelp['hours/0/open/4/start']
yelp_clean['hours_thu_close'] = yelp['hours/0/open/4/end']
yelp_clean['hours_fri_open'] = yelp['hours/0/open/5/start']
yelp_clean['hours_fir_close'] = yelp['hours/0/open/5/end']
yelp_clean['hours_sat_open'] = yelp['hours/0/open/6/start']
yelp_clean['hours_sat_close'] = yelp['hours/0/open/6/end']

# clean attributes
yelp_clean.loc[yelp_clean['hours_sun_open'] == 0,10:] = None
yelp_clean.iloc[:,10:] = yelp_clean.iloc[:,10:].replace([0],[2400])
yelp_clean.loc[yelp_clean['phone'] < 10**9, 6] = None
yelp_clean.loc[yelp_clean['phone'] > 10**10, 6] = None

# another version with more information for later stage
yelp_more = yelp_clean[:];
yelp_more['latitude'] = yelp['coordinates/latitude']
yelp_more['longitude'] = yelp['coordinates/longitude']
yelp_more['id'] = yelp['Unnamed: 0']

# yelp_clean = yelp_clean.sort_values('name')
# yelp_more = yelp_more.sort_values('name')


# process "tripadvisor_la" data
trip0 = pd.read_csv("tripadvisor_la.csv");
trip0['duplicated'] = trip0.duplicated(subset = ['name','address_street'],keep='first')
trip = trip0[trip0['duplicated'] == False]

# dict & func
pricedict_trip = {'$':1, '$$ - $$$':2.5, '$$$$':4}

# clean yelp dataset
trip_clean = pd.DataFrame();
trip_clean['name'] = trip['name']
trip_clean['category_1'] = trip['type_1']
trip_clean['category_2'] = trip['type_2']
trip_clean['address'] = trip['address_street']
trip_clean['city'] = trip['address_locality'].str.split(',').str[0]
trip_clean['zipcode'] = trip['address_locality'].str.split(',').str[1].str.extract('(\d\d\d\d\d)(?=-)')
trip_clean['phone'] = trip['phone'].str.replace('[+ -]','').apply(pd.to_numeric, errors = 'coerce').apply(trip_phone)
trip_clean['price'] = trip['money'].map(pricedict_trip)
trip_clean['rating'] = trip['rate']
trip_clean['review_count'] = trip['n_reviews']
trip_clean['hours_sun_open'] = trip['sun_hours'].str.split('-').str[0].str.strip().apply(get_hour)
trip_clean['hours_sun_close'] = trip['sun_hours'].str.split('-').str[1].str.strip().apply(get_hour)
trip_clean['hours_mon_open'] = trip['mon_hours'].str.split('-').str[0].str.strip().apply(get_hour)
trip_clean['hours_mon_close'] = trip['mon_hours'].str.split('-').str[1].str.strip().apply(get_hour)
trip_clean['hours_tue_open'] = trip['tue_hours'].str.split('-').str[0].str.strip().apply(get_hour)
trip_clean['hours_tue_close'] = trip['tue_hours'].str.split('-').str[1].str.strip().apply(get_hour)
trip_clean['hours_wed_open'] = trip['wed_hours'].str.split('-').str[0].str.strip().apply(get_hour)
trip_clean['hours_wed_close'] = trip['wed_hours'].str.split('-').str[1].str.strip().apply(get_hour)
trip_clean['hours_thu_open'] = trip['thur_hours'].str.split('-').str[0].str.strip().apply(get_hour)
trip_clean['hours_thu_close'] = trip['thur_hours'].str.split('-').str[1].str.strip().apply(get_hour)
trip_clean['hours_fri_open'] = trip['fri_hours'].str.split('-').str[0].str.strip().apply(get_hour)
trip_clean['hours_fri_close'] = trip['fri_hours'].str.split('-').str[1].str.strip().apply(get_hour)
trip_clean['hours_sat_open'] = trip['sat_hours'].str.split('-').str[0].str.strip().apply(get_hour)
trip_clean['hours_sat_close'] = trip['sat_hours'].str.split('-').str[1].str.strip().apply(get_hour)

# another version with more information
trip_more = trip_clean[:];
trip_more['category_3'] = trip['type_3']
trip_more['zipcode_full'] = trip['address_locality'].str.split(',').str[1].str.extract('(\d\d\d\d\d-\d\d\d\d)')
trip_more['id'] = trip['id']

# save
yelp_clean.to_csv('A.csv', index = False)
trip_clean.to_csv('B.csv',index = False)
yelp_more.to_csv('yelp_full.csv', index = False)
trip_more.to_csv('trip_full.csv', index = False)
