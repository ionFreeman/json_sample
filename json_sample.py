from flask import Flask, jsonify, request, json, make_response
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logfile = logging.FileHandler(f"{__name__}.log")
logfile.setFormatter(formatter)
logger.addHandler(logfile)
logger.setLevel('INFO')

app = Flask(__name__)

# JSON does not have Tuples -- contacts is best modeled as a tuple,
# but it will be a list in JSON
contacts: Tuple[int, List[Dict[str, str]]] = [0, []]

@app.route('/contactdb', methods=['GET'])
def get_contacts():
    try:
        sortedcontactlist = contacts[1]
        sortedcontactlist.sort(key=lambda x:f'{x["lname"]} {x["fname"]}')
        # I want to return an sorted list, so I'll build the json myself
        retval = f'{{"count":"{contacts[0]}", "contacts":['
        if contacts[0] > 0:
            first: bool = True
            for jsn in [json.dumps(contact) for contact in sortedcontactlist]:
                comma = u'' if first else u','
                retval = f'{retval} \n {comma}\t{jsn}'
                first = False
        retval += "\n]}"
        logger.info(f'returning {retval}')
        return make_response(retval)
    except Exception as e:
        logger.error(e)
        return jsonify(e)


@app.route('/contactdb', methods=['POST'])
def add_contact():
    # test for required fname and lname fields
    logger.info(request.get_data(as_text = True))
    contact = request.get_json()
    try:
        logger.info(f"received {contact}")
        # scan the list for matching lname, fname
        contactlist = contacts[1]
        for existing in[old for old in contactlist
                        # blow up if fname and lname are not received
                        if old["lname"] == contact["lname"]
                           and old["fname"] == contact["fname"]]:
            contacts[0] -= 1
            contactlist.remove(existing)
        contacts[0] += 1
        contactlist.append(contact)
        contacts[1] = contactlist
        return jsonify(contacts) # return the new unordered dict
    except Exception as e:
        logger.error(e)
        return jsonify(e)