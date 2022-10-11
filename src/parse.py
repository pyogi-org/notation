from dataclasses import dataclass
from typing import Iterator, Literal

import music21
from music21.stream import Score

# Only including full steps from
# https://github.com/cuthbertLab/music21/blob/1025c6cc5703e27ad5eb924c0098e11e3dd04f3b/music21/pitch.py#L93-L107
Accidental = Literal[
    "natural",
    "sharp",
    "double-sharp",
    "triple-sharp",
    "quadruple-sharp",
    "flat",
    "double-flat",
    "triple-flat",
    "quadruple-flat",
]


@dataclass
class Note:
    time: float
    note: int  # note % 7 == 0 is C
    accidental: Accidental
    part: int


# TODO: Sort deterministically so can test it
def parse(filename: str) -> Iterator[Note]:
    score = music21.converter.parse(filename)
    if isinstance(score, Score):
        part_num = 0
        for part in score.parts:
            for note in part.flat.notes:
                time = float(note.offset)
                for pitch in note.pitches:
                    note = pitch.diatonicNoteNum - 1
                    accidental = (
                        pitch.accidental.name if pitch.accidental else "natural"
                    )
                    # Convert flats to sharps
                    # TODO: Check correct and handle doubles
                    if "flat" in accidental:
                        note -= 1
                        accidental = "sharp"
                    # TODO: Handle doubles; this might be wrong
                    if "sharp" in accidental:
                        accidental = "sharp"
                    yield Note(
                        time=time,
                        note=note,
                        accidental=accidental,
                        part=part_num,
                    )
            part_num += 1
