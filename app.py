from flask import Flask, flash, redirect, render_template, request, session, jsonify, url_for, jsonify
from cs50 import SQL
import requests


app = Flask("__name__")

db = SQL("sqlite:///database.db")


@app.route("/")
def index():
    posts = db.execute("SELECT * FROM posts")
    return render_template("index.html", posts=posts)

@app.route("/posts/<post_id>")
def post(post_id):
    # check if post exits
    post = db.execute("SELECT * FROM posts WHERE id = ?", post_id)
    if len(post) == 0:
        return "invalid post"
    
    # load comments
    comments = load_post_comments(post_id)
    # return post info 
    print(post, comments)
    return render_template("post.html", post=post[0], comments=comments)

    

# when a user responds to a comment, you have to check two things, if the main comments eixits and if the sub comments exits

@app.route("/submit_comment", methods=['POST'])
def submit_comment():
    text = request.json['text']
    post_id = request.json['post_id']
    username = request.json['username']

    # do checks, is the post valid
    post_check = db.execute("SELECT * FROM posts WHERE id = ?", post_id)
    if len(post_check) == 0:
        return ""

    # add the comment
    db.execute("INSERT INTO comments (comment_text, username, post_id) VALUES (?,?,?)", text, username, post_id)
    return ""

@app.route("/submit_sub_comment", methods=['POST'])
def submit_sub_comment():
    reply_to_id = request.json['reply_to_id']
    main_comment_id = request.json['main_comment_id']
    
    text = request.json['text']
    username = request.json['username']

    # do checks, 1 check if the main comment is valid, 2 check if the sub comment is valid
    comment_check = db.execute("SELECT * FROM comments WHERE id = ?", main_comment_id)
    if len(comment_check) == 0:
        return ""

    sub_comment_check = db.execute("SELECT * FROM sub_comments WHERE id = ?", reply_to_id)
    if len(sub_comment_check) == 0 and reply_to_id is not None:
        return ""

    # add the sub comment
    db.execute(
        "INSERT INTO sub_comments (comment_text, username, main_comment_id, reply_to_id) VALUES (?,?,?,?)",
        text,username,main_comment_id,reply_to_id)
    return ""


def load_post_comments(post_id):
    # check if posts exits
    check = db.execute("SELECT * FROM posts WHERE id = ?", post_id)
    if len(check) == 0:
        return ""

    # load the comments
    comments = db.execute("SELECT * FROM comments WHERE post_id = ?", post_id)
    return comments

@app.route("/load_sub_comments", methods=['POST'])
def load_sub_comments():
    main_comment_id = request.json['comment_id']
    # check if the comment exits
    check = db.execute("SELECT * FROM comments WHERE id = ?", main_comment_id)
    if len(check) == 0:
        return ""
    
    # now load the sub comments
    sub_comments = db.execute("SELECT * FROM sub_comments WHERE main_comment_id = ?", main_comment_id)
    return jsonify(sub_comments)