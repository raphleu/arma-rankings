# To run this, you must first import the appropriate dependencies. You can do pip install -r requirements.txt
# if you have the requirements.txt, otherwise do pip install google-cloud-storage

# You also need to have proper credentials for accessing the appropriate buckets. For that, get the JSON cred file from
# me (raph) and make sure you set an environment variable named GOOGLE_APPLICATION_CREDENTIALS to the absolute path of that file.

from google.cloud import storage
from google.cloud.storage import Blob
import sys

match_subtype = 'pickup-fortress1'

client = storage.Client()
bucket = client.get_bucket("unparsed_server_logs")

match_results_blob = Blob(match_subtype + '/ladderlog.txt', bucket)
try:
    with open("ladderlog.txt", "r") as log_file:
        match_results_blob.upload_from_file(log_file)
except IOError:
    print "Couldn't open ladderlog.txt. Are you sure it exists in the same directory as this script?"
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise