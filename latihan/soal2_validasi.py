"""Soal 2 - validasi_data() dengan schema, *args, dan **kwargs."""


def validasi_data(data, schema, *args, **kwargs):
    """Validasi dictionary `data` terhadap `schema`.

    Aturan schema per field (semua opsional kecuali 'type'):
        type       : tipe Python atau tuple tipe (mis. int, (int, float))
        required   : bool (default True)
        min / max  : rentang nilai untuk angka
        min_length / max_length : panjang untuk str/list
        choices    : daftar nilai yang diperbolehkan

    *args   : fungsi validator tambahan, bentuk f(data) -> str | None
              (kembalikan pesan error, atau None jika valid).
    **kwargs: strict=False -> tolak field di luar schema bila True
              stop_on_first=False -> berhenti di error pertama bila True

    Returns:
        (is_valid: bool, errors: list[str])
    """
    strict = kwargs.get("strict", False)
    stop_first = kwargs.get("stop_on_first", False)
    errors = []

    def tambah(pesan):
        errors.append(pesan)
        return stop_first

    for field, aturan in schema.items():
        wajib = aturan.get("required", True)
        if field not in data or data[field] is None:
            if wajib and tambah(f"'{field}' wajib diisi"):
                return False, errors
            continue

        nilai = data[field]
        tipe = aturan.get("type")
        if tipe:
            # bool adalah subclass int; tolak bila tipe yang diminta bukan bool
            salah_bool = isinstance(nilai, bool) and tipe not in (bool, (bool,))
            if salah_bool or not isinstance(nilai, tipe):
                nama = tipe.__name__ if isinstance(tipe, type) else \
                    "/".join(t.__name__ for t in tipe)
                if tambah(f"'{field}' harus bertipe {nama}, "
                          f"bukan {type(nilai).__name__}"):
                    return False, errors
                continue

        if isinstance(nilai, (int, float)):
            if "min" in aturan and nilai < aturan["min"]:
                if tambah(f"'{field}' minimal {aturan['min']}, didapat {nilai}"):
                    return False, errors
            if "max" in aturan and nilai > aturan["max"]:
                if tambah(f"'{field}' maksimal {aturan['max']}, didapat {nilai}"):
                    return False, errors

        if hasattr(nilai, "__len__"):
            if "min_length" in aturan and len(nilai) < aturan["min_length"]:
                if tambah(f"'{field}' minimal {aturan['min_length']} karakter/item"):
                    return False, errors
            if "max_length" in aturan and len(nilai) > aturan["max_length"]:
                if tambah(f"'{field}' maksimal {aturan['max_length']} karakter/item"):
                    return False, errors

        if "choices" in aturan and nilai not in aturan["choices"]:
            if tambah(f"'{field}' harus salah satu dari {aturan['choices']}"):
                return False, errors

    if strict:
        for field in data.keys() - schema.keys():
            if tambah(f"Field '{field}' tidak dikenal"):
                return False, errors

    for validator in args:
        pesan = validator(data)
        if pesan and tambah(pesan):
            return False, errors

    return len(errors) == 0, errors


if __name__ == "__main__":
    schema = {
        "nama": {"type": str, "min_length": 3},
        "umur": {"type": int, "min": 17, "max": 60},
        "ipk": {"type": (int, float), "min": 0, "max": 4},
        "prodi": {"type": str, "choices": ["TI", "SI", "MI"], "required": False},
    }
    cek_nama = lambda d: "Nama tidak boleh angka semua" if str(d.get("nama", "")).isdigit() else None

    print(validasi_data({"nama": "Budi", "umur": 20, "ipk": 3.5}, schema, cek_nama))
    print(validasi_data({"nama": "Al", "umur": 10, "ipk": "tinggi", "x": 1},
                        schema, cek_nama, strict=True))
