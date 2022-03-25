from dataclasses import dataclass


@dataclass
class URLData:
    url: str
    content: bytes = ""
    content_type: str = ""
    encoding: str = ""
