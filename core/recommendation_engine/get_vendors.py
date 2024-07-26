#Functions for vendors

from flask import jsonify,Response
import json
from interfaces.vendor_model import Vendor
from utils.helper import category_in_services_search, duplicates_removal
from utils.vendor_similarity import similar_services
from interfaces.mongodb.db_functions import VendorsRepository

def get_vendors(slug,num_of_recomm):
    vendor_repo = VendorsRepository()
    input_vendor = vendor_repo.find_by_slug(slug)
    if not input_vendor:
        return jsonify({'error': 'Vendor not found'})

    input_category = input_vendor["category"].lower()
    input_address = input_vendor["address"]
    input_services = input_vendor["services"]

    address_list = input_address.split(',')
    input_city = address_list[0]
    input_state = address_list[1][1:]


    services = "|".join(input_services)
    vendors_list = vendor_repo.find_vendors(input_category,input_city,input_state,services)

    combined_vendors = []

    #SEARCH 1 : Same category and same city 
    similar_vendors = []
    for ven in vendors_list:
        address = ven["address"]
        city = address.split(',')[0]
        if city == input_city and ven['category'] == input_category:
            similar_vendors.append(ven)
    combined_vendors = duplicates_removal(similar_vendors,input_vendor)
    combined_vendors 

    #SEARCH 2 : Category in services in same city
    if(len(combined_vendors) < num_of_recomm):
        similar_vendors=[]
        for ven in vendors_list:
            address = ven["address"]
            city = address.split(',')[0]
            if city == input_city :
                similar_vendors.append(ven)
        vendors_with_category_in_services = category_in_services_search(input_category,similar_vendors)
        vendors_with_category_in_services = duplicates_removal(vendors_with_category_in_services, input_vendor)
        combined_vendors = combined_vendors + vendors_with_category_in_services
        
    #SEARCH 3 : Same Category and Same state
    if len(combined_vendors) < num_of_recomm:
        similar_vendors = []
        for ven in vendors_list:
            address = ven["address"]
            state = address.split(',')[1][1:]
            if state == input_state and ven['category'] == input_category:
                similar_vendors.append(ven)
        additional_vendors_2 = duplicates_removal(similar_vendors,input_vendor)
        if (len(additional_vendors_2) > 0):
            combined_vendors = combined_vendors + additional_vendors_2


    #SEARCH 4 : Same state and similar services
    if len(combined_vendors) < num_of_recomm:
        similar_vendors=[]
        for ven in vendors_list:
            address = ven["address"]
            state = address.split(',')[1][1:]
            if state == input_state:
                similar_vendors.append(ven)
        additional_vendors_3 = duplicates_removal(similar_vendors,input_vendor)
        if(len ( additional_vendors_3) > 0):
            additional_vendors_3 = similar_services(input_vendor ,additional_vendors_3)
        if len(additional_vendors_3) > 0:
            combined_vendors = combined_vendors + [v[0] for v in additional_vendors_3]


    combined_vendors= duplicates_removal(combined_vendors,input_vendor)

    if len(combined_vendors) == 0:
        return "No vendors found", 404
    
    combined_vendors = combined_vendors[:num_of_recomm]
    serialized_vendors = {f'vendor_{i+1}': Vendor(vendor['name'], vendor['address'], vendor['category'], vendor['services']).serialize() for i, vendor in enumerate(combined_vendors)}

    response_data = {
        'total_vendors_found': len(serialized_vendors),
        'vendors': serialized_vendors
    }
    
    response_json = json.dumps(response_data, indent=4, ensure_ascii=False)
    return Response(response_json, mimetype='application/json')