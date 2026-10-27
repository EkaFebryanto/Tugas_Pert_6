"""Program Pengambilan dan Analisis Data JSONPlaceholder.

Mengambil data dari public REST API JSONPlaceholder memakai library requests,
kemudian mengolah data menggunakan lambda, map, filter, sorted, dan reduce.
Hasil akhir disimpan dalam format JSON.
"""

from collections import Counter
from functools import reduce
import json
import sys
from typing import Any, Dict, List, Tuple, Union

import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


def ambil_data(
    endpoint: str = None,
) -> Union[List[Dict[str, Any]], Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]]:
    """Mengambil data dari endpoint public REST API JSONPlaceholder.

    Fungsi ini melakukan HTTP GET dengan timeout 10 detik, memvalidasi status
    kode dengan raise_for_status(), dan menangani error dengan try/except.
    Jika endpoint tidak ditentukan, fungsi mengambil users dan posts sekaligus.

    Args:
        endpoint (str, optional): Nama endpoint API ('users' atau 'posts').

    Returns:
        Union[List[Dict[str, Any]], Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]]:
            List data JSON jika endpoint diberikan, atau tuple (users, posts) jika None.

    Raises:
        requests.RequestException: Jika terjadi kesalahan request HTTP atau koneksi.
    """
    try:
        if endpoint:
            clean_endpoint = endpoint.strip("/")
            resp = requests.get(f"{BASE_URL}/{clean_endpoint}", timeout=10)
            resp.raise_for_status()
            return resp.json()

        # Mengambil users dan posts secara berurutan
        resp_users = requests.get(f"{BASE_URL}/users", timeout=10)
        resp_users.raise_for_status()

        resp_posts = requests.get(f"{BASE_URL}/posts", timeout=10)
        resp_posts.raise_for_status()

        return resp_users.json(), resp_posts.json()
    except requests.RequestException as err:
        print(f"[ERROR] Terjadi kegagalan request API: {err}", file=sys.stderr)
        raise


def analisis(
    users: List[Dict[str, Any]], posts: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Menganalisis data users dan posts menggunakan functional programming.

    Transformasi dilakukan tanpa loop for eksplisit, murni memakai lambda
    bersama higher-order functions: map, filter, sorted, dan reduce.

    Args:
        users (List[Dict[str, Any]]): Data dari endpoint /users.
        posts (List[Dict[str, Any]]): Data dari endpoint /posts.

    Returns:
        Dict[str, Any]: Dictionary hasil analisis berisi metrik yang ditentukan.
    """
    # Mapping ID user ke nama penulis menggunakan map dan lambda (tanpa loop for)
    user_map = dict(map(lambda u: (u["id"], u["name"]), users))

    # 1. map: Menambahkan nama penulis dan jumlah kata judul ke setiap post
    posts_diperkaya = list(
        map(
            lambda p: {
                **p,
                "penulis": user_map.get(p["userId"], "Tidak Diketahui"),
                "jumlah_kata_judul": len(p["title"].split()),
            },
            posts,
        )
    )

    # 2. filter: Memilih post yang judulnya memiliki minimal 6 kata
    judul_panjang = list(
        filter(lambda p: p["jumlah_kata_judul"] >= 6, posts_diperkaya)
    )

    # 3. sorted: 5 post dengan judul terpanjang (jumlah kata menurun, lalu judul A-Z)
    top5_raw = sorted(
        posts_diperkaya,
        key=lambda p: (-p["jumlah_kata_judul"], p["title"]),
    )[:5]

    top5_judul_terpanjang = list(
        map(
            lambda p: {
                "id": p["id"],
                "judul": p["title"],
                "penulis": p["penulis"],
                "jumlah_kata": p["jumlah_kata_judul"],
            },
            top5_raw,
        )
    )

    # 4. sorted: Ranking jumlah post per penulis (jumlah menurun, lalu nama A-Z)
    frekuensi_penulis = Counter(map(lambda p: p["penulis"], posts_diperkaya))
    ranking_penulis = sorted(
        frekuensi_penulis.items(),
        key=lambda item: (-item[1], item[0]),
    )
    post_per_user = list(
        map(
            lambda item: {
                "penulis": item[0],
                "jumlah_post": item[1],
            },
            ranking_penulis,
        )
    )

    # 5. functools.reduce: Menghitung total kata seluruh judul dan rata-ratanya
    total_kata_judul = reduce(
        lambda acc, p: acc + p["jumlah_kata_judul"],
        posts_diperkaya,
        0,
    )
    total_post = len(posts_diperkaya)
    rata_rata_kata = (
        round(total_kata_judul / total_post, 2) if total_post > 0 else 0.0
    )

    # 6. Mengemas seluruh hasil analisis ke dalam satu dictionary
    return {
        "total_post": total_post,
        "total_user": len(users),
        "rata_rata_kata_judul": rata_rata_kata,
        "jumlah_judul_panjang": len(judul_panjang),
        "top5_judul_terpanjang": top5_judul_terpanjang,
        "post_per_user": post_per_user,
    }


def simpan_json(
    data: Dict[str, Any], path_file: str = "hasil_analisis.json"
) -> None:
    """Menyimpan dictionary data ke file JSON dengan format rapi.

    Args:
        data (Dict[str, Any]): Data yang akan disimpan.
        path_file (str, optional): Path file tujuan. Default 'hasil_analisis.json'.
    """
    with open(path_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"[INFO] Data berhasil disimpan ke '{path_file}'.")


if __name__ == "__main__":
    print("[INFO] Mengambil data dari JSONPlaceholder API...")
    try:
        users, posts = ambil_data()
        print(f"[INFO] Berhasil mengambil {len(users)} users dan {len(posts)} posts.")

        # Lakukan analisis data
        hasil = analisis(users, posts)

        # Simpan hasil analisis ke file JSON
        simpan_json(hasil)

        # Tampilkan ringkasan singkat di konsol
        print("\n=== Ringkasan Analisis ===")
        print(f"Total Post                : {hasil['total_post']}")
        print(f"Total User                : {hasil['total_user']}")
        print(f"Rata-rata Kata Judul      : {hasil['rata_rata_kata_judul']}")
        print(f"Jumlah Judul Panjang (>=6): {hasil['jumlah_judul_panjang']}")
        print(f"Top 5 Judul Terpanjang    : {len(hasil['top5_judul_terpanjang'])} post")
        print(f"Post per User             : {len(hasil['post_per_user'])} penulis terdaftar")
    except requests.RequestException as err:
        sys.exit(f"[FATAL] Program dihentikan karena kegagalan API: {err}")
