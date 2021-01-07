import logging
from os import environ

from flask import jsonify, Flask, redirect, render_template, request
from http import HTTPStatus
import uuid

from google.cloud import storage
from image import Picture

CLOUD_STORAGE_BUCKET = environ.get("CLOUD_STORAGE_BUCKET")
storage_client = storage.Client()

app = Flask(__name__)
app.config["MAX_IMAGE_FILESIZE"] = 16 * 1024 * 1024  # 16 MB
app.config["ALLOWED_IMAGE_TYPE"] = ["JPEG", "JPG", "PNG", "GIF"]

logger = logging.getLogger("logger")


@app.route("/upload", methods=["POST"])
def uploadImage():
    userId = request.form.get("userId")
    if request.files.getlist("images"):
        files = request.files.getlist("images")
        for fileObject in files:
            isValidImage, error_msg = checkFileValidity(fileObject, request)
            if False in isValidImage.values():
                resp = response(HTTPStatus.BAD_REQUEST, error_msg[0])
                return jsonify(resp), HTTPStatus.BAD_REQUEST
            image = Picture(str(uuid.uuid4()), fileObject.filename)
            uploaded = image.uploadImage(fileObject, userId)
    if uploaded:
        resp = response(
            HTTPStatus.CREATED, "Successfully uploaded {} images".format(
                len(files))
        )
        return jsonify(resp), HTTPStatus.CREATED
    else:
        resp = (
            response(HTTPStatus.NO_CONTENT, "Could not upload image"),
            HTTPStatus.NO_CONTENT,
        )
        return jsonify(resp), HTTPStatus.NO_CONTENT


@app.route("/delete", methods=["DELETE"])
def deleteImage():
    userId = request.form.get("userId")
    if request.form.get("imageId"):
        fileName = request.form.get("imageId")
        deleted = Picture().deleteImage(fileName, userId)
    elif request.args.get("bulk"):
        deleted = Picture().bulkDelete(userId)
    else:
        resp = response(
            HTTPStatus.BAD_REQUEST,
            "Image id not provided, nor bulk_delete option was not selected",
        )
        return jsonify(resp), HTTPStatus.BAD_REQUEST

    if deleted:
        resp = response(HTTPStatus.MOVED_PERMANENTLY,
                        "Successfully deleted image(s)")
        return jsonify(resp), HTTPStatus.MOVED_PERMANENTLY
    resp = response(HTTPStatus.INTERNAL_SERVER_ERROR, "Could not delete image")
    return jsonify(resp), HTTPStatus.INTERNAL_SERVER_ERROR


def checkFileValidity(fileObject, request):
    # Private helper function to validate file type, file name and file size
    isValid = {"name": True, "type": True, "size": True}
    error_msg = []
    ext = fileObject.filename.rsplit(".", 1)[1]

    # File Name Check
    if fileObject.filename == "" or "." not in fileObject.filename:
        isValid["valid_name"] = False
        error_msg.append("File name not valid")
        return isValid, error_msg

    # File Type Check (only images/gifs are allowed)
    if ext.upper() not in app.config["ALLOWED_IMAGE_TYPE"]:
        isValid["type"] = False
        error_msg.append("File type not allowed")
        return isValid, error_msg

    # File Size Check, if size exceeds, do not upload
    if "file_size" in request.cookies:
        file_size = request.cookies["file_size"]
        if int(file_size) <= app.config["MAX_IMAGE_FILESIZE"]:
            isValid["size"] = False
            error_msg.append(
                "File size exceeded maximum size of 500,000 bytes")

    return isValid, error_msg

def response(status_code, message):
    return {"status_code": status_code, "details": message}


if __name__ == "__main__":
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    logger.info("Running App on http://localhost:8080")
    app.run(host="127.0.0.1", port=8080, debug=True)
