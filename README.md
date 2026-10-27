## 👤 IDENTITAS

| | |
|---|---|
| **NAMA** | EKA FEBRYANTO |
| **NPM** | 20241320014 |
| **KELAS** | A1 SISTEM INFORMASI |

---

# Tugas Pertemuan 6 - Pemrograman Python

Repositori ini berisi kumpulan tugas dan latihan pemrograman Python (Soal 1 s.d. Soal 5) yang mencakup struktur data, modularisasi kode, pembuatan paket, serta konsumsi REST API.

---

## Struktur Repositori

```text
├── .gitignore
├── README.md
├── bukti_eksekusi/
│   ├── S1.png                      # Bukti eksekusi Soal 1
│   ├── S2.png                      # Bukti eksekusi Soal 2
│   ├── S3V1.png                    # Bukti eksekusi Soal 3 (utilitas_akademik.py)
│   ├── S3V2.png                    # Bukti eksekusi Soal 3 (main.py)
│   ├── S4.png                      # Bukti eksekusi Soal 4
│   └── S5.png                      # Bukti eksekusi Soal 5
├── latihan/
│   ├── soal1_statistik.py          # Soal 1: Fungsi statistik deskriptif
│   ├── soal2_validasi.py           # Soal 2: Fungsi validasi data berdasarkan schema
│   ├── utilitas_akademik.py        # Soal 3: Modul utilitas transkrip & IPK
│   ├── main.py                     # Soal 3: Program utama pemanggil modul utilitas
│   ├── sistem_informasi/           # Soal 4: Package sistem informasi mahasiswa
│   │   ├── __init__.py
│   │   ├── model/                  # Data class Mahasiswa
│   │   ├── service/                # Layanan CRUD Mahasiswa
│   │   └── utils/                  # Validator NIM, nama, angkatan
│   ├── soal4_demo.py               # Soal 4: Demo CRUD package sistem informasi
│   └── soal5_api.py                # Soal 5: Versi skrip API
└── latihan_api/
    ├── requirements.txt            # Dependensi (requests)
    ├── soal5_api.py                # Soal 5: Program utama API dengan higher-order functions
    └── hasil_analisis.json         # Hasil analisis data JSONPlaceholder
```

---

## Deskripsi Soal

### 1. Soal 1 - Statistik Deskriptif (`soal1_statistik.py`)
Menghitung `mean`, `median`, `modus`, `range`, dan `std_dev` hanya menggunakan Python standard library (`math` dan `statistics`).

### 2. Soal 2 - Validasi Data (`soal2_validasi.py`)
Memvalidasi dictionary data terhadap skema aturan (tipe data, `min`/`max`, `min_length`/`max_length`, `choices`, fungsi validator tambahan `*args`, serta parameter `strict` dan `stop_on_first` pada `**kwargs`).

### 3. Soal 3 - Modul Utilitas Akademik (`utilitas_akademik.py` & `main.py`)
Menyediakan fungsi konversi nilai ke huruf dan bobot, perhitungan IPK tertimbang SKS, serta format pencetakan transkrip nilai akademik mahasiswa.

### 4. Soal 4 - Package Sistem Informasi Mahasiswa (`sistem_informasi/` & `soal4_demo.py`)
Penerapan modular package Python dengan struktur:
- `model`: Representasi data Mahasiswa.
- `utils`: Validasi data mahasiswa (format NIM, nama tidak kosong, batas tahun angkatan).
- `service`: Operasi CRUD (Create, Read, Update, Delete) data mahasiswa dengan penanganan error.

### 5. Soal 5 - Konsumsi REST API & Functional Programming (`latihan_api/soal5_api.py`)
Mengambil data endpoint `/users` dan `/posts` dari JSONPlaceholder menggunakan `requests`, lalu mengolah data dengan:
- `map` dan `lambda` untuk pengayaan data
- `filter` dan `lambda` untuk menyaring judul panjang
- `sorted` dan `lambda` untuk perankingan post
- `functools.reduce` untuk agregasi total kata
Hasil akhir diekspor ke file `hasil_analisis.json`.

---

## Cara Menjalankan

### Menjalankan Soal 1 s.d. 4:
```powershell
cd latihan
python soal1_statistik.py
python soal2_validasi.py
python utilitas_akademik.py
python main.py
python soal4_demo.py
```

### Menjalankan Soal 5:
```powershell
cd latihan_api

# Buat & aktifkan virtual environment (jika belum)
python -m venv .venv
.\.venv\Scripts\activate

# Install dependensi & jalankan
pip install -r requirements.txt
python soal5_api.py
```
