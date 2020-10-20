from google.cloud import storage
from google.cloud.storage import Blob

client = storage.Client()
parsed_bucket = client.get_bucket('parsed_server_logs')

match_subtype = 'pickup-fortress1'

blob = parsed_bucket.blob(match_subtype + '/ladderlog.json')

blob.download_to_filename('raw_data/' + match_subtype + '_parsed.json')