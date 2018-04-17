from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://build-a-blog:beproductive@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO']=True
db=SQLAlchemy(app) # db is instance of
#app.secret_key="abcdefgh" 


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
        
        else: # (not title_error and not body_error):
            #return redirect('/index?title=' + title + '&body=' + body)
            
            new_blog = Blog(title, body)
            db.session.add(new_blog)
            db.session.commit()
            #get_id = request.args.get("id")
            blogs = Blog.query.filter_by(title=title).all()
            return render_template('blog.html', blogs=blogs)
    else:
        return render_template('newpost.html')
    
@app.route('/', methods=['POST', 'GET'])
def index():
    
    blogs = Blog.query.filter_by().all()   
    return render_template('index.html', blogs=blogs) 

@app.route('/blog', methods=['GET'])##postadded
def main_blog():
    blog_id=request.args.get('id')
    blogs=Blog.query.filter_by(id=blog_id)
    return render_template('blog.html', blogs=blogs)


#@app.route('/single', methods=['POST','GET'])    
#def single_entry():
 #   if request.method=='POST':
  #      title=request.form['title']
   #     body=request.form['body']


    #return render_template('list.html') 

#blogs=[]



#@app.route('/index', methods=['GET'])
#def indexList():
    
 #   title=request.args.get('title')
  #  body=request.args.get('body')
   # #new_entry = Blog(title, body)
   # #db.session.add(new_entry)
   # #db.session.commit()
   # get_id = request.args.get('id')
   # blogs = Blog.query.filter_by(id=get_id)
    
    ##return render_template('list.html', blogs=blogs)
    #return render_template('single_entry.html', blogss=blogs)

if __name__ == '__main__':
    app.run()
