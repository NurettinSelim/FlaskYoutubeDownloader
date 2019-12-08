
#Kullanılacak Modüller
from flask import Flask,render_template,request,redirect,send_from_directory,abort
from pytube import YouTube
import os

app = Flask(__name__)

#Sorun çıkartan karakterler dosya adından silen foksiyon
def temizle3(kod): 
    kod = kod.replace("|","")
    kod = kod.replace(".","")
    kod = kod.replace('"',"")
    kod = kod.replace(':',"")
    kod = kod.replace('#',"")
    kod = kod[:-3]
    kod = kod + ".mp3"
    return kod
def temizle4(kod): 
    kod = kod.replace("|","")
    kod = kod.replace(".","")
    kod = kod.replace('"',"")
    kod = kod.replace(':',"")
    kod = kod.replace('#',"")
    kod = kod[:-3]
    kod = kod + ".mp4"
    return kod


#Ana Sayfa
@app.route("/",methods=["POST","GET"])
def index():
    
    if request.method == "POST":    
        link=request.form.get("link")
        try:
            #Linki parçalayarak id kısmını alıyor
            kod = link[link.index("=")+1:]
        except ValueError:
            return render_template("refresh.html")
            
        return redirect("/download/"+ kod)
    else:    
        return render_template("home.html")

@app.route("/download/<string:id>")
def download(id):    
    video = YouTube("http://youtube.com/watch?v="+id)
    video_name = video.title 
    video_name = video_name+".mp4"       
    video.streams.filter(only_audio=True,file_extension='mp4').first().download("down/")

    name4= temizle4(video_name)
    name3= temizle3(video_name)

    code= """ ffmpeg -i "D:\Python Projeleri\FlaskYoutubeDownloader\down\{}" -f mp3 -ab 128000 -vn "D:\Python Projeleri\FlaskYoutubeDownloader\down\{}" """.format(name4,name3)
    print(code)
    os.system(code)
    return render_template("start.html",title = video_name[:-3])

@app.route("/file/<string:name>")
def file(name):
    print(temizle3(name))
    return send_from_directory("down/",temizle3(name),as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True) 