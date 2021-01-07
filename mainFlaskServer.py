import logging
from os import environ

from flask import jsonify, Flask, redirect, render_template, request
from http import HTTPStatus
import uuid

from google.cloud import storage
from image import Picture

CLOUD_STORAGE_BUCKET = environ.get("CLOUD_STORAGE_BUCKET")

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
            isValidImage, errorMesssage = checkFileValidity(fileObject, request)
            if False in isValidImage.values():
                resp = response(HTTPStatus.BAD_REQUEST, errorMesssage[0])
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
    isValid = {"name": True, "type": True, "size": True}
    errorMesssage = []
    ext = fileObject.filename.rsplit(".", 1)[1]


    if fileObject.filename == "" or "." not in fileObject.filename:
        isValid["valid_name"] = False
        errorMesssage.append("File name not valid")
        return isValid, errorMessage

    if ext.upper() not in app.config["ALLOWED_IMAGE_TYPE"]:
        isValid["type"] = False
        errorMesssage.append("File type not allowed")
        return isValid, errorMessage

    if "file_size" in request.cookies:
        file_size = request.cookies["file_size"]
        if int(file_size) <= app.config["MAX_IMAGE_FILESIZE"]:
            isValid["size"] = False
            errorMesssage.append(
                "File size exceeded maximum size of 500,000 bytes")

    return isValid, errorMesssage

def response(status_code, message):
    return {"status_code": status_code, "details": message}


if __name__ == "__main__":
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    logger.info("Running App on http://localhost:8080")
    app.run(host="127.0.0.1", port=8080, debug=False)
