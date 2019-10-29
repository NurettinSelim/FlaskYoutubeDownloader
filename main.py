
#Kullanılacak Modüller
from flask import Flask,render_template,request,redirect,send_from_directory,abort
from pytube import YouTube

app = Flask(__name__)

#Sorun çıkartan karakterler dosya adından silen foksiyon
def temizle(kod): 
    kod = kod.replace("|","")
    kod = kod.replace(".","")
    kod = kod.replace('"',"")
    kod = kod[:-3]
    kod = kod + ".mp4"
    return kod


#Ana Sayfa
@app.route("/",methods=["POST","GET"])
def index():
    
    if request.method == "POST":    
        link=request.form.get("link")
        global kod
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
    video_name = YouTube("http://youtube.com/watch?v="+id).title        
    video.streams.filter(progressive=True,file_extension='mp4').first().download("FlaskYoutubeDownloader/download/")
    

    return render_template("start.html",title = video_name)

@app.route("/file/<string:name>")
def file(name):
    print(temizle(name))
    return send_from_directory("FlaskYoutubeDownloader/download/",temizle(name),as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True) 