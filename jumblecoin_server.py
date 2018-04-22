from flask import Flask, request, render_template
from server_common import *
import json
import log as log
import jumblecoin as b
import miner
from miner import mine_next

# initialise the flask app
app = Flask(__name__)

# create an empty chain
chain = b.new_chain()

previous_proof = b.last_block(chain).proof
b.add_new_block_to_chain(chain, json.dumps({'name': 'bob', 'value': 1}), mine_next(previous_proof))
previous_proof = b.last_block(chain).proof
b.add_new_block_to_chain(chain, json.dumps({'name': 'alice', 'value': 1}), mine_next(previous_proof))
previous_proof = b.last_block(chain).proof
b.add_new_block_to_chain(chain, json.dumps({'name': 'charles', 'value': 1}), mine_next(previous_proof))
log.log(json.dumps(chain.to_dict()))


@app.route('/chain', methods=['GET'])
def get_entire_chain():
    return create_json_response(chain.to_dict())


@app.route('/last_block', methods=['GET'])
def get_last_block():
    return create_json_response(b.last_block(chain).__dict__)


@app.route('/block', methods=['POST'])
def post_new_block():
    log.log('received block creation request with data: {}'.format(request.get_data()))
    data = parse_request_data(request)
    # validate the request has all required fields
    errors = []
    if 'recipient' not in data or data['recipient'] == '':
        errors.append('"recipient" cannot be empty')
    if 'previous_hash' not in data or data['previous_hash'] == '':
        errors.append('"previous_hash" cannot be empty')
    if 'proof' not in data:
        errors.append('"proof" cannot be empty')
    if errors:
        return create_error_response(errors)
    block_data = json.dumps({'name': data['recipient'], 'value': 1})
    # validate the contents of the request is cromulent
    global chain
    success, errors = b.validate_block_data_for_chain(
        chain=chain,
        previous_hash=data['previous_hash'],
        proof=data['proof'],
        data=block_data
    )
    if not success:
        return create_error_response(errors)
    # everything was ok
    new_chain = b.add_new_block_to_chain(chain, block_data, data['proof'])
    chain = new_chain
    log.log('block for {} added'.format(json.loads(block_data)['name']))
    say_next_properties()
    print(generate_leader_board())
    return create_json_response(chain.to_dict(), status_code=201)


def say_next_properties():
    log.log('----> next "previous_hash" will be {}'.format(b.hash_block(b.last_block(chain))))
    log.log('----> next "proof" will be: {}'.format(mine_next(b.last_block(chain).proof)))


@app.route('/cost', methods=['POST'])
def increase_cost():
    data = parse_request_data(request)
    if 'secret' not in data or data['secret'] != '8fb5c3b9d42e089f74dd1b9accda2f507c1e589aef6876b2697b0de42fb65255':
        log.log('secret missing or invalid')
        return make_response('', 404)
    new_cost = data['cost']
    b.PROOF_COST = new_cost
    miner.PROOF_COST = new_cost
    log.log('NEW COST is now {}'.format(b.PROOF_COST))
    say_next_properties()
    return make_response('', 201)


@app.route('/leaderboard', methods=['GET'])
def get_dashboard():
    return render_template(
        'leaderboard.html',
        leaders=generate_leader_board(),
        blocks=chain.blocks
    )


def generate_leader_board() -> (str, int):
    leaders = {}
    global chain
    for block in chain.blocks:
        data = json.loads(block.data)
        value = int(data['value'])
        name = data['name']
        if name not in leaders:
            leaders[name] = value
        else:
            leaders[name] += value
    sorted_leaders = sorted(leaders, key=leaders.get)
    leader_tuples = []
    for leader in reversed(sorted_leaders):
        leader_tuples.append((leader, leaders[leader]))
    return leader_tuples


if __name__ == '__main__':
    say_next_properties()
    app.run(port=8080)
