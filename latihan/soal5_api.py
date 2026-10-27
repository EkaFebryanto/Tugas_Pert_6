"""Soal 5 - Ambil data JSONPlaceholder, olah dengan lambda/map/filter/sorted."""
import json
from collections import Counter
from functools import reduce

import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


def ambil_data(endpoint):
    resp = requests.get(f"{BASE_URL}/{endpoint}", timeout=10)
    resp.raise_for_status()
    return resp.json()


def analisis(users, posts):
    nama_user = {u["id"]: u["name"] for u in users}

    # map: tambahkan nama penulis dan jumlah kata judul
    posts_ex = list(map(lambda p: {**p,
                                   "penulis": nama_user[p["userId"]],
                                   "jumlah_kata_judul": len(p["title"].split())},
                        posts))

    # filter: judul panjang (>= 6 kata)
    judul_panjang = list(filter(lambda p: p["jumlah_kata_judul"] >= 6, posts_ex))

    # sorted: 5 judul terpanjang (kata desc, lalu judul asc)
    top5 = sorted(posts_ex, key=lambda p: (-p["jumlah_kata_judul"], p["title"]))[:5]

    # reduce: total kata seluruh judul
    total_kata = reduce(lambda acc, p: acc + p["jumlah_kata_judul"], posts_ex, 0)

    # jumlah post per user, diurutkan dari terbanyak
    per_user = Counter(map(lambda p: p["penulis"], posts_ex))
    ranking = sorted(per_user.items(), key=lambda kv: (-kv[1], kv[0]))

    return {
        "total_post": len(posts_ex),
        "total_user": len(users),
        "rata_rata_kata_judul": round(total_kata / len(posts_ex), 2),
        "jumlah_judul_panjang": len(judul_panjang),
        "top5_judul_terpanjang": list(map(
            lambda p: {"id": p["id"], "judul": p["title"],
                       "penulis": p["penulis"],
                       "jumlah_kata": p["jumlah_kata_judul"]}, top5)),
        "post_per_user": [{"penulis": n, "jumlah_post": j} for n, j in ranking],
    }


def simpan_json(data, nama_file="hasil_analisis.json"):
    with open(nama_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Hasil disimpan ke {nama_file}")


if __name__ == "__main__":
    try:
        users, posts = ambil_data("users"), ambil_data("posts")
    except requests.RequestException as e:
        raise SystemExit(f"Gagal mengambil data: {e}")
    hasil = analisis(users, posts)
    print(json.dumps(hasil, indent=2, ensure_ascii=False)[:800], "...")
    simpan_json(hasil)
