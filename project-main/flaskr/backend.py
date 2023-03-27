from google.cloud import storage
import hashlib
import json


class Backend:
    """Creates a backend object.

    Attributes:
        content_bucket_name: Name of the bucket that holds the content
        password_bucket_name: Name of the bucket that holds the passwords
        storage_client: Allows you to interact with blobs and data
        content_bucket_object: A bucket object for "content_wiki"
        password_bucket_object: A bucket object for "hannahmontana"
    """

    def __init__(self, storage_client=storage.Client()):
        """ Initializes the instance"""
        self.content_bucket_name = "content_wiki"
        self.password_bucket_name = "hannahmontana"
        self.storage_client = storage_client
        self.content_bucket_object = self.storage_client.bucket(
            self.content_bucket_name)
        self.password_bucket_object = self.storage_client.bucket(
            self.password_bucket_name)

    def get_wiki_page(self, name):
        """ Gets an uploaded page from the content bucket. """
        blob = self.content_bucket_object.blob(name)
        with blob.open("r") as read_file:
            read_blob = read_file.read()
        return read_blob

    def get_all_page_names(self):
        """ Gets the names of all pages from the content bucket. """
        page_names = self.storage_client.list_blobs(self.content_bucket_name)
        page_names_list = []
        for blob in page_names:
            page_names_list.append(blob.name)
        return page_names_list

    def upload(self, source_file_name, file, bucket_name="content_wiki"):
        """Uploads a File (photo) with a given name."""
        blob_name = source_file_name
        blob = self.content_bucket_object.blob(blob_name)
        blob.upload_from_file(file)

    def sign_up(self, _password, _name):
        ''' Will create a blob inside the bucket if it doesn't exist and has the password into said blob'''
        print("IN BACKEND")
        print(_name, _password)
        pass_hash = hashlib.sha256(_password.encode())
        bucket = self.storage_client.bucket("hannahmontana")
        if bucket.get_blob(str(_name)) is not None:
            return False
        blob = bucket.blob(str(_name))
        with blob.open("w") as blob_open:
            blob_open.write(pass_hash.hexdigest())
        return True

    def sign_in(self, _password, _name):
        ''' Will check to see if _usernames blob already exists, if it does, it checks password, if it doesn't, it throws an error'''
        bucket = self.storage_client.bucket("hannahmontana")
        pass_hash = hashlib.sha256(_password.encode())
        if bucket.get_blob(str(_name)) is not None:
            blob = bucket.blob(str(_name))
            with blob.open('r') as blob_open:
                if blob_open.read() != pass_hash.hexdigest():
                    return False
        else:
            return False
        return True

    def get_image(self, image):
        """ Gets an image from the content bucket. """
        blob = self.content_bucket_object.blob(image)
        with blob.open("rb") as temp_image:
            read_image = temp_image.read()
        return read_image
