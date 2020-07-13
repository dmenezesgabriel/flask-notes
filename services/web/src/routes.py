import os
from werkzeug.utils import secure_filename
from flask import (send_from_directory, request)


def setup_routes(app):
    @app.route('/static/<path:filename>')
    def static_files(filename):
        return send_from_directory(app.config['STATIC_FOLDER'], filename)

    @app.route('/media/<path:filename>')
    def media_files(filename):
        return send_from_directory(app.config['MEDIA_FOLDER'], filename)

    @app.route("/upload", methods=["GET", "POST"])
    def upload_file():
        if request.method == "POST":
            file = request.files["file"]
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["MEDIA_FOLDER"], filename))
        return """
        <!doctype html>
        <title>upload new File</title>
        <form action="" method=post enctype=multipart/form-data>
        <p><input type=file name=file><input type=submit value=Upload>
        </form>
        """
