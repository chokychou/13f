from google.cloud import storage

class Bucket:

    def __init__(self, gcp_project_id=None, bucket_name =None) -> None:
        self._gcp_project_id = gcp_project_id
        self._bucket_name = bucket_name
        self._blob_name = None
        return
    def set_bucket_name(self, bucket_name):
        self._bucket_name = bucket_name
        return self
    def set_filepath(self, blob_name):
        """_summary_
        blob_name is equivalent to filepath.
        """
        self._blob_name = blob_name
        return self
    def get_blob(self):
        storage_client = storage.Client(project=self._gcp_project_id)
        bucket = storage_client.bucket(self._bucket_name)
        return bucket.blob(self._blob_name)
    def write_file(self, data, should_merge=False):
        with self.get_blob().open("wb") as f:
            f.write(data)
        return self

    def read_file(self):
        data = "".encode("utf-8")
        try:
            with self.get_blob().open("rb") as f:
                data = f.read()
            return data
        except:
            return data
