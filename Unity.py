import pandas as pd
import glob
import os

all_files = glob.glob("dataset_youtube_*.csv")
temp_list = []

for filename in all_files:
    df = pd.read_csv(filename)
    df['source_file'] = filename 
    temp_list.append(df)

df_master = pd.concat(temp_list, axis=0, ignore_index=True)

# --- PROSES MERAPIKAN ---
# 1. Hapus duplikat berdasarkan ID unik komentar
df_master = df_master.drop_duplicates(subset=['comment_id'])

# 2. Hilangkan pindah baris agar satu komentar = satu baris di Excel
df_master['text'] = df_master['text'].astype(str).str.replace(r'[\n\r]+', ' ', regex=True).str.strip()

# 3. Urutkan waktu
df_master = df_master.sort_values(by="create_time").reset_index(drop=True)

# --- MENAMPILKAN INFO ---
print("="*40)
print(f"HASIL ANALISIS DATASET")
print("="*40)
print(f"Total Komentar Gabungan: {len(df_master)} baris")
print("-"*40)
print("Top 5 Video dengan Komentar Terbanyak:")
print(df_master['source_file'].value_counts().head(5))

# Simpan
df_master.to_csv("master_dataset_clean.csv", index=False)