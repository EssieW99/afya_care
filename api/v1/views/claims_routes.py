""" API routes for the claims model """

from api.v1.views import app_views
from models.db import DB
from models.claims import Claims
from flask import Flask, flash, jsonify, request, make_response, abort, redirect, session
from datetime import date, datetime

db = DB()

def auto_review_claim(claim, required_documents=1, max_claim=100000):
    """
    Automatically reviews a claim and returns a status to help
    with the review process
    """

    "ensure claim is submitted within 7 days of date of service"
    days_since_service = (date.today() - claim.claim_date).days
    if days_since_service > 7:
        return 'Denied', 'Claim must be submitted within 7 days of the date of service'

    "check maximum claim amount"
    if claim.claim_amount > max_claim:
        return 'Denied', 'Claim amount exceeds the maximum allowed'
    
    "check the number of uploaded documents"
    document_num = len(claim.documents.split(',')) if claim.documents else 0
    if document_num < required_documents:
        return 'Denied', f'Minimum {required_documents} documents are required to process claim'
    
    "default flag for manual review"
    return 'Pending', 'Claim requires further review'

@app_views.route('/claims', methods=['POST'], strict_slashes=False)
def upload_claims():
    """ saves claim reports in the databse"""

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing data'}), 400

    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not authenticated'}), 401

    claim_date = data.get('claim_date')
    claim_type = data.get('claim_type')
    claim_amount = data.get('claim_amount')
    documents = data.get('documents')

    if not claim_date or not claim_type or not claim_amount:
        return jsonify({'error': 'Missing required claim details'}), 400

    documents_str = ','.join(documents) if isinstance(documents, list) else None

    try:
        claim_date = datetime.strptime(claim_date, '%m-%d-%Y').date()
    except ValueError:
        return jsonify({'error': 'Invalid claim date format'}), 400

    claim = db.save_claim(user_id=user_id, claim_date=claim_date, claim_type=claim_type, claim_amount=claim_amount, documents=documents_str)
    if claim:
        status, message = auto_review_claim(claim)
        claim.status = status
        claim.review_message = message
        db.save()
        return jsonify({'message': 'Claim successfully submitted!', 'status': status, 'review_message': message}), 200
    else:
        return jsonify({'error': 'Error saving the claim'}), 500
    
@app_views.route('/claims/user', methods=['GET'], strict_slashes=False)
def get_claim_by_id(user_id):
    """
    gets all the claims made by a specific user
    """

    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'errror': 'User not authenticated'}), 401
    claims = DB.get_claims_by_user(user_id)
    if not claims:
        return jsonify({'error': f'No claims found for user ID {user_id}'}), 404
    
    return jsonify([claim.to_dict() for claim in claims]), 200

@app_views.route('/claims/<string:claim_type>', methods=['GET'], strict_slashes=False)
def get_claims_by_type(claim_type):
    """
    gets all the claims under a certain type
    """

    claims = DB.get_claims_by_type(claim_type)
    if not claims:
        return jsonify({'error': f'No claims found for the type {claim_type}'}), 404
    
    return jsonify([claim.to_dict() for claim in claims]), 200

@app_views.route('/claims', methods=['GET'], strict_slashes=False)
def get_all_claims():
    """
    gets all the claims made
    """

    claims = DB.get_all_claims()
    if not claims:
        return jsonify({'error': 'No claims found'}), 404
    
    return jsonify([claim.to_dict() for claim in claims])
