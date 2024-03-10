from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import requests
from clean_it import clean_it

from authlib.integrations.flask_client import OAuth

app = Flask(__name__)

# Connect to PostgreSQL
conn=psycopg2.connect(
host="dpg-cnm94so21fec7395uong-a", database="dhp2024_tq84", user="dhp2024_tq84_user", password="QSkx41pWFZslweIaslsdwtFhk97ftivs")
cur=conn.cursor()

# Create the table if it doesn't exist (adjust columns as needed)
cur.execute("""CREATE TABLE IF NOT EXISTS News_Content (id serial primary key,
        URL varchar,
        Given_text text,
        Words_count int,
        Sentence_count int,
        Stop_words_count int,
        UPOS_tags_info text,
        Most_frequent_words text
        )
""")
conn.commit()

#google Authentication---------------------------------------------------------------------------------------------------------------------------------------------------

app.secret_key = b'1122'
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='http://1057527378199-co9tqua4oj17e0s2rsbhbabpth2t2s4k.apps.googleusercontent.com',
    client_secret='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',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    refresh_token_params=None,
    redirect_uri='https://editnpress.onrender.com/login',
    client_kwargs={'scope': 'openid profile email'},
)

@app.route('/Glogin')
def login():
    redirect_uri = url_for('login_page', _external=True)
    
    return google.authorize_redirect(redirect_uri)


"""---------------------------------------------------------------------------------------------------------------------------------------------------------"""

# Route for home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling form submission
@app.route('/submit', methods=['POST', 'GET'])
def submit():
    if request.method == 'POST':
        url = request.form['url']
    # checking validity of given URL
    if url.startswith("https://indianexpress.com/article/") and requests.head(url).status_code==200:
        #calling the function for cleaning , from clean_it module
        url,clean_text_result,words_count,sent_count,count_stop_words,upos_text,most_freq_words=clean_it(url)
        cur.execute("""INSERT INTO News_Content(
        URL,
        Given_text,
        Words_count,
        Sentence_count,
        Stop_words_count,
        UPOS_tags_info,
        Most_frequent_words) VALUES (%s,%s,%s,%s,%s,%s,%s) on conflict do nothing""",(url,clean_text_result,words_count,sent_count,count_stop_words,upos_text,most_freq_words))
        conn.commit()
        return redirect(url_for('result'))
    #handling the errors while giving invalid url
    else:
        text='Please enter a valid URL from IndianExpress website!'
        return render_template('index.html',text=text)

# Route for displaying processed text
@app.route('/result')
def result():
        #showing only the last entered data in the tale, given by user at that time
    cur.execute("SELECT * FROM News_Content ORDER BY id DESC LIMIT 1")
    article = cur.fetchall() 
    cur.execute("SELECT URL FROM News_Content ORDER BY id DESC LIMIT 1")
    url=cur.fetchall()
    return render_template('result.html', article=article,url=url)
#route for displaying relevent plain text of the article without any other unnecessory information
@app.route('/plain_text')
def plain_text():
    cur.execute("SELECT Given_text FROM News_Content ORDER BY id DESC LIMIT 1")
    cleantext = cur.fetchall() 
    return render_template('plain_text.html', news_text=cleantext)
#route for Admin login page
@app.route('/login', methods=['POST','GET'])
def login():
    user=''
    paswd=''
    mesg=''
    if request.method=='POST':
        user=request.form['Username']
        paswd=request.form['Password']
    if user=='admin@example.com' and paswd=='12345': #pre defined user credentials
        return render_template('admin.html')
    else:
        mesg='Wrong ID or Password'
        return render_template('login.html',mesg=mesg) #showing appropriate message for wrong id or password
#route for admin login portal
@app.route('/login_page')
def login_page():
    return render_template('login.html')
#route for displaying full data history    
@app.route('/view_history')
def view_history():
    cur.execute("SELECT * FROM News_Content")
    full_history = cur.fetchall() 
    return render_template('history.html', history=full_history)
#for admin to have the autherity to clear the table data
@app.route('/clear_history')
def clear_history():
    mesg='History is cleared!'
    cur.execute("Delete from News_Content")
    conn.commit()
    cur.execute('ALTER SEQUENCE News_Content_id_seq RESTART WITH 1') #this will restart the id column with 1
    conn.commit()
    return render_template('history.html',mesg=mesg)

if __name__ == '__main__':
    app.run(debug=True)


