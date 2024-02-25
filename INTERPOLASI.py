import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
import easygui

# Mendefinisikan x_uniform untuk kedua metode interpolasi
x_uniform = np.arange(0, 11, 0.2)
print(x_uniform)

# Meminta pengguna untuk memilih metode interpolasi
metode_interpolasi = 2

# Direktori awal diatur ke desktop
desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop/')

# Meminta pengguna untuk memilih file CSV dari desktop
nama_file = easygui.fileopenbox(title="Pilih File CSV", filetypes=["*.csv"], default=desktop_path)

# Pastikan pengguna memilih file
if nama_file is not None:
    # Baca file CSV dan simpan ke dalam DataFrame
    df = pd.read_csv(nama_file, header=None)

    # Simpan kolom x_data dan y_data ke dalam array NumPy
    x_data = np.array(df.iloc[:, 0])
    y_data = np.array(df.iloc[:, 1])

    # Urutkan titik-titik data berdasarkan nilai x
    sorted_indices = np.argsort(x_data)
    x_data_sorted = x_data[sorted_indices]
    y_data_sorted = y_data[sorted_indices]

    if metode_interpolasi == 1:
        # Buat fungsi interpolasi spline kubik
        interpolator = CubicSpline(x_data, y_data)
        # Hitung nilai y yang diinterpolasi untuk data x_uniform
        y_interpolated = interpolator(x_uniform)
    elif metode_interpolasi == 2:
        # Inisialisasi daftar kosong untuk menyimpan hasil interpolasi piecewise
        x_piecewise = []
        y_piecewise = []

        # Interpolasi piecewise menggunakan pendekatan linier
        for i in range(len(x_data_sorted) - 1):
            x1, x2 = x_data_sorted[i], x_data_sorted[i + 1]
            y1, y2 = y_data_sorted[i], y_data_sorted[i + 1]

            slope = (y2 - y1) / (x2 - x1)
            step_size = x_uniform[i + 1] - x_uniform[i]  # Mendapatkan pertambahan dari nilai x_uniform
            x_values = np.arange(x1, x2, step_size)  # Gunakan pertambahan nilai dari x_uniform
            y_values = y1 + slope * (x_values - x1)

            x_piecewise.extend(x_values)
            y_piecewise.extend(y_values)

        # Tambahkan titik terakhir
        x_piecewise.append(x_data_sorted[-1])
        y_piecewise.append(y_data_sorted[-1])

# Plot data asli dan hasil interpolasi
plt.plot(x_data, y_data, 'o', label='Data Asli')

if metode_interpolasi == 1:
    # Plot interpolasi spline kubik
    plt.plot(x_uniform, y_interpolated, "-", label='Interpolasi Spline Kubik')

elif metode_interpolasi == 2:
    # Plot interpolasi piecewise
    plt.plot(x_piecewise, y_piecewise, "--", label='Interpolasi Piecewise (Linier)')

plt.xlabel('x')
plt.ylabel('y')
plt.title('Interpolasi Data')
plt.legend()

# Simpan hasil interpolasi ke file CSV
nama_file_tanpa_ext = os.path.splitext(nama_file)[0]  # nama file tanpa ekstensi
nama_file_interpolated = f"{nama_file_tanpa_ext}_interpolated.csv"
if metode_interpolasi == 1:
    # Simpan hasil interpolasi Cubic Spline
    data_interpolated = np.column_stack((x_uniform, y_interpolated))
    np.savetxt(nama_file_interpolated, data_interpolated, delimiter=',', fmt='%f', header='x,y', comments='')
elif metode_interpolasi == 2:
    # Simpan hasil interpolasi Piecewise Linear
    data_interpolated = np.column_stack((x_piecewise, y_piecewise))
    np.savetxt(nama_file_interpolated, data_interpolated, delimiter=',', fmt='%f', header='x,y', comments='')

# Tampilkan plot
plt.show()
