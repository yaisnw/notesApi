from sqlmodel import Field, SQLModel 


class Note(SQLModel, table=True):
    model_config = {"from_attributes": True}
    id: int | None = Field(default=None, primary_key=True)
    title: str
    content: str


class NoteUpdate(SQLModel):
    title: str | None = None
    content: str | None = None