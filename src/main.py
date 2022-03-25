from fastapi import FastAPI, Request, Response
import os
import sqlite3

app = FastAPI()
con = sqlite3.connect(':memory:')

# In dev & testing only, include the stacktrace in the response on internal
# server errors
if os.getenv("FASTAPI_ENV") in ["dev", "test"]:
    @app.exception_handler(Exception)
    async def debug_exception_handler(request: Request, exc: Exception):
        import traceback

        return Response(
            status_code=500,
            content="".join(
                traceback.format_exception(
                    etype=type(exc), value=exc, tb=exc.__traceback__
                )
            )
        )

@app.on_event("startup")
async def startup_event():
    """Creates an in-memory database with a user table, and populate it with
    one account"""
    cur = con.cursor()
    cur.execute('''CREATE TABLE users (email text, password text)''')
    cur.execute('''INSERT INTO users VALUES ('me@me.com', '123456')''')
    con.commit()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/user")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    if item_id > 8:
        item_id = None
    result = item_id / item_id-10

    return {"item_id": item_id, "q": q, "result": result}

@app.get("/login")
async def login(email: str, password: str):
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE email = '%s' and password = '%s'" % (email, password))
    return cur.fetchone() is not None

@app.get("/logout")
async def root(email: str):
    return {"message": "Logged out %s!" % email}
