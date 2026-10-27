def validasi_nim(nim):
    """NIM harus string 7-10 digit angka."""
    return isinstance(nim, str) and nim.isdigit() and 7 <= len(nim) <= 10


def validasi_mahasiswa(mhs):
    """Kembalikan list pesan error (kosong jika valid)."""
    errors = []
    if not validasi_nim(mhs.nim):
        errors.append("NIM harus 7-10 digit angka")
    if not mhs.nama or not mhs.nama.strip():
        errors.append("Nama tidak boleh kosong")
    if not mhs.prodi:
        errors.append("Prodi tidak boleh kosong")
    if not isinstance(mhs.angkatan, int) or not 2000 <= mhs.angkatan <= 2100:
        errors.append("Angkatan tidak valid")
    return errors
