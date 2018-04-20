import json
from blockchain import *

chain = new_chain()
add_new_block_to_chain(chain, 'hello', '2')
add_new_block_to_chain(chain, 'hello again', '2')
add_new_block_to_chain(chain, 'hey', '2')
print(json.dumps(chain.to_dict(), indent=4))

print(validate_block_data_for_chain(chain, '4', '', ''))
print(validate_block_data_for_chain(chain, hash_block(last_block(chain)), proof='', data='jumblesale'))
