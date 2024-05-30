"""
main function text
"""
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import MySQLdb

app = FastAPI()

db_config = {
    # 'host': '',
    # 'user': '',
    # 'passwd': '',
    'db': 'fastapi_db'
}

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

app.mount(
    "/static",
    StaticFiles(
        directory=os.path.join(
            parent_dir,
            "static")),
    name="static")

"""
Haal parent directory op
"""
@app.get("/", response_class=HTMLResponse)
async def get_html():
    with open(os.path.join(parent_dir, "index.html"), "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

"""
Haal data folder op,
hier wordt backend in gerund
"""
@app.get("/data")
async def get_data():
    db = MySQLdb.connect(**db_config)

    cursor = db.cursor()
    cursor.execute("SELECT message FROM messages LIMIT 1")

    result = cursor.fetchone()

    db.close()

    return {"message": result[0] if result else "No message found"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="192.168.56.0", port=8000)