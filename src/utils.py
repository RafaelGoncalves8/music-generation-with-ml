import os
import music21 as m21


def get_vocabulary(data):
    notes = set([])
    for seq in data:
        for e in seq:
            notes.add(e)
    pitchnames = sorted(notes)
    # create a dictionary to map pitches to integers
    return dict((note, number) for number, note in enumerate(pitchnames))


def tokenize(seq, vocabulary):
    tokens = []
    for e in seq:
        tokens.append(vocabulary[e])
    return tokens


def detokenize(tokens, vocabulary):
    vocabulary_rev = dict((vocabulary[k], k) for k in vocabulary)
    seq = []
    for e in tokens:
        seq.append(vocabulary_rev[e])
    return seq


def load_songs(dataset_path, max_songs=None):
  songs = []
  for path, subdirs, files in os.walk(dataset_path):
    if max_songs == None:
        max_songs = len(files)
    for file in [f for f in files if f[-3:] == "mid"][:max_songs]:
        song = m21.converter.parse(os.path.join(path, file))
        song_measured = song.makeNotation()
        songs.append(song_measured)

  return songs


def transpose_to_CmajAmin(song):
  # pick music tone
  parts = song.getElementsByClass(m21.stream.Part)
  measures = parts[0].getElementsByClass(m21.stream.Measure)
  key = measures[0][4]

  # estimate tone
  if not isinstance(key, m21.key.Key):
    key = song.analyze("key")

  # calculate interval
  if (key.mode == "major"):
    interval = m21.interval.Interval(key.tonic, m21.pitch.Pitch("C"))
  elif (key.mode == "minor"):
    interval = m21.interval.Interval(key.tonic, m21.pitch.Pitch("A"))

  # transpose to calculated interval
  return song.transpose(interval)


def stream_to_notes(stream):
    notes = []
    parts = m21.instrument.partitionByInstrument(stream)
    if parts:
        notes_to_parse = parts.parts[0].recurse()
    else:
        notes_to_parse = stream.flat.notes
    for element in notes_to_parse:
        if isinstance(element, m21.note.Note):
            notes.append(str(element.pitch))
        elif isinstance(element, m21.chord.Chord):
            notes.append('.'.join(str(n) for n in element.normalOrder))
    return notes


def notes_to_stream(note_array):
    offset = 0
    output_notes = []
    for pattern in note_array:
        # pattern is a chord
        if ('.' in pattern) or pattern.isdigit():
            notes_in_chord = pattern.split('.')
            notes = []
            for current_note in notes_in_chord:
                new_note = m21.note.Note(int(current_note))
                new_note.storedInstrument = m21.instrument.Piano()
                notes.append(new_note)
            new_chord = m21.chord.Chord(notes)
            new_chord.offset = offset
            output_notes.append(new_chord)
        # pattern is a note
        else:
            new_note = m21.note.Note(pattern)
            new_note.offset = offset
            new_note.storedInstrument = m21.instrument.Piano()
            output_notes.append(new_note)
        # increase offset each iteration so that notes do not stack
        offset += 0.5

    midi_stream = m21.stream.Stream(output_notes)

    return midi_stream


def notebook_show(music):
    display(Image(str(music.write('lily.png'))))


def notebook_play(music):
    filename = music.write('mid')
    os.system(f'fluidsynth -ni font.sf2 {filename} -F {filename}\.wav -r 16000 > /dev/null')
    display(Audio(filename + '.wav'))


def create_lilypond_environment():
    environment = m21.environment.UserSettings()
    environment.create()
    environment['lilypondPath'] = '/usr/bin/lilypond'
