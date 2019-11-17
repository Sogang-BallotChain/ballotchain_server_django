from . import interface, config
from web3 import Web3, HTTPProvider

w3 = Web3(HTTPProvider(config.rpc_url))

