# Ropsten configuration
'''
rpc_url = "https://ropsten.infura.io/v3/49b9acbd693940a0bf84fef21253e244"
master = "21DF8E8466D4C5B11BE3E1890C45C99A290BC3D7388151CC658BC35885D50F74"
faucet_url = "http://www.ballotchain.net:9000"
'''

# Geth configuration
# mining 시작하고, 마스터 계정 이더 충분한지 확인하기 
# pub_key -> 0x55969a2b4d94684036fa0948468B8C1D54f15FC2
'''
rpc_url = "http://www.ballotchain.net:8805"
master = "0x41c5c3326bb54c3fad0192672805f8e69d8d368c1545805655935d58a0db497e"
faucet_url = "http://www.ballotchain.net:9000"
'''

# Node0 configuration
# pub_key -> 0x2d1C36bfdFf49290Daa4F1CC66F3a61963f6d9A2, 0x569519ba44a386951f7212842e4e405b2d342a14 (locals-faucet)
'''
rpc_url = "http://44.227.84.27:8805"
master = "0x79144f818edcafb2827098b9bd370839990c6fde28f4756d62342dec2a92c1f2"
faucet_url = "http://44.227.84.27:9000"
coinbase = "0x6b082d847a9f469ca2eba8e19bc2d3a8c3a2dcee"
'''

# Node 1, 2, 3 configuration
connection_pool = [
    {
        # Node 1
        'rpc_url': "http://44.229.82.215:8805",
        'coinbase': "0x61c657b1f2bcb975c0c62a10922a6ec5ca7a3fbb"
    },
    {
        # Node 2
        'rpc_url': "http://44.228.100.192:8805",
        'coinbase': "0x5715a4d0664220a29e4b75bbecf236a81c5746cc"
    },
    {
        # Node 3
        'rpc_url': "http://44.228.43.11:8805",
        'coinbase': "0x902005a72a986959c015ddfe05403b7a2498ee1b"
    }
]

rpc_url = connection_pool[0]['rpc_url']
coinbase = connection_pool[0]['coinbase']
master = "0x79144f818edcafb2827098b9bd370839990c6fde28f4756d62342dec2a92c1f2"