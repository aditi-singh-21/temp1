from flask import request, jsonify,Blueprint
from core.recommendation_engine.get_vendors import get_vendors

recommended_vendors = Blueprint('recommended', __name__)
@recommended_vendors.route('/get-vendors', methods=['POST'])

def get_recommended_vendors():
    
    data = request.get_json()
    input_slug = data.get('slug')
    num_vendors = data.get('num_vendors', 10) #if not provided , set 10
    if not input_slug:
        return jsonify({"error": "No slug provided"}), 400
    
    vendors = get_vendors(input_slug,num_vendors)
    if isinstance(vendors, tuple) and vendors[1] == 404:
        return vendors
    if 'error' in vendors.get_json():
        return vendors, 404
    
    return vendors, 200

