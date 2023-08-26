from django.urls import path
from note.views import index,  add_note, get_notes, get_note, delete_note

urlpatterns = [
    path("", index, name="note_base"),
    path("all", get_notes, name="get_notes"),
    path("add", add_note, name="add_note"),
    path("note/<int:id>", get_note, name="get_note"),
    path("delete/<int:id>", delete_note, name="delete_note"),
]
