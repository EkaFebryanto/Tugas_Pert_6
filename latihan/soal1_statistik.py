"""Soal 1 - hitung_statistik() hanya dengan standard library."""
import math
import statistics


def hitung_statistik(angka, sampel=True):
    """Hitung mean, median, modus, range, dan standar deviasi.

    Args:
        angka: list angka (int/float), tidak boleh kosong.
        sampel: True -> standar deviasi sampel (n-1); False -> populasi (n).

    Returns:
        dict dengan kunci: mean, median, modus, range, std_dev.
        'modus' berupa list karena bisa lebih dari satu nilai.
    """
    if not angka:
        raise ValueError("List angka tidak boleh kosong")
    if not all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in angka):
        raise TypeError("Semua elemen harus berupa angka")

    n = len(angka)
    if n == 1:
        std = 0.0
    elif sampel:
        std = statistics.stdev(angka)
    else:
        std = statistics.pstdev(angka)

    return {
        "mean": statistics.mean(angka),
        "median": statistics.median(angka),
        "modus": statistics.multimode(angka),
        "range": max(angka) - min(angka),
        "std_dev": round(std, 4),
    }


def _hitung_std_manual(angka):
    """Verifikasi dengan math.sqrt (populasi)."""
    m = sum(angka) / len(angka)
    return math.sqrt(sum((x - m) ** 2 for x in angka) / len(angka))


if __name__ == "__main__":
    data = [70, 85, 85, 90, 60, 75, 90, 100]
    hasil = hitung_statistik(data)
    for k, v in hasil.items():
        print(f"{k:8}: {v}")
    # Uji konsistensi
    assert math.isclose(hitung_statistik(data, sampel=False)["std_dev"],
                        _hitung_std_manual(data), abs_tol=1e-4)
    print("Semua pengujian lolos.")
