#Creating utility functions or helping functions

import re

def clean_services(services):
    if not services:
        return ""
    if isinstance(services, str):
        return services
    return " ".join(services)

def check_category_in_services(category, services):
    category = category.lower()
    if isinstance(services, list):
        services = " ".join(services)
    services = services.lower()
    services = re.sub(r'[^\w\s]', '', services)
    return category in services

def category_in_services_search(input_category, same_city_vendor):
    matching_vendors = [v for v in same_city_vendor if check_category_in_services(input_category, v.get("services", ""))]
    return matching_vendors


def ensure_dict(vendor):
    if isinstance(vendor, tuple):
        vendor = vendor[0]
    return vendor if isinstance(vendor, dict) else {}


def duplicates_removal(similar_vendors,input_vendor):
    slugs = set()
    unique_vendors =[]
    for ven in similar_vendors:
        if ven['slug'] not in slugs and ven['slug'] != input_vendor['slug']:
            slugs.add(ven['slug'])
            unique_vendors.append(ven)
    return unique_vendors

