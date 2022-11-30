from flask import Flask, render_template, url_for, request
import os
from dotenv import load_dotenv
import requests
import smtplib

load_dotenv('important.env')
app=Flask(__name__)


@app.route("/")
def main_page():
    blog_url=os.getenv("API")
    response=requests.get(blog_url)
    posts = response.json()
    return render_template("index.html", posts=posts)

@app.route("/about.html")
def about():
    return render_template("about.html")

@app.route("/contact.html")
def contact():
    return render_template("contact.html")

@app.route("/post/<int:post_id>")
def post(post_id):
    blog_url = os.getenv("API")
    response=requests.get(blog_url)
    posts=response.json()

    for blog_post in posts:

        if blog_post["id"] == post_id:
            post_title = blog_post["title"]
            post_subtitle = blog_post["subtitle"]
            post_body = blog_post["body"]
            date_posted = blog_post["date"]
            return render_template("post.html", post_title=post_title, post_subtitle=post_subtitle, post_body=post_body, date_posted=date_posted)
        
        else:
            return render_template("not_found.html")

@app.route("/form-entry", methods=["GET","POST"])
def receive_data():

    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone_num = request.form['phone']
        msg = request.form['message']

        print(name)
        print(email)
        print(phone_num)
        print(msg)

        if len(name) and len(email) and len(msg) !=0:
            send_mail=os.getenv("MY_EMAIL")
            send_password=os.getenv("PASSWORD")
            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=send_mail, password=send_password)
                connection.sendmail(
                    from_addr=send_mail,
                    to_addrs=send_mail,
                    msg=f"Subject: Client Message.\n\nName:{name}\nEmail:{email}\nPhone:{phone_num}\nMessage:{msg}"

                )
        return render_template("contact.html", msg_sent=True)
    
    return render_template("contact.html", msg_sent=False)


# auto run server when script runs
if __name__ == "__main__":
    app.run(debug=True)

