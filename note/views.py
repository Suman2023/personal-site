from django.shortcuts import render, HttpResponse
from note.models import Note


# Create your views here.
def index(request):
    print("called index")
    start = int(request.GET.get("start", 0))
    if start < 0:
        start = 0
    end = start + 10
    all_notes = Note.objects.all()[start : end + 1]
    print(all_notes)
    show_next = False
    if len(all_notes) > 10:
        show_next = True
    context = {
        "notes": all_notes[:10],
        "start": start,
        "end": end,
        "show_prev": True if start != 0 else False,
        "show_next": show_next,
    }
    return render(request, "notes_base.html", context=context, status=200)


def add_note(request):
    note = request.POST.get("note")
    new_note = None
    note_error = None
    try:
        if len(note) < 1:
            raise ValueError("Length must be greater than 1")
        new_note = Note.objects.create(title=note)
    except Exception as e:
        print(e)
        note_error = f"Something went Wrong: {str(e)}"
    context = {"note": new_note, "error": note_error}
    # if note_error:
    #     return render(request, "note.html", context)
    return get_notes(request, error=note_error)


def get_notes(request, error=None):
    print("get_notes")
    start = int(request.GET.get("start", 0))
    if start < 0:
        start = 0
    end = start + 10
    all_notes = Note.objects.all()[start : end + 1]
    show_next = False
    if len(all_notes) > 10:
        show_next = True
        all_notes = all_notes[:10]
    context = {
        "notes": all_notes,
        "start": start,
        "end": end,
        "show_prev": True if start != 0 else False,
        "show_next": show_next,
        "error": error,
    }
    print(context)
    return render(
        request,
        "all_notes.html",
        context=context,
        status=200 if all_notes or start == 0 else 204,
    )


def get_note(request, id):
    note_error = None
    note = Note.objects.filter(id=id).first()
    if not note:
        note_error = f"Note not found for {id=}"
    context = {"note": note, "error": note_error}
    return render(request, "note.html", context)


def delete_note(request, id):
    print("delete_note")
    Note.objects.filter(id=id).delete()
    return get_notes(request)
