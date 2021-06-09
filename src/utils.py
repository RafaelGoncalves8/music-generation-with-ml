import numpy as np
import music21 as m21


def get_vocabulary(data):
    notes = set([])
    for e in data:
        notes.add(e)
    pitchnames = sorted(notes)
    # create a dictionary to map pitches to integers
    return dict((note, number) for number, note in enumerate(pitchnames))


def tokenize(seq, vocabulary):
    tokens = []
    for e in seq:
        tokens.append(vocabulary[e])
    return tokens


def detokenize(tokens, vocabulary)
    vocabulary_rev = vocabulary.update(dict((vocabulary[k], k) for k in vocabulary))
    seq = []
    for e in tokens:
        seq.append(vocabulary_rev[e])
    return seq


def load_songs(dataset_path, max_songs=None):
  songs = []
  for path, subdirs, files in os.walk(dataset_path):
    if max_files == None:
        max_files = len(files)
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


def stream_to_note_array(stream):
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
    return np.array(notes)
