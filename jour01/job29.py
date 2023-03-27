print("JOB 29 ###################################################################################################################")

def arrondir_notes(notes):
    multiple = 5
    distance = 3
    notes_arrondies = []
    for note in notes:
        if ((multiple - note % multiple) < distance) and (note >= 40):
            notes_arrondies.append(note + 5 - note % 5)
        else:
            notes_arrondies.append(note)
    return notes_arrondies
    
notes_arrondies = print(arrondir_notes([83, 82, 58, 33, 79, 68]))