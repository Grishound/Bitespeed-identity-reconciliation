from .models import db, Contact
from sqlalchemy import or_
from flask import jsonify
from datetime import datetime
import pytz


def get_current_time():
    """
    Return the current time with IST timezone.
    """
    timeStamp = datetime.now().timestamp()

    # assigning the timezone to the current timestamp
    currentDateTime = datetime.fromtimestamp(timeStamp, pytz.timezone("Asia/Kolkata"))
    return currentDateTime


def get_existing_primary_contacts(**kwargs):
    """
    Return all the primary contacts which match the query.
    If a secondary contact matches the query, its linked primary contact will be added.
    """
    email = kwargs.get("email")
    phone_number = kwargs.get("phone_number")
    if email and phone_number:
        matchingContacts = Contact.query.filter(
            or_(Contact.phoneNumber == phone_number, Contact.email == email)
        ).all()
    elif email:
        matchingContacts = Contact.query.filter(or_(Contact.email == email)).all()
    elif phone_number:
        matchingContacts = Contact.query.filter(
            or_(Contact.phoneNumber == phone_number)
        ).all()
    else:
        # this can never happen
        matchingContacts = []

    result = set()
    for contact in matchingContacts:
        if contact.linkPrecedence == "secondary":
            linked_contact = Contact.query.get(contact.linkedId)
            result.add(linked_contact)
        else:
            result.add(contact)
    result = list(result)

    if len(result) == 2:
        # the first element has to be the one with the lowest id
        result.sort(key=lambda x: x.id)

    return result


def return_response(primary_contact, secondary_contacts):
    """
    Returns the JSON response for the query.
    """
    response = {
        "contact": {
            "primaryContactId": primary_contact.id,
            "emails": [primary_contact.email] if primary_contact.email else [],
            "phoneNumbers": [primary_contact.phoneNumber] if primary_contact.phoneNumber else [],
            "secondaryContactIds": [contact.id for contact in secondary_contacts],
        }
    }
    emailSet = set()
    phoneNumberSet = set()
    for contact in secondary_contacts:
        if contact.email:
            emailSet.add(contact.email)
        if contact.phoneNumber:
            phoneNumberSet.add(contact.phoneNumber)

    if primary_contact.email:
        if primary_contact.email in emailSet:
            emailSet.remove(primary_contact.email)
    if primary_contact.phoneNumber:
        if primary_contact.phoneNumber in phoneNumberSet:
            phoneNumberSet.remove(primary_contact.phoneNumber)

    for secondaryEmail in emailSet:
        response["contact"]["emails"].append(secondaryEmail)
    for secondaryPhoneNumber in phoneNumberSet:
        response["contact"]["phoneNumbers"].append(secondaryPhoneNumber)

    return response
