"""Soal 3 - Program utama yang memakai utilitas_akademik."""
from utilitas_akademik import hitung_ipk, konversi_nilai_huruf, generate_transkrip


def main():
    mk = [
        {"kode": "IF101", "nama": "Algoritma Pemrograman", "sks": 3, "nilai": 88},
        {"kode": "IF102", "nama": "Basis Data", "sks": 3, "nilai": 76},
        {"kode": "IF103", "nama": "Jaringan Komputer", "sks": 2, "nilai": 67},
        {"kode": "MK104", "nama": "Statistika", "sks": 2, "nilai": 91},
    ]
    print(generate_transkrip("Siti Aminah", "2024001", mk))
    print("Konversi 79 ->", konversi_nilai_huruf(79))
    print("IPK            :", hitung_ipk(mk))


if __name__ == "__main__":
    main()
