from flask import Flask, request, render_template
from server_common import *
import log as log
import simple_chain as b
# initialise the flask app
app = Flask(__name__)


@app.route('/chain', methods=['GET'])
def get_entire_chain():
    return create_json_response(chain.to_dict(), suppress_logging=True)


@app.route('/block', methods=['POST'])
def post_block():
    data = parse_request_data(request)
    errors = []
    global chain
    if 'previous_hash' not in data or data['previous_hash'] == '':
        errors.append('"previous_hash" cannot be empty')
    elif data['previous_hash'] != b.next_previous_hash(chain):
        errors.append('{} is not a correct previous hash'.format(data['previous_hash']))
    if 'message' not in data or data['message'] == '':
        errors.append('"message" cannot be empty')
    if errors:
        say_next_previous_hash()
        return create_error_response(errors)
    chain = b.add_new_block_to_chain(chain, data['previous_hash'], data['message'])
    response = create_json_response(b.last_block(chain).__dict__, status_code=201)
    say_next_previous_hash()
    return response


@app.route('/dashboard', methods=['GET'])
def get_dashboard():
    return render_template('dashboard.html', blocks=reversed(chain.blocks))


def say_next_previous_hash():
    log.log('----> next "previous_hash" is: "{}"'.format(get_next_previous_hash()))


def get_next_previous_hash():
    return b.next_previous_hash(chain)

if __name__ == '__main__':
    # create an empty chain
    chain = b.new_chain()
    b.add_new_block_to_chain(chain, get_next_previous_hash(), 'bob sends $4 to alice')
    b.add_new_block_to_chain(chain, get_next_previous_hash(), 'alice send $3 to bob')
    b.add_new_block_to_chain(chain, 'b6b9eb45395b098d2d5c84ee1dc566c9016a5a5a84d716a7df40d2795892b69a', 'bob sends $100 to charles')
    b.add_new_block_to_chain(chain, get_next_previous_hash(), 'alice sends $1 to bob')
    say_next_previous_hash()
    app.run(port=8080)
