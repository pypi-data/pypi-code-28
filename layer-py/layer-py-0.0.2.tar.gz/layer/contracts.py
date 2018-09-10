import json
from web3 import Web3


layerAddress = Web3.toChecksumAddress(
    '0x1eec085e9c39eeccb3277d1104599ac18ab8fe27')
layerAbi = """[
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"name": "previousOwner",
				"type": "address"
			},
			{
				"indexed": true,
				"name": "newOwner",
				"type": "address"
			}
		],
		"name": "OwnershipTransferred",
		"type": "event"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_addr",
				"type": "address"
			},
			{
				"name": "_url",
				"type": "string"
			}
		],
		"name": "addLayerNode",
		"outputs": [
			{
				"name": "",
				"type": "address"
			},
			{
				"name": "",
				"type": "string"
			},
			{
				"name": "",
				"type": "address[]"
			}
		],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_addr",
				"type": "address"
			},
			{
				"name": "_name",
				"type": "string"
			},
			{
				"name": "_approved",
				"type": "bool"
			},
			{
				"name": "_category",
				"type": "uint256"
			}
		],
		"name": "addProvider",
		"outputs": [
			{
				"name": "",
				"type": "address"
			},
			{
				"name": "",
				"type": "string"
			},
			{
				"name": "",
				"type": "bool"
			},
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_addr",
				"type": "address"
			}
		],
		"name": "deleteLayerNodeByAddress",
		"outputs": [
			{
				"name": "",
				"type": "bool"
			}
		],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_addr",
				"type": "address"
			}
		],
		"name": "deleteProviderByAddress",
		"outputs": [
			{
				"name": "",
				"type": "bool"
			}
		],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_addr",
				"type": "address"
			},
			{
				"name": "_approve",
				"type": "bool"
			}
		],
		"name": "setApproveLayerNode",
		"outputs": [
			{
				"name": "",
				"type": "address"
			},
			{
				"name": "",
				"type": "bool"
			}
		],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_addr",
				"type": "address"
			},
			{
				"name": "_approve",
				"type": "bool"
			}
		],
		"name": "setApproveProvider",
		"outputs": [
			{
				"name": "",
				"type": "address"
			},
			{
				"name": "",
				"type": "bool"
			}
		],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "newOwner",
				"type": "address"
			}
		],
		"name": "transferOwnership",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_addr",
				"type": "address"
			},
			{
				"name": "_url",
				"type": "string"
			}
		],
		"name": "updateLayerNodeUrl",
		"outputs": [
			{
				"name": "",
				"type": "address"
			},
			{
				"name": "",
				"type": "string"
			}
		],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "_addr",
				"type": "address"
			}
		],
		"name": "getLayerNodeByAddress",
		"outputs": [
			{
				"name": "",
				"type": "address"
			},
			{
				"name": "",
				"type": "string"
			},
			{
				"name": "",
				"type": "bool"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "getLayerNodes",
		"outputs": [
			{
				"name": "",
				"type": "address[]"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "_addr",
				"type": "address"
			}
		],
		"name": "getProviderByAddress",
		"outputs": [
			{
				"name": "",
				"type": "address"
			},
			{
				"name": "",
				"type": "string"
			},
			{
				"name": "",
				"type": "bool"
			},
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "getProviders",
		"outputs": [
			{
				"name": "",
				"type": "address[]"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"name": "",
				"type": "address"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	}
]"""

DEFAULT_GETH_RPC_HOST = 'http://34.233.128.254:8555'


class Contracts:
    __w3 = None
    layer_contract = None

    def __init__(self, geth_rpc_host=DEFAULT_GETH_RPC_HOST):
        w3 = Web3(Web3.HTTPProvider(geth_rpc_host))
        self.__w3 = w3
        self.layer_contract = self.__w3.eth.contract(
            address=layerAddress, abi=layerAbi)

    def getBlockNumber(self):
        return self.__w3.eth.blockNumber

    def getLayerNodes(self):
        return self.layer_contract.functions.getLayerNodes().call()

    def getLayerNodeByAddress(self, addr):
        try:
            addr = Web3.toChecksumAddress(addr)
        except Exception:
            return None

        try:
            info = self.layer_contract.functions.getLayerNodeByAddress(
                addr).call()
            return {
                'address': info[0],
                'url': info[1],
                'approved': info[2]
            }
        except Exception:
            return None

    def getProviders(self):
        return self.layer_contract.functions.getProviders().call()

    def getProviderByAddress(self, addr):
        try:
            addr = Web3.toChecksumAddress(addr)
        except Exception:
            return None

        try:
            info = self.layer_contract.functions.getProviderByAddress(
                addr).call()
            return {
                'address': info[0],
                'name': info[1],
                'approved': info[2],
                'category': info[3],
            }
        except Exception:
            return None

    def owner(self):
        return self.layer_contract.functions.owner().call()

    # setter

    def transferOwnership(self, newOwner):
        return self.layer_contract.functions.transferOwnership(newOwner).call()

    def addLayerNode(self, my_address, my_privKey, address, url):
        try:
            my_address = Web3.toChecksumAddress(my_address)
        except Exception:
            return 'invalid my_address', None

        if not my_privKey:
            return 'empty my_privKey', None

        try:
            address = Web3.toChecksumAddress(address)
        except Exception:
            return 'invalid address', None

        if not url:
            return 'empty url', None

        try:
            encodedABI = self.layer_contract.encodeABI(
                fn_name='addLayerNode', args=[address, url])
            gasPrice = self.__w3.eth.gasPrice
            gasEstimate = self.__w3.eth.estimateGas(
                {'from': my_address, 'to': layerAddress, 'data': encodedABI})
            signed_txn = self.__w3.eth.account.signTransaction(dict(
                nonce=self.__w3.eth.getTransactionCount(my_address),
                gasPrice=self.__w3.eth.gasPrice,
                # gas=2000000,
                gas=gasEstimate,
                to=layerAddress,
                value=0,
                data=encodedABI,
            ), my_privKey,)
            tx_hash = self.__w3.eth.sendRawTransaction(
                signed_txn.rawTransaction)
            return None, tx_hash
        except Exception as e:
            # print('encodeABI error: ', e)
            return str(e), None

    def addProvider(self, my_address, my_privKey, address, name, approved, category):
        try:
            my_address = Web3.toChecksumAddress(my_address)
        except Exception:
            return 'invalid my_address', None

        if not my_privKey:
            return 'empty my_privKey', None

        try:
            address = Web3.toChecksumAddress(address)
        except Exception:
            return 'invalid address', None

        if not name:
            return 'empty name', None

        if not category:
            return 'empty category', None

        try:
            encodedABI = self.layer_contract.encodeABI(
                fn_name='addProvider', args=[address, name, approved, category])
            gasPrice = self.__w3.eth.gasPrice
            gasEstimate = self.__w3.eth.estimateGas(
                {'from': my_address, 'to': layerAddress, 'data': encodedABI})
            signed_txn = self.__w3.eth.account.signTransaction(dict(
                nonce=self.__w3.eth.getTransactionCount(my_address),
                gasPrice=self.__w3.eth.gasPrice,
                # gas=2000000,
                gas=gasEstimate,
                to=layerAddress,
                value=0,
                data=encodedABI,
            ), my_privKey,)
            tx_hash = self.__w3.eth.sendRawTransaction(
                signed_txn.rawTransaction)
            return None, tx_hash
        except Exception as e:
            # print('encodeABI error: ', e)
            return str(e), None
