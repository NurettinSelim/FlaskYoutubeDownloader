from flask import Flask, render_template, request, redirect, send_from_directory

import downloader

path = "D:/Python Projeleri/FlaskYoutubeDownloader/downloads/%(title)s.%(ext)s"

app = Flask(__name__)


def save_id(video_id, name, ext):
    with open("id_list.csv", mode="a+") as file:
        file.write(f"{video_id}:{name}.{ext}\n")


def get_name_from_id(video_id):
    with open("id_list.csv", mode="r") as file:
        for num, line in enumerate(file.readlines()):
            if line.startswith(video_id):
                return line.split(':')[1].strip()

    return None


# Main Page
@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        link = request.form.get("link")
        try:
            kod = link[link.index("=") + 1:]
        except ValueError:
            return render_template("refresh.html")

        return redirect("/download/" + kod)
    else:
        return render_template("home.html")


# Download Request Page
@app.route("/download/<string:video_id>")
def download(video_id):
    video = downloader.download_mp3("http://youtube.com/watch?v=" + video_id, path)
    save_id(video["display_id"], video["title"], "mp3")
    return render_template("start.html", id=video["display_id"], title=video["title"])


# Download Page
@app.route("/file/<string:video_id>")
def file(video_id):
    name = get_name_from_id(video_id)
    if name == None:
        return render_template("refresh.html")

    return send_from_directory("downloads/", name, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
