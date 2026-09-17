from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
from dotenv import load_dotenv
import os
from sqlmodel import create_engine, SQLModel, Session, select
from src.notesapi.db import Note, NoteUpdate

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/notes")
def upload_note(note: Note):
    new_note = Note(title=note.title, content=note.content)
    with Session(engine) as s:
        s.add(new_note)
        s.commit()
        return new_note.model_dump()


@app.put("/notes/{note_id}")
def update_note(note_id: int, note: NoteUpdate):
    if not note_id:
        raise HTTPException(status_code=400, detail="No note_id provided")
    if not note:
        raise HTTPException(status_code=400, detail="No note provided")
    with Session(engine) as s:
        statement = select(Note).where(Note.id == note_id)
        results = s.exec(statement)
        old_note = results.one()
        if note.title:
            old_note.title = note.title
        if note.content:
            old_note.content = note.content
        s.add(old_note)
        s.commit()
        s.refresh(old_note)
        return old_note.model_dump()


@app.get("/notes/{note_id}")
def get_note(note_id: int):
    with Session(engine) as s:
        statement = select(Note).where(Note.id == note_id)
        note = s.exec(statement).one_or_none()
        if not note:
            raise HTTPException(status_code=404, detail="note doesn't exist")
        return note.model_dump()


@app.get("/notes")
def get_notes():
    with Session(engine) as s:
        statement = select(Note)
        notes = s.exec(statement).all()
        return notes


@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    with Session(engine) as s:
        statement = select(Note).where(Note.id == note_id)
        results = s.exec(statement)
        note = results.one_or_none()
        if not note:
            raise HTTPException(status_code=404, detail="Note doesn't exist")
        s.delete(note)
        s.commit()
        return note.model_dump()
