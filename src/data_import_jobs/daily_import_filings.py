import os
import sys
import json
from absl import flags
from src.data_import_jobs.utils import *
from src.data_import_jobs.gcp_utils import *
from concurrent.futures import ThreadPoolExecutor
import multiprocessing

@check_env
def get_filings(shift_date=0, disable_cache=0, metadata=None):
    """
    Returns:
        samples: samples::Samples

        For example:
        sample {
            sample {
                cik: "1" (Filing 1)
                date_filed: 2021-01-01
                info_table {
                    cusip: "a" (Company a)
                    value: 1
                }
                info_table {
                    cusip: "b" (Company b)
                    value: 1
                }
            }
        }
    """
    try:
        bucket = Bucket(metadata.gcp_project_id, metadata.database_id)
    except:
        raise Exception("Failed to get GCP bucket.")

    date = (datetime.date.today() - datetime.timedelta(days=shift_date)).strftime("%Y-%m-%d")
    path = fileCacheDailyFn(date)

    samples = sample_pb2.Samples()
    data = bucket.set_filepath(path).read_file()
    samples.ParseFromString(data)

    if len(samples.sample) != 0 and not disable_cache:
        print("Got samples from cache: ", path)
        return samples

    try:
        print("Getting latest 13F filings...")
        # Query latest 13F list.
        latest_filings = latest_thirteen_f_filings()

        # Download from the above query
        latest_filings = list(map(process_latest_filings, latest_filings))

    except:
        raise Exception("Failed to get latest 13F filings.")

    assert len(latest_filings) != 0, "No 13F filings found."

    #######################################
    # Process Cik Mapping Upload to cloud #
    #######################################
    cik_path = cikPathGen()
    serialized_cik_mappings = bucket.set_filepath(cik_path).read_file()
    cik_mappings = sample_pb2.CacheMappings()
    cik_mappings.ParseFromString(serialized_cik_mappings)

    try:
        for cik_mapping in list(map(generate_cik_mapping, latest_filings)):
            cik_mappings.cache_mapping[cik_mapping.key].CopyFrom(cik_mapping)
    except:
        raise Exception("Failed to generate cik mappings.")

    try:
        bucket.set_filepath(cik_path).write_file(
            cik_mappings.SerializeToString()
        )
    except:
        raise Exception("Failed to write latest 13F filings to GCP bucket.")

    #######################################
    # Process Samples Upload to cloud     #
    #######################################
    try:
        samples = sample_pb2.Samples()
        for filing in list(map(parse_to_proto_str, latest_filings)):
            samples.sample.append(filing)
    except:
        raise Exception("Failed to add to samples.")

    try:
        bucket.set_filepath(path).write_file(
            samples.SerializeToString()
        )
    except:
        raise Exception("Failed to write latest 13F filings to GCP bucket.")

    return samples


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
    get_filings(disable_cache=1, metadata=metadata)
