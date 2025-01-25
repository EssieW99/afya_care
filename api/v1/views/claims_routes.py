""" API routes for the claims model """

from api.v1.config import Config
from api.v1.views import app_views
from models.db import DB
from models.claims import Claims
from flask import Flask, flash, jsonify, request, make_response, abort, redirect, session, render_template
from datetime import date, datetime
from werkzeug.utils import secure_filename
import os

db = DB()

def auto_review_claim(claim_date,claim_amount, documents, required_documents=1, max_claim=500000):
    """
    Automatically reviews a claim and returns a status to help
    with the review process
    """

    "ensure claim is submitted within 7 days of date of service"
    if isinstance(claim_date, str):
        claim.claim_date = datetime.strptime(claim_date, '%Y-%m-%d').date()

    days_since_service = (date.today() - claim_date).days
    if days_since_service > 7:
        return 'Denied', 'Claim must be submitted within 7 days of the date of service'

    "check maximum claim amount"
    if int(claim_amount) > max_claim:
        return 'Denied', 'Claim amount exceeds the maximum allowed'
    
    "check the number of uploaded documents"
    document_num = len(documents.split(',')) if documents else 0
    if document_num < required_documents:
        return 'Denied', f'Minimum {required_documents} documents are required to process claim'
    
    "default flag for manual review"
    return 'Pending', 'Claim requires further review'

@app_views.route('/claims', methods=['POST'], strict_slashes=False)
def upload_claims():
    """ saves claim reports in the databse"""

    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not authenticated'}), 401

    claim_date = request.form['claim_date']
    claim_type = request.form['claim_type']
    claim_amount = request.form['claim_amount']

    print(f"Received claim_date: {claim_date}, claim_type: {claim_type}, claim_amount: {claim_amount}")

    if not claim_date or not claim_type or not claim_amount:
        return render_template('claims.html', error_message="Missing claim details")
    
    try:
        claim_date = datetime.strptime(claim_date, '%m-%d-%Y').date()
    except ValueError:
        return render_template('claims.html', error_message="Invalid date format. Please use MM-DD-YYYY")

    if 'files[]' not in request.files:
        return render_template('claims.html', error_message="No files provided")
    
    documents = request.files.getlist('files[]')
    document_paths = []
    UPLOAD_FOLDER = Config.UPLOAD_FOLDER

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    for document in documents:
        if document:
            filename = secure_filename(document.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            document.save(file_path)
            document_paths.append(file_path)

    document_str = (',').join(document_paths)

    status, message = auto_review_claim(claim_date, claim_amount, ','.join(document_paths))
    if status == 'Denied':
        return render_template('claims.html', error_message=message)

    claim = db.save_claim(user_id=user_id, claim_date=claim_date, claim_type=claim_type, claim_amount=claim_amount, documents=document_str)
    if claim:
        claim.status = status
        claim.review_message = message
        db.save()
        return render_template('claims.html', message="Submitted Successfully. Pending Review")
    else:
        return render_template('claims.html', error_message="Error saving claim. Try Again")
    
@app_views.route('/claims/user', methods=['GET'], strict_slashes=False)
def get_claim_by_id(user_id):
    """
    gets all the claims made by a specific user
    """

    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'errror': 'User not authenticated'}), 401
    claims = db.get_claims_by_user(user_id)
    if not claims:
        return jsonify({'error': f'No claims found for user ID {user_id}'}), 404
    
    return jsonify([claim.to_dict() for claim in claims]), 200

@app_views.route('/claims/<string:claim_type>', methods=['GET'], strict_slashes=False)
def get_claims_by_type(claim_type):
    """
    gets all the claims under a certain type
    """

    claims = db.get_claims_by_type(claim_type)
    if not claims:
        return jsonify({'error': f'No claims found for the type {claim_type}'}), 404
    
    return jsonify([claim.to_dict() for claim in claims]), 200

@app_views.route('/claims/users', methods=['GET'], strict_slashes=False)
def get_all_claims():
    """
    gets all the claims made
    """

    claims = db.get_all_claims()
    if not claims:
        return jsonify({'error': 'No claims found'}), 404
    
    return jsonify([claim.to_dict() for claim in claims])
