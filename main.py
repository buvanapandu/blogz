from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://build-a-blog:beproductive@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO']=True
db=SQLAlchemy(app) # db is instance of
app.secret_key="abcdefgh" 


class Blog(db.Model):

    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(120))
    body=db.Column(db.Text(255))

    def __init__(self, title, body):    
            self.title=title
            self.body=body


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    title_error=""
    body_error=""
    title = ""
    body = ""
    
    if request.method=='POST':
        title=request.form['title']
        body=request.form['body']
        
        if title=="" and body=="":
            title_error="Please fill in the title"
            body_error="Please fill in the body"
            return render_template("newpost.html", title_error=title_error, body_error=body_error)
        if(title == ""):
            title_error="Please fill in the title"
            return render_template("newpost.html", title_error=title_error, body_error=body_error, body=body)
        if(body == ""):
            body_error="Please fill in the body"
            return render_template("newpost.html", title_error=title_error, body_error=body_error, title=title)
        
        else: 
            
            new_blog = Blog(title, body)
            db.session.add(new_blog)
            db.session.commit()
            blogs = Blog.query.filter_by(title=title).all()
            return render_template('blog.html', blogs=blogs)
    else:
        return render_template('newpost.html')
    
@app.route('/', methods=['POST', 'GET'])
def index():
    
    blogs = Blog.query.filter_by().all()   
    return render_template('index.html', blogs=blogs) 

@app.route('/blog', methods=['GET'])
def main_blog():
    blog_id=request.args.get('id')
    blogs=Blog.query.filter_by(id=blog_id)
    return render_template('blog.html', blogs=blogs)

if __name__ == '__main__':
    app.run()
