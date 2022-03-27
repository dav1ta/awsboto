import boto3

import os
import sys
import threading


s3 = boto3.client('s3')
with open('FILE_NAME', 'rb') as f:
    s3.upload_fileobj(f, 'BUCKET_NAME', 'OBJECT_NAME')


s3.upload_file(
    'FILE_NAME',
    'BUCKET_NAME',
    'OBJECT_NAME',
    ExtraArgs={
        'Metadata': {'mykey': 'myvalue'},
        'ACL': 'public-read',
        'GrantRead': 'uri="http://acs.amazonaws.com/groups/global/AllUsers"',
        'GrantFullControl': 'id="01234567890abcdefg"',
    },
)

# with progress bar


class ProgressPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                '\r%s  %s / %s  (%.2f%%)'
                % (self._filename, self._seen_so_far, self._size, percentage)
            )
            sys.stdout.flush()
