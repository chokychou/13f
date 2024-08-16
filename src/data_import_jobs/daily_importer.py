import os
import sys
import json
from absl import flags
from src.data_import_jobs.utils import *
from src.data_import_jobs.gcp_utils import *
from src.data_import_jobs.daily_import_filings import *
from src.data_import_jobs.daily_import_process import *
from concurrent.futures import ThreadPoolExecutor
import multiprocessing

flags.DEFINE_string("job_stage", "dev", "Pipeline job stage [test/staging/prod].")
flags.DEFINE_string("gcp_project_id", "stocker-416721", "GCP project ID.")

FLAGS = flags.FLAGS
FLAGS(sys.argv)

def run():
    print("Job starting at stage: " + FLAGS.job_stage + "...")

    kStorageBucket = "stocker-datahub-"
    kDatabaseId = kStorageBucket + FLAGS.job_stage

    metadata = Struct(
        gcp_project_id=FLAGS.gcp_project_id,
        database_id=kDatabaseId
    )

    get_filings(metadata=metadata)
    extract_filings_to_issuer(metadata=metadata)
    print("Job finished successfully.")

if __name__ == "__main__":
    run()
