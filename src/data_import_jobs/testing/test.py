import src.proto.sample_pb2 as sample_pb2
from src.data_import_jobs.utils import *
from src.data_import_jobs.gcp_utils import *


##########################
# Cusip
def test_cusip():
    data = bucket.set_filepath("issuer/02079K107/data").read_file()

    proto_str = sample_pb2.Issuer()
    proto_str.ParseFromString(data)
    print(proto_str)


##########################
# 13f
def test_13f():
    date = "2024-07-10"
    path = fileCacheDailyFn(date)

    samples = sample_pb2.Samples()
    data = bucket.set_filepath(path).read_file()
    samples.ParseFromString(data)
    print(samples)

def read_cache_map():
    path = "form_13f/cik_mapping/data"
    cache_mappings = sample_pb2.CacheMappings()
    data = bucket.set_filepath(path).read_file()
    cache_mappings.ParseFromString(data)
    print(cache_mappings)

if __name__ == "__main__":
    bucket = Bucket("stocker-416721", "stocker-datahub-dev")
    test_13f()
