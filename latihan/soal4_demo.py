"""Demo CRUD package sistem_informasi."""
from sistem_informasi.model import Mahasiswa
from sistem_informasi.service import MahasiswaService

if __name__ == "__main__":
    svc = MahasiswaService()
    svc.tambah(Mahasiswa("2024001", "Siti Aminah", "Teknik Informatika", 2024))
    svc.tambah(Mahasiswa("2024002", "Budi Santoso", "Sistem Informasi", 2024))
    print("Create/Read:", [m.nama for m in svc.semua()])

    svc.ubah("2024002", prodi="Manajemen Informatika")
    print("Update     :", svc.ambil("2024002"))

    svc.hapus("2024001")
    print("Delete     :", [m.nim for m in svc.semua()])

    for aksi in (lambda: svc.ambil("9999999"),
                 lambda: svc.tambah(Mahasiswa("12", "", "TI", 1999))):
        try:
            aksi()
        except (KeyError, ValueError) as e:
            print("Error      :", e)
