from dataclasses import dataclass, asdict


@dataclass
class Mahasiswa:
    nim: str
    nama: str
    prodi: str
    angkatan: int

    def to_dict(self):
        return asdict(self)
