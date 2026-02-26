from flask import Flask, render_template , request , url_for , redirect
import requests
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidad.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

def news():
    API_KEY = "df276925f1cc4a07b771dbb69b872b61"
    url = (
        "https://newsapi.org/v2/everything?"
        "q=cambio climático OR medio ambiente OR calentamiento global OR contaminación OR energías renovables"
        "&language=es"
        "&sortBy=relevancy"
        "&pageSize=20"
        "&apiKey=" + API_KEY
    )
    data = requests.get(url).json()
    noticias = data.get("articles", [])
    lista_noticias = []
    for noticia in noticias:
        lista_noticias.append({
            "title": noticia["title"],
            "description": noticia["description"],
            "url": noticia["url"]
        })
    return lista_noticias

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/informate")
def informate():
    noticias = news()
    return render_template("informate.html",noticias = noticias)

@app.route("/comunidad",methods=["GET", "POST"] )
def comunidad():
    if request.method == "POST":
        name = request.form["name"]
        categoria = request.form["categoria"]
        title = request.form["title"]
        content = request.form.get("content")
        new_post = Post(
            name=name,
            categoria=categoria,
            title=title,
            content=content
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("comunidad"))
    posts = Post.query.all()
    return render_template("comunidad.html", posts = posts )


@app.route("/donar")
def donar():
    return render_template("donar.html")


if __name__ == "__main__":
    app.run(debug=True)