"""Soal 3 - Modul utilitas akademik."""

# (batas bawah, huruf, bobot) diurutkan dari tertinggi
SKALA_NILAI = [
    (85, "A", 4.0),
    (80, "A-", 3.7),
    (75, "B+", 3.3),
    (70, "B", 3.0),
    (65, "B-", 2.7),
    (60, "C+", 2.3),
    (55, "C", 2.0),
    (40, "D", 1.0),
    (0, "E", 0.0),
]


def konversi_nilai_huruf(nilai_angka):
    """Konversi nilai 0-100 menjadi (huruf, bobot)."""
    if not 0 <= nilai_angka <= 100:
        raise ValueError("Nilai harus di antara 0 dan 100")
    for batas, huruf, bobot in SKALA_NILAI:
        if nilai_angka >= batas:
            return huruf, bobot


def hitung_ipk(daftar_mk):
    """Hitung IPK = sum(bobot * sks) / sum(sks).

    daftar_mk: list dict {"kode", "nama", "sks", "nilai"} (nilai 0-100).
    """
    total_sks = sum(mk["sks"] for mk in daftar_mk)
    if total_sks == 0:
        return 0.0
    total_mutu = sum(konversi_nilai_huruf(mk["nilai"])[1] * mk["sks"]
                     for mk in daftar_mk)
    return round(total_mutu / total_sks, 2)


def generate_transkrip(nama, nim, daftar_mk):
    """Hasilkan transkrip nilai dalam bentuk string."""
    garis = "=" * 62
    baris = [garis, "TRANSKRIP NILAI".center(62), garis,
             f"Nama : {nama}", f"NIM  : {nim}", "-" * 62,
             f"{'No':<4}{'Kode':<9}{'Mata Kuliah':<26}{'SKS':>4}{'Nilai':>7}{'Huruf':>6}{'Mutu':>6}",
             "-" * 62]
    for i, mk in enumerate(daftar_mk, 1):
        huruf, bobot = konversi_nilai_huruf(mk["nilai"])
        baris.append(f"{i:<4}{mk['kode']:<9}{mk['nama']:<26}{mk['sks']:>4}"
                     f"{mk['nilai']:>7}{huruf:>6}{bobot * mk['sks']:>6.1f}")
    baris += ["-" * 62,
              f"Total SKS : {sum(mk['sks'] for mk in daftar_mk)}",
              f"IPK       : {hitung_ipk(daftar_mk):.2f}", garis]
    return "\n".join(baris)


if __name__ == "__main__":
    assert konversi_nilai_huruf(90) == ("A", 4.0)
    assert konversi_nilai_huruf(72) == ("B", 3.0)
    assert konversi_nilai_huruf(30) == ("E", 0.0)
    contoh = [{"kode": "IF101", "nama": "Algoritma", "sks": 3, "nilai": 88},
              {"kode": "IF102", "nama": "Basis Data", "sks": 3, "nilai": 76}]
    assert hitung_ipk(contoh) == 3.65
    print("Self-test utilitas_akademik lolos.")
