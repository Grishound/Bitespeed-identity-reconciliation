from flask import jsonify, request
from app import app
from .models import db, Contact
from .functions import get_existing_primary_contacts, get_current_time, return_response

@app.route('/identify', methods=['POST'])
def identify_contact():
    data = request.json
    email = data.get('email')
    phone_number = data.get('phoneNumber')

    # Check if the incoming request has any existing contacts
    if not email and not phone_number:
        # no phone_number or email provided.
        return jsonify({"message": "Neither email nor phoneNumber present."}), 404

    elif not email:
        # only phone_number provided
        existing_primary_contacts = get_existing_primary_contacts(phone_number=phone_number)

        if not existing_primary_contacts:
            # Create a new primary contact if no existing contacts are found
            current_time = get_current_time()
            primary_contact = Contact(
                phoneNumber=phone_number,
                email=email,
                linkPrecedence="primary",
                createdAt=current_time,
                updatedAt=current_time
            )
            db.session.add(primary_contact)
            db.session.commit()
            secondary_contacts = []
        else:
            primary_contact = existing_primary_contacts[0]
            secondary_contacts = Contact.query.filter_by(linkedId=primary_contact.id).all()

    elif not phone_number:
        # only email provided
        existing_primary_contacts = get_existing_primary_contacts(email=email)

        if not existing_primary_contacts:
            # Create a new primary contact if no existing contacts are found
            current_time = get_current_time()
            primary_contact = Contact(
                phoneNumber=phone_number,
                email=email,
                linkPrecedence="primary",
                createdAt=current_time,
                updatedAt=current_time
            )
            db.session.add(primary_contact)
            db.session.commit()
            secondary_contacts = []
        else:
            primary_contact = existing_primary_contacts[0]
            secondary_contacts = Contact.query.filter_by(linkedId=primary_contact.id).all()

    else:
        # both phone_number and email present
        existing_primary_contacts = get_existing_primary_contacts(email=email, phone_number=phone_number)

        if not existing_primary_contacts:
            # Create a new primary contact if no existing contacts are found
            current_time = get_current_time()
            primary_contact = Contact(
                phoneNumber=phone_number,
                email=email,
                linkPrecedence="primary",
                createdAt=current_time,
                updatedAt=current_time
            )
            db.session.add(primary_contact)
            db.session.commit()
            secondary_contacts = []
        else:
            primary_contact = existing_primary_contacts[0]

            if len(existing_primary_contacts) == 2:
                # change second_primary to secondary and map its secondary_contacts to first_primary
                existing_primary_contacts[1].linkPrecedence = "secondary"
                existing_primary_contacts[1].linkedId = primary_contact.id
                existing_primary_contacts[1].updatedAt = get_current_time()
                extra_secondary_contacts = Contact.query.filter_by(linkedId=existing_primary_contacts[1].id).all()
                for contact in extra_secondary_contacts:
                    contact.linkedId = primary_contact.id
                    contact.updatedAt = get_current_time()
                db.session.commit()

                secondary_contacts = Contact.query.filter_by(linkedId=primary_contact.id).all()

            else:
                # single primary contact
                email_exists = db.session.query(db.exists().where(Contact.email == email)).scalar()
                phone_number_exists = db.session.query(db.exists().where(Contact.phoneNumber == phone_number)).scalar()

                if not email_exists or not phone_number_exists:
                    # Create a new secondary contact if contact has some new information
                    current_time = get_current_time()
                    new_secondary_contact = Contact(
                        phoneNumber=phone_number,
                        email=email,
                        linkedId=primary_contact.id,
                        linkPrecedence="secondary",
                        createdAt=current_time,
                        updatedAt=current_time
                    )
                    db.session.add(new_secondary_contact)
                    db.session.commit()

                secondary_contacts = Contact.query.filter_by(linkedId=primary_contact.id).all()

    # Prepare the response payload
    response = return_response(primary_contact, secondary_contacts)

    return jsonify(response), 200
