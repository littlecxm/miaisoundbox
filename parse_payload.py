#!/usr/bin/env python3
#https://github.com/flying1008

import json
import os
import base64
import hashlib
import datetime
import time
import sys
import argparse
import struct

def u32(x):
    return struct.unpack('>I', x)[0]

def u64(x):
    return struct.unpack('>Q', x)[0]

def usage():
    print("Usage:******************* ")
    print("./parse_payload.py payload.bin")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='payload parse')
    parser.add_argument('payloadfile', type=argparse.FileType('rb'),
                    help='payload file name')
    args = parser.parse_args()
    filename =args.payloadfile.name
    magic = args.payloadfile.read(4)
    assert magic == b'CrAU'

    file_format_version = u64(args.payloadfile.read(8))
    assert file_format_version == 2

    manifest_size = u64(args.payloadfile.read(8))

    if file_format_version > 1:
        metadata_signature_size = u32(args.payloadfile.read(4))

    filename =args.payloadfile.name
    sha256 = hashlib.sha256()
    md5 = hashlib.md5()
    with open(filename,"rb") as f:
        while True:
            chunk = f.read(16 * 1024)
            if not chunk:
                break
            md5.update(chunk)
            sha256.update(chunk)
    payload_hash =base64.b64encode(sha256.digest()).decode()
    f.close()
    print("hash:",md5.hexdigest())
    print("FILE_HASH:",payload_hash)
    print("FILE_SIZE:",os.path.getsize(filename))
    sha2 = hashlib.sha256()
    with open(filename,"rb") as w:
        chunk = w.read(manifest_size+24)
        sha2.update(chunk)
    meta_hash =base64.b64encode(sha2.digest()).decode()
    w.close()
    print("METADATA_HASH:",meta_hash)
    print("METADATA_SIZE:",manifest_size+24)

    param={}
    other_param ={}
    param['hash'] = md5.hexdigest()
    other_param['FILE_HASH'] = payload_hash
    other_param['FILE_SIZE'] = str(os.path.getsize(filename))
    other_param['METADATA_HASH'] = meta_hash
    other_param['METADATA_SIZE']= str(manifest_size+24)
    param['otherParam'] = other_param
    print(json.dumps(other_param))
    json_name = os.path.basename(filename) + "_other_param.json"
    other_param_file = open(json_name,"w")
    json.dump(param,other_param_file)
    other_param_file.close()

