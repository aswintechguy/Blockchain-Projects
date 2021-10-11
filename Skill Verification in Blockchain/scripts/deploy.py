from brownie import accounts, config, network, SkillVerify, Contract
import os

def deploySkillVerify(var=False):
    account = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
    if not os.path.exists('contract_address.txt'):
        skillVerify = SkillVerify.deploy({"from": account})
        f = open("contract_address.txt", "w")
        f.write(skillVerify.address)
        f.close()
    else:
        # address = "0xe78A0F7E598Cc8b0Bb87894B0F60dD2a88d6a8Ab"
        f = open("contract_address.txt", "r")
        address = str(f.read())
        f.close()
        skillVerify = Contract.from_abi(
            "SkillVerify", address, SkillVerify.abi)
    return skillVerify

