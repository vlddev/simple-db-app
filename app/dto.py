from dataclasses import dataclass

@dataclass
class BookDto:
    id: int
    title: str
    publish_date: str
    lang: str
    series: str
    note: str

@dataclass
class RecordingDto:
    id: int
    title: str
    score:float
    hasContract: bool
    # artists:list[ArtistDto]

@dataclass
class MessageDto:
    mtype: str
    message: str
