from flask import Flask, jsonify, request, json, make_response
import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# use old timey variable interpolation because PyCharm is going crazy
logfile = logging.FileHandler("{}.log".format(__name__))
logfile.setFormatter(formatter)
logger.addHandler(logfile)
logger.setLevel('INFO')

app = Flask(__name__)

contacts = [0, []]

@app.route('/contactdb', methods=['GET'])
def get_contacts():
    try:
        sortedcontactlist = contacts[1]
        sortedcontactlist.sort(key=lambda x:'{} {}'.format(x["lname"], x["fname"]))
        logger.info('returning {} contacts {}'.format(contacts[0], sortedcontactlist))
        # I want to return an ordered map, so I'll build the json myself
        retval = "{0}, [".format(contacts[0])
        if contacts[0] > 0:
            first = True
            for jsn in [json.dumps(contact) for contact in sortedcontactlist]:
                retval = '{}\n{}\t{}'.format(retval, '' if first else ',', jsn)
        retval += "\n]"
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
        # blow up if fname and lname are not received -- FUNCTIONAL LOG MESSAGE
        logger.info("received {} {}".format(contact['fname'], contact['lname']))
        contacts[0] += 1
        contactlist = contacts[1]
        contactlist.append(contact)
        contacts[1] = contactlist
        return jsonify(contacts) # return the new unordered dict
    except Exception as e:
        logger.error(e)
        return jsonify(e)