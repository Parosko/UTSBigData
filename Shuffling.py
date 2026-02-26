import pandas as pd

# 1. Load dataset master yang sudah digabungkan
file_input = "Data/master_dataset_clean.csv"
df = pd.read_csv(file_input)

# 2. Proses Shuffling (Mengacak urutan baris)

df_shuffled = df.sample(frac=1, random_state=42).reset_index(drop=True)

# 3. Simpan hasil acakan ke file baru
file_output = "Data/master_dataset_shuffled.csv"
df_shuffled.to_csv(file_output, index=False)

print(f"Berhasil mengacak {len(df_shuffled)} baris data.")
print(f"Dataset yang sudah terserak random disimpan di: {file_output}")

# 4. Intip sedikit data untuk memastikan sudah teracak
print("\nCek 10 baris pertama (kolom source_file):")
print(df_shuffled['source_file'].head(10))