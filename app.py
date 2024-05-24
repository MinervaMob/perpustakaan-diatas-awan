from flask import Flask, render_template, request, redirect
import time
import csv

app = Flask(__name__)

# membaca data csv
def read_data(file_path):
    data = []
    with open(file_path, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            data.append(row)
    return data

# pengurutan menggunakan bubble sort
def bubble_sort(arr, arr_sort):
    n = len(arr)
    
    start_time = time.time()
    for i in range(n):
        swapped = False

        for j in range(n - 1 - i):
            if arr[j][arr_sort] > arr[j + 1][arr_sort]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        if not swapped:
            break

    end_time = time.time()
    execution_time = end_time - start_time

    return arr, execution_time

# algoritma pencarian linier
def linear_search(data, key):

    # Menyimpan hasil pencarian berdasarkan kesesuaian huruf depan
    results_prefix = [row for row in data if row['judul_buku'].lower().startswith(key.lower())]
    # Menyimpan hasil pencarian berdasarkan kesesuaian dalam judul
    results_contains = [row for row in data if key.lower() in row['judul_buku'].lower()]

    return results_prefix, results_contains

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/book')
def book():
    file_path = 'data.csv'
    arr = read_data(file_path)
    arr_sort = 'judul_buku' 
    sorted_arr, execution_time = bubble_sort(arr, arr_sort)
    context_data = {
        "books": sorted_arr,
        "execution_time": float(execution_time)
    }
    return render_template('book.html', **context_data)

# Fitur Mencari Buku
@app.route('/search', methods=['POST'])
def search():
    file_path = 'data.csv'
    data = read_data(file_path)
    search_key = request.form['target'].lower()
    
    # Lakukan pencarian dengan menggunakan kedua metode
    waktu_mulai = time.time()
    results_prefix, results_contains = linear_search(data, search_key)
    waktu_selesai = time.time()
    
    waktu_eksekusi = waktu_selesai - waktu_mulai
    waktu_eksekusi = "{:.4f}".format(waktu_eksekusi)
    
    return render_template('cari.html', prefix_results=results_prefix, contains_results=results_contains, search_key=search_key, waktu_eksekusi=waktu_eksekusi)

# Halaman Detail Buku
@app.route('/detail/<judul_buku>')
def detail(judul_buku):
    file_path = 'data.csv'
    data = read_data(file_path)

    for index in data:
        if index.get('judul_buku') == judul_buku:
            book_data = index

    return render_template('detail.html', data=book_data)

# Fitur Tambahkan Buku
@app.route('/tambah_buku')
def tambah_buku_form():
    return render_template('tambah_buku.html')

# rute untuk menangani penambahan buku
@app.route('/tambah_buku', methods=['POST'])
def tambah_buku():
    file_path = 'data.csv'
    data = read_data(file_path)

    # informasi buku dari formulir
    judul = request.form['judul']
    kode_buku = request.form['kode_buku']
    penulis = request.form['penulis']
    penerbit = request.form['penerbit']
    tahun_terbit = request.form['tahun_terbit']
    jumlah_halaman = request.form['jumlah_halaman']

    # dictionary untuk buku baru
    buku_baru = {
        'judul_buku': judul,
        'kode_buku': kode_buku,
        'penulis': penulis,
        'penerbit': penerbit,
        'tahun_terbit': tahun_terbit,
        'jumlah_halaman': jumlah_halaman
    }

    # Tambahkan buku baru ke dalam data
    data.append(buku_baru)

    # Simpan data yang sudah ditambahkan ke file CSV
    with open(file_path, 'a', newline='') as csv_file:
        fieldnames = ['judul_buku', 'kode_buku', 'penulis', 'penerbit', 'tahun_terbit', 'jumlah_halaman']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writerow(buku_baru)

    # Redirect kembali ke halaman buku setelah menambahkan buku
    return redirect('/book')

# fitur menghapus buku 
@app.route('/hapus/<judul_buku>', methods=['POST'])
def hapus_buku(judul_buku):
    file_path = 'data.csv'
    data = read_data(file_path)

    # Cari buku berdasarkan judul
    for index, book in enumerate(data):
        if book['judul_buku'] == judul_buku:
            # Hapus buku dari data
            hapus_buku = data.pop(index)

            # Simpan data yang sudah dihapus ke file CSV
            with open(file_path, 'w', newline='') as csv_file:
                hapus = hapus_buku.keys()
                writer = csv.DictWriter(csv_file, fieldnames=hapus)
                writer.writeheader()
                writer.writerows(data)

            # Redirect kembali ke halaman buku setelah menghapus
            return redirect('/book')

    # Jika buku tidak ditemukan
    return render_template('buku_tidak_ditemukan.html', judul_buku=judul_buku)

@app.route('/presentasi')
def presentasi():
    return render_template('presentasi.html')


if __name__ == '__main__':
    app.run(debug=True)
