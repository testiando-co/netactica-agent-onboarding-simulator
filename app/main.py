import sqlite3

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.database import Base, engine
from app.routers import api, web

Base.metadata.create_all(bind=engine)

# Migrate: add email column if it doesn't exist yet
try:
    conn = sqlite3.connect("./data/phone_ti.db")
    cursor = conn.execute("PRAGMA table_info(phone_ti)")
    columns = [row[1] for row in cursor.fetchall()]
    if "email" not in columns:
        conn.execute("ALTER TABLE phone_ti ADD COLUMN email TEXT")
        conn.commit()
    conn.close()
except Exception:
    pass

app = FastAPI(title="Phone TI Lookup")

app.add_middleware(SessionMiddleware, secret_key="phone-ti-secret-key")

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(api.router)
app.include_router(web.router)
