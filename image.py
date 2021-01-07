import datetime
import logging
from os import environ

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

#fiero - A modern and simplest convenient ORM package in Python
from fireo.models import Model
from fireo import fields
from google.cloud import storage

from debugging.logger import CustomLogger

# Use the application default credentials
CLOUD_STORAGE_BUCKET = environ.get("CLOUD_STORAGE_BUCKET")
storageClient = storage.Client()

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {"projectId": environ.get("PROJECT_ID"), })

logger = logging.getLogger("logger")
db = firestore.client()


class Picture(Model):
    blobName = fields.TextField()
    userId = fields.TextField()
    imageId = fields.TextField()
    dateAdded = fields.DateTime()
    fileName = fields.TextField()
    productNumber = fields.TextField()

    def __init__(self, imageId="", fileName="", blobName="", userId="", productNumber=""):
        self.imageId = imageId
        self.dateAdded = datetime.datetime.now()
        self.fileName = fileName
        self.blobName = blobName
        self.userId = userId
        self.productNumber = productNumber

    def uploadImage(self, imageObject, userId):
        try:
            bucket = storageClient.get_bucket(CLOUD_STORAGE_BUCKET)
            blob = bucket.blob(userId + "_" + self.fileName)
            blob.upload_from_string(
                imageObject.read(), content_type=imageObject.content_type
            )
            self.blobName = blob.name
            self.userId = userId
            logger.info("Uploaded image to Google Cloud")
            db.collection("Images").document(self.imageId).set(self.__dict__)
            logger.info(
                "Successfully stored document with image_id: {} in Firestore".format(
                    # Store image ID
                    self.imageId
                )
            )
            return True
        except Exception as e:
            logger.error(str(e))
            return False

    def deleteImage(self, imageId, userId):
        image = db.collection("ImagesCollection").document(imageId)
        bucket = storageClient.get_bucket(CLOUD_STORAGE_BUCKET)
        dictionaryOfImages = image.get().to_dict()

        # Check permissions
        if dictionaryOfImages["user_id"] != user_id:
            logger.error("This action is not allowed for the current user")
            return False
        try:
            bucket.delete_blob(image_dict["blobName"])
            logger.debug("Deleted Blob: {}".format(
                dictionaryOfImages["blobName"]))
            image.delete()
            logger.debug(
                "Firestore deleted imageId: {}".format(
                    dictionaryOfImages["imageId"]
                )
            )
            return True
        except Exception as e:
            logger.debug(str(e))
            logger.error("Cannot find blob in the bucket")
            return False

    def bulkDelete(self, userId):
        images = db.collection("Images").stream()
        count = 0
        try:
            for image in images:
                isDeleted = self.deleteImage(image.get("imageId"), userId)
                if isDeleted:
                    db.collection("Images").document(
                        image.get("imageId")).delete()
                    count += 1
                    logger.debug("Deleted {} images".format(count))
            return True
        except Exception as e:
            logger.error("Bulk-Delete Exception: {}".format(str(e)))
            return False
