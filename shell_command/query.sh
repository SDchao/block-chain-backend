export FABRIC_PATH=/home/sdchao/BlockChain/fabric-samples
export NETWORK_PATH=$FABRIC_PATH/test-network
export FABRIC_CFG_PATH=$FABRIC_PATH/config/
export CORE_PEER_TLS_ENABLED=true
export CORE_PEER_LOCALMSPID="Org1MSP"
export CORE_PEER_TLS_ROOTCERT_FILE=$NETWORK_PATH/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=$NETWORK_PATH/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
export CORE_PEER_ADDRESS=localhost:7051
peer chaincode query -C mychannel -n basic -c $1
# tobecontinued