[in the context of cryptocurrencies] a decentralised method of solving
the double spending problem
    * a digital currency can be copied for free
    * "A transaction is considered valid when it is included in the
    blockchain that contains the most amount of computational work.
    This makes double-spending impossibly difficult, and more infeasible
    as the size of the overall network grows."
a ledger
centralised or decentralised (in a decentralised model, all nodes have
to have same way of verifying chain, need to deal with byzantine general
problem)
because nodes can arrive at consensus individually, it is impossible to
tamper with history without being able to crack the crypto used on the
chain

## structure
each block is stored with a timestamp and, optionally, an index
each block will have a self-identifying hash
each block’s hash will be a cryptographic hash of the block’s index, timestamp, data, and the hash of the previous block’s hash
first block is a genesis block - "Initial commit"
    * has to be inserted manually

# workshop
* we'll produce a centralised blockchain - has to be, because cost of building it decentralised would be huge
* discuss proof of work concept
* have them mine a new block
* have a centralised server which can be POSTED to to prove they got the block.
    chain records username of person who mined the block
* they will need to provide:
    * the hash of the previous block (hit `block/last` or such)
    * their name
    * a valid proof of work
    * maybe a timestamp?
then we'll have our own block chain

## limitations
* centralised - no consensus
* linear - each block stores its index

the hash of the nth block is hash(block[n-1] + hash(block[n-2]..))

## steps
1. introduction - what is block chain?
1. hash of hashes
1. provable history
1. genesis block
1. let's hash a simple chain
    * practical with simple server, validate chain
1. provide time to validate, then
    * practical, add a new block
1. it was easy to add a block, right? so they have no value
1. crypto currencies use a block chain to store transaction history, 
but each block needs to have some value
1. proof of work
1. let's mine a coin
    * practical with pow, mining coins
