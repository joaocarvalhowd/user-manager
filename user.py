from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class User():
    def __init__(self, fullname, nickname, role, access_level, last_access):
        self.fullname = fullname
        self.nickname = nickname
        self.role = role
        self.access_level = access_level
        self.last_access = last_access

    fullname: str
    nickname: str
    role: str
    access_level: str
    last_access: str
