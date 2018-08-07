import json
import time
import posixpath

from tus_client import client
from tus_client.exceptions import TusCommunicationError

from spell.api.exceptions import ClientException, UnauthorizedRequest
from spell.api import base_client, models
from spell.api.utils import url_path_join

USER_DATASET_RESOURCE_URL = "datasets"


class UserDatasetsClient(base_client.BaseClient):
    def __init__(self, token, base_url, version_str, resource_url=USER_DATASET_RESOURCE_URL, **kwargs):
        self.resource_url = resource_url
        upload_url = posixpath.join(base_url, version_str, "datasets", "upload")
        self.tus_client = client.TusClient(upload_url, headers={'Authorization': 'Bearer {}'.format(token)})
        super(UserDatasetsClient, self).__init__(token=token, base_url=base_url, version_str=version_str, **kwargs)

    def new_dataset(self, name):
        """Create a new user dataset

        Keyword arguments:
        name -- the name of this dataset

        Returns:
        a UserDataset object for the created dataset
        """
        payload = {"name": name}
        r = self.request("post", self.resource_url, payload=payload)
        self.check_and_raise(r)
        return self.get_json(r)["user_dataset"]

    def remove_dataset(self, name):
        """Delete the user's dataset

        Keyword arguments:
        name -- the name of the dataset to be deleted

        Returns:
        nothing if successful
        """
        payload = {"name": name}
        r = self.request("delete", self.resource_url, payload=payload)
        self.check_and_raise(r)

    def complete_upload(self, dataset_id):
        """Report upload completion for a dataset

        Keyword arguments:
        dataset_id -- the id of the dataset
        """
        r = self.request("post", url_path_join(self.resource_url, str(dataset_id), "upload_complete"))
        self.check_and_raise(r)

    def upload_file(self, fullpath, dataset_id, dataset_path, q=None, terminate=None, retries=1, retry_delay=30):
        """Upload a dataset file to Spell

        Keyword arguments:
        fullpath -- the local path on disk to the file to upload
        dataset_id -- the id of the dataset
        dataset_path -- the relative path of the file within the root of the dataset
        q -- an optional queue.Queue to which uploaded byte updates will be pushed
        terminate -- an optional threading.Event, which if becomes set, will terminate the upload
        retries -- an optional number of retries to attempt for communication issues before throwing an exception
        retry_delay -- an optional delay to specify for waiting between retry attempts
        """
        try:
            attempts = 0
            while True:
                try:
                    uploader = self.tus_client.uploader(fullpath,
                                                        metadata={
                                                            "path": posixpath.join(str(dataset_id), dataset_path)
                                                        },
                                                        retries=retries, retry_delay=retry_delay)
                    break
                except TusCommunicationError as e:
                    if attempts < retries:
                        attempts += 1
                        time.sleep(30)
                    else:
                        raise e
            if q:
                prev, curr = 0, uploader.offset
                q.put(curr-prev)
            while uploader.offset < uploader.file_size and (not terminate.is_set() if terminate else True):
                uploader.upload_chunk()
                if q:
                    prev, curr = curr, uploader.offset
                    q.put(curr-prev)
        except TusCommunicationError as e:
            # attempt to decode spell exceptions
            if hasattr(e, "response_content") and e.response_content:
                error = None
                try:
                    error = json.loads(e.response_content, object_hook=models.Error.response_dict_to_object)
                    if e.status_code == 401:
                        raise UnauthorizedRequest(msg=str(error))
                    else:
                        raise ClientException(msg=str(error))
                except Exception:
                    pass
                if error:
                    raise ClientException(msg=str(error))
            raise e
