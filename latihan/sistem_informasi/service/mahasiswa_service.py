from sistem_informasi.model import Mahasiswa
from sistem_informasi.utils import validasi_mahasiswa


class MahasiswaService:
    """CRUD Mahasiswa dengan dictionary {nim: Mahasiswa} sebagai penyimpanan."""

    def __init__(self):
        self._db = {}

    # Create
    def tambah(self, mhs):
        errors = validasi_mahasiswa(mhs)
        if errors:
            raise ValueError("; ".join(errors))
        if mhs.nim in self._db:
            raise KeyError(f"NIM {mhs.nim} sudah terdaftar")
        self._db[mhs.nim] = mhs
        return mhs

    # Read
    def ambil(self, nim):
        try:
            return self._db[nim]
        except KeyError:
            raise KeyError(f"NIM {nim} tidak ditemukan") from None

    def semua(self):
        return list(self._db.values())

    # Update
    def ubah(self, nim, **perubahan):
        mhs = self.ambil(nim)
        for kunci, nilai in perubahan.items():
            if kunci == "nim" or not hasattr(mhs, kunci):
                raise ValueError(f"Field '{kunci}' tidak dapat diubah")
            setattr(mhs, kunci, nilai)
        errors = validasi_mahasiswa(mhs)
        if errors:
            raise ValueError("; ".join(errors))
        return mhs

    # Delete
    def hapus(self, nim):
        self.ambil(nim)
        return self._db.pop(nim)
