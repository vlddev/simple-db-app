import sys
import traceback
import utils
import requests

#print(f'makeContract return: {utils.makeContract(150, 1, 1)}')

contractList = utils.getContracts(1)
print(f"\ncontracts = {contractList}")
recordingIds = utils.getContractRecordingIds(contractList)
print(f"\nrecordingIds = {recordingIds}")
contractList = utils.extendContractsWithRecording(contractList)
print(f"\nextended contracts = {contractList}")
print("\nsearchByTitleArtist")
err_msg, resultList = utils.searchByTitleArtist('the wind', '', recordingIds)
print(f"err_msg = {err_msg}")
print(f"resultList = {resultList}")
