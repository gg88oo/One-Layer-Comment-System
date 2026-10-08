# One-Layer Comment System

A Flask comment system where every comment has a single flat list of replies. Any reply can respond to any other reply, and each one shows who it's replying to ("reply to >> josh"), so conversations stay readable without deep nesting.

## How it works

- Posts have comments.
- Each comment has replies, loaded on demand with "show replies".
- Replies are stored in one table. `reply_to_id` points at the reply being answered, or is `NULL` when answering the main comment.
- Only one reply box exists per comment. Clicking "reply" on the comment or on any reply re-aims that box at the right target.

## Tech stack

Python, Flask, SQLite, Jinja2, vanilla JavaScript (`fetch`, async/await)

## Database

| Table | Columns |
|-------|---------|
| posts | id, text, username |
| comments | id, comment_text, post_id, username |
| sub_comments | id, comment_text, main_comment_id, reply_to_id, username |

The "reply to >> name" label comes from a self-join on `sub_comments`:

```sql
SELECT s.id, s.comment_text AS text, s.reply_to_id, s.username,
       r.username AS reply_to_username
FROM sub_comments s
LEFT JOIN sub_comments r ON s.reply_to_id = r.id
WHERE s.main_comment_id = ?
ORDER BY s.id
```

`LEFT JOIN` matters: replies to the main comment have `reply_to_id = NULL`, and a regular join would drop them.

## Routes

| Route | Purpose |
|-------|---------|
| `/` | List all posts |
| `/posts/<id>` | A post with its comments |
| `/submit_comment` | Add a comment (POST, JSON) |
| `/submit_sub_comment` | Add a reply (POST, JSON) |
| `/load_sub_comments` | Return a comment's replies as JSON (POST) |

## Setup

```bash
pip install flask cs50   # or whichever DB helper you use
python create_db.py
flask run
```

## Things I learned

- Jinja runs on the server once, so replies fetched after page load must be built in JavaScript.
- Use `textContent` instead of `innerHTML` for user text so people can't inject HTML.
- One flat list with a "reply to" label is simpler than recursive nesting.

## Possible improvements

- Real-time updates with Flask-SocketIO
- User accounts instead of typed usernames
- Delete and edit for comments