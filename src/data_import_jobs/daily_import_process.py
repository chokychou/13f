import os
import sys
import json
from absl import flags
from src.data_import_jobs.utils import *
from src.data_import_jobs.gcp_utils import *
from concurrent.futures import ThreadPoolExecutor
import multiprocessing

@check_env
def extract_filings_to_issuer(shift_date=0, metadata=None):
    """_summary_
    Filing has type sample.
    """
    # path as key, sample::Issuers as value
    cache_map = {}

    def executorHelper(path, issuer):
        with lock:
            bucket.set_filepath(path).write_file(issuer.SerializeToString())
            print("Wrote to GCP bucket: " + issuer.cusip)
    def infoTableIteratorHelper(sample):
        """
        cache_map = {
            "issuer/a/data":
                issuer {
                    cusip: "a" (Company a):
                        {
                            cik: "1" (Filing 1)
                            date_filed: 2021-01-01
                            value: 1
                        },
                    cusip: "a" (Company b):
                        {
                            cik: "1" (Filing 1)
                            date_filed: 2021-01-01
                            value: 1
                        }
                },
            "issuer/b/data": { ... }
        }
        """
        print("Processing sample: ", sample.cik)
        
        for n_entry in sample.info_table:
            path = issuerCacheFn(n_entry.cusip, form)
            p_issuer = sample_pb2.Issuer()
            with lock:
                if path not in cache_map.keys():
                    p_issuer.ParseFromString(bucket.set_filepath(path).read_file())
                    # Add a thread lock to cache_map
                    cache_map[path] = p_issuer
                else:
                    p_issuer = cache_map[path]
                # Use a ThreadPoolExecutor to update the issuer
                with ThreadPoolExecutor(max_workers=1) as executor:
                    executor.submit(update_issuer_with_new_entry, p_issuer, n_entry, (sample.filing_id, sample.date_filed, sample.cik))

    form = "data"

    try:
        bucket = Bucket(metadata.gcp_project_id, metadata.database_id)
    except:
        raise Exception("Failed to get GCP bucket.")

    date = (datetime.date.today() - datetime.timedelta(days=shift_date)).strftime("%Y-%m-%d")
    serialized_samples = bucket.set_filepath(fileCacheDailyFn(date)).read_file()
    samples = sample_pb2.Samples()
    samples.ParseFromString(serialized_samples)
    #########################################
    # Process CUSIP Mapping Upload to cloud #
    #########################################
    cusip_path = cusipPathGen()
    serialized_cusip_mappings = bucket.set_filepath(cusip_path).read_file()
    cusip_mappings = sample_pb2.CacheMappings()
    cusip_mappings.ParseFromString(serialized_cusip_mappings)

    try:
        for sample in samples.sample:
            for cusip_mapping in list(map(generate_cusip_mapping, sample.info_table)):
                cusip_mappings.cache_mapping[cusip_mapping.key].CopyFrom(cusip_mapping)
    except:
        raise Exception("Failed to generate cusip mappings.")

    try:
        bucket.set_filepath(cusip_path).write_file(
            cusip_mappings.SerializeToString()
        )
    except:
        raise Exception("Failed to write cusip mapping to GCP bucket.")

    m = multiprocessing.Manager()
    lock = m.Lock()

    with ThreadPoolExecutor() as executor:
        executor.map(infoTableIteratorHelper, samples.sample) 

    print("Finshed processing samples.")

    with ThreadPoolExecutor() as executor:
        results = executor.map(executorHelper, *zip(*cache_map.items()))

if __name__ == "__main__":
    flags.DEFINE_string("job_stage", "dev", "Pipeline job stage [test/staging/prod].")
    flags.DEFINE_string("gcp_project_id", "stocker-416721", "GCP project ID.")

    FLAGS = flags.FLAGS
    FLAGS(sys.argv)

    kStorageBucket = "stocker-datahub-"
    kDatabaseId = kStorageBucket + FLAGS.job_stage

    metadata = Struct(
        gcp_project_id=FLAGS.gcp_project_id,
        database_id=kDatabaseId
    )
    
    extract_filings_to_issuer(metadata=metadata)
