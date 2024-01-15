import os
import sys
import requests
import hashlib
import time

# ThreatGrid Settings
tgurl = 'https://panacea.threatgrid.com/api/v2/samples'
tg_api_key = 'YOUR_API_KEY_HERE'

###NOTE the samples are submitted as private
form_data = {'api_key': tg_api_key, 'private': 'true'}

def md5hash(file):
    BSIZE = 65536
    hnd = open(file, 'rb')
    hashmd5 = hashlib.md5()
    while True:
        info = hnd.read(BSIZE)
        if not info:
            break
        hashmd5.update(info)
    return hashmd5.hexdigest()

def submit_file(file):
    try:
        subres = requests.post(tgurl + '?', files=sample, data=form_data, verify=True)
        if subres.status_code == 200:
            sampleid = subres.json()["data"]["id"]
            submittedat = subres.json()["data"]["submitted_at"]
            submittedfile = subres.json()["data"]["filename"]
            fileMd5 = subres.json()["data"]["md5"]
            fileSHA1 = subres.json()["data"]["sha1"]
            fileSHA256 = subres.json()["data"]["sha256"]
            print("[ THREATGRID STATUS: Successful file submission ]")
            print('--------------------------------------------------------------------------')
            print("  Submitted at: {0}".format(str(submittedat)))
            print("  Sample ID: {0}".format(str(sampleid)))
            print()
            print("  Submitted file: {0}".format(str(submittedfile)))
            print()
            print("     MD5: {0}".format(str(fileMd5)))
            print("    SHA1: {0}".format(str(fileSHA1)))
            print("  SHA256: {0}".format(str(fileSHA256)))
            print('--------------------------------------------------------------------------')
            print()
            print()
            return sampleid
        else:
            print("ERROR: Something went wrong in {0}. Error: {1}".format(sys._getframe().f_code.co_name, str(subres.text)))
            sys.exit()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("ERROR: Error in {location}.{funct_name}() - line {line_no} : {error}".format(location=__name__, funct_name=sys._getframe().f_code.co_name, line_no=exc_tb.tb_lineno, error=str(e), ))
        sys.exit()

input_param = sys.argv[1]
input_files = []
unique_files = []

# Validate a parameter was provided as an argument
if len(sys.argv) < 2:
    sys.exit('Usage:\n %s sample' % sys.argv[0])

# If the supplied parameter is a file validate it exists
if not os.path.exists(input_param):
    sys.exit('File {} doesn\'t exist'.format(input_param))

# Check if the supplied parameter is a directory
if os.path.isdir(input_param):
    print()
    print('You have supplied a directory')
    print()
    for (dirpath, dirnames, filenames) in os.walk(input_param):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            file_hash = md5hash(file_path)
            if file_hash not in unique_files:
                unique_files.append(file_hash)
                input_files.append(file_path)
            else:
                os.remove(file_path)            
else:
    # Append the provided parameter to input_files
    input_files.append(input_param)

number_of_files = len(input_files)

print("------------------------")
print("SUBMITTING [ {0} ] FILES".format(str(number_of_files)))
print("------------------------")
print()
for file in input_files:
    sample = {'sample': open(file, 'rb')}
    submit_file(sample)

time.sleep(10)