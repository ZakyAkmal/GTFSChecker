import streamlit as st
import pandas as pd
import requests
import zipfile
import os
import glob
import gdown
import re
import shutil
import io
import json
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pickle

st.set_page_config(page_title="Transit Data Checker", page_icon="🚇", layout="wide")

# ==========================================
# DATA STATIS: JENIS LAYANAN
# ==========================================
MASTER_LAYANAN = {
    "10A": "Rusun", "10B": "Rusun", "10C": "IPLK", "11B": "Rusun", "11C": "Rusun",
    "11D": "IPLK", "11M": "Rusun", "11P": "Rusun", "11Q": "IPLK", "11R": "Rusun",
    "11W": "IPLK", "12A": "IPLK", "12B": "IPLK", "12C": "Rusun", "12F": "Rusun",
    "12H": "Rusun", "12P": "IPLK", "14A": "IPLK", "14B": "IPLK", "1A": "IPLK",
    "1B": "IPLK", "1C": "IPLK", "1E": "IPLK", "1F": "IPLK", "1H": "IPLK",
    "1K": "Royaltrans", "1M": "IPLK", "1N": "IPLK", "1P": "IPLK", "1Q": "IPLK",
    "1R": "IPLK", "1T": "Royaltrans", "1W": "IPLK", "21ST": "IPLK", "2B": "IPLK",
    "2F": "Rusun", "2H": "Rusun", "2P": "IPLK", "2Q": "IPLK", "3A": "Rusun",
    "3B": "Rusun", "3C": "Rusun", "3D": "IPLK", "3E": "IPLK", "4B": "IPLK",
    "4C": "IPLK", "4E": "Rusun", "4F": "IPLK", "4K": "IPLK", "5B": "IPLK",
    "5F": "IPLK", "5M": "IPLK", "5N": "IPLK", "6C": "IPLK", "6D": "IPLK",
    "6H": "IPLK", "6K": "IPLK", "6M": "IPLK", "6N": "IPLK", "6P": "Royaltrans",
    "6Q": "IPLK", "6T": "IPLK", "6U": "IPLK", "6W": "IPLK", "7A": "IPLK",
    "7B": "IPLK", "7C": "IPLK", "7D": "IPLK", "7E": "IPLK", "7P": "IPLK",
    "7Q": "IPLK", "7R": "IPLK", "7T": "IPLK", "7U": "IPLK", "7V": "IPLK",
    "7W": "IPLK", "8A": "IPLK", "8C": "IPLK", "8D": "IPLK", "8E": "IPLK",
    "8K": "IPLK", "8M": "IPLK", "8N": "IPLK", "9D": "IPLK", "9E": "IPLK",
    "9F": "Rusun", "9H": "IPLK", "B11": "Transjabodetabek", "B13": "Royaltrans",
    "B14": "Royaltrans", "B21": "Transjabodetabek", "B25": "Transjabodetabek",
    "B41": "Transjabodetabek", "BW1": "Wisata", "BW2": "Wisata", "BW4": "Wisata",
    "BW9": "Wisata", "D11": "Transjabodetabek", "D21": "Transjabodetabek",
    "D31": "Royaltrans", "D32": "Royaltrans", "D41": "Transjabodetabek",
    "P11": "Transjabodetabek", "S11": "Transjabodetabek", "S12": "Royaltrans",
    "S14": "Royaltrans", "S21": "Transjabodetabek", "S22": "Transjabodetabek",
    "S31": "Royaltrans", "S61": "Transjabodetabek", "SH1": "Transjabodetabek",
    "T11": "Transjabodetabek", "T12": "Transjabodetabek", "T31": "Transjabodetabek",
    "JAK.01": "Mikrotrans", "JAK.02": "Mikrotrans", "JAK.03": "Mikrotrans",
    "JAK.04": "Mikrotrans", "JAK.05": "Mikrotrans", "JAK.06": "Mikrotrans",
    "JAK.07": "Mikrotrans", "JAK.08": "Mikrotrans", "JAK.09": "Mikrotrans",
    "JAK.10": "Mikrotrans", "JAK.100": "Mikrotrans", "JAK.102": "Mikrotrans",
    "JAK.105": "Mikrotrans", "JAK.106": "Mikrotrans", "JAK.107": "Mikrotrans",
    "JAK.108": "Mikrotrans", "JAK.10A": "Mikrotrans", "JAK.10B": "Mikrotrans",
    "JAK.11": "Mikrotrans", "JAK.110A": "Mikrotrans", "JAK.112": "Mikrotrans",
    "JAK.113": "Mikrotrans", "JAK.115": "Mikrotrans", "JAK.117": "Mikrotrans",
    "JAK.118": "Mikrotrans", "JAK.12": "Mikrotrans", "JAK.120": "Mikrotrans",
    "JAK.13": "Mikrotrans", "JAK.14": "Mikrotrans", "JAK.15": "Mikrotrans",
    "JAK.16": "Mikrotrans", "JAK.17": "Mikrotrans", "JAK.18": "Mikrotrans",
    "JAK.19": "Mikrotrans", "JAK.20": "Mikrotrans", "JAK.21": "Mikrotrans",
    "JAK.22": "Mikrotrans", "JAK.23": "Mikrotrans", "JAK.24": "Mikrotrans",
    "JAK.25": "Mikrotrans", "JAK.26": "Mikrotrans", "JAK.27": "Mikrotrans",
    "JAK.28": "Mikrotrans", "JAK.29": "Mikrotrans", "JAK.30": "Mikrotrans",
    "JAK.31": "Mikrotrans", "JAK.32": "Mikrotrans", "JAK.33": "Mikrotrans",
    "JAK.34": "Mikrotrans", "JAK.35": "Mikrotrans", "JAK.36": "Mikrotrans",
    "JAK.37": "Mikrotrans", "JAK.38": "Mikrotrans", "JAK.39": "Mikrotrans",
    "JAK.40": "Mikrotrans", "JAK.41": "Mikrotrans", "JAK.42": "Mikrotrans",
    "JAK.43B": "Mikrotrans", "JAK.43C": "Mikrotrans", "JAK.44": "Mikrotrans",
    "JAK.45": "Mikrotrans", "JAK.46": "Mikrotrans", "JAK.47": "Mikrotrans",
    "JAK.48A": "Mikrotrans", "JAK.49": "Mikrotrans", "JAK.50": "Mikrotrans",
    "JAK.51": "Mikrotrans", "JAK.52": "Mikrotrans", "JAK.53": "Mikrotrans",
    "JAK.54": "Mikrotrans", "JAK.56": "Mikrotrans", "JAK.58": "Mikrotrans",
    "JAK.59": "Mikrotrans", "JAK.60": "Mikrotrans", "JAK.61": "Mikrotrans",
    "JAK.64": "Mikrotrans", "JAK.71": "Mikrotrans", "JAK.72": "Mikrotrans",
    "JAK.73": "Mikrotrans", "JAK.74": "Mikrotrans", "JAK.75": "Mikrotrans",
    "JAK.76": "Mikrotrans", "JAK.77": "Mikrotrans", "JAK.78A": "Mikrotrans",
    "JAK.78B": "Mikrotrans", "JAK.79": "Mikrotrans", "JAK.80": "Mikrotrans",
    "JAK.84": "Mikrotrans", "JAK.85": "Mikrotrans", "JAK.86": "Mikrotrans",
    "JAK.87": "Mikrotrans", "JAK.88": "Mikrotrans", "JAK.89": "Mikrotrans",
    "JAK.90": "Mikrotrans", "JAK.93": "Mikrotrans", "JAK.95": "Mikrotrans",
    "JAK.98": "Mikrotrans", "JAK.99": "Mikrotrans",
    "1": "BRT", "2": "BRT", "2A": "BRT", "3": "BRT", "3F": "BRT", "3H": "BRT",
    "4": "BRT", "4D": "BRT", "5": "BRT", "5C": "BRT", "6": "BRT", "6A": "BRT",
    "6B": "BRT", "6V": "BRT", "7": "BRT", "7F": "BRT", "8": "BRT", "9": "BRT",
    "9A": "BRT", "9C": "BRT", "9N": "BRT", "10": "BRT", "10D": "BRT",
    "10H": "BRT", "11": "BRT", "12": "BRT", "13": "BRT", "13B": "BRT",
    "13E": "BRT", "14": "BRT", "L13E": "BRT", "B51": "Transjabodetabek",
    "SH2": "Transjabodetabek", "PRJ2": "BRT", "PRJ3": "BRT", "2C": "BRT"
}

LIST_HALTE = [
    "Puri Beta 1", "JORR", "Duri Kepa", "Kebon Jeruk", "Bungur", "Tanah Kusir", "Jelambar",
    "Kali Grogol Arah Utara", "Kali Grogol Arah Selatan", "Jembatan Tiga", "Kota Bambu Arah Utara",
    "Kemanggisan Arah Utara", "Ps. Palmerah", "St. Palmerah", "Kota Bambu Arah Selatan",
    "Kemanggisan Arah Selatan", "Blok M", "Bandengan", "Transjakarta Tanah Abang 1", "Kali Besar",
    "Explorer Tanah Abang", "Transjakarta Tanah Abang 2", "Kebon Sirih Arah Utara", "Tegal Parang Arah Barat",
    "Blok M Jalur 2", "Ancol", "Gambir", "Istiqlal", "ASEAN", "Gambir 2", "Tegal Parang Arah Timur",
    "Perintis Kemerdekaan", "Pisangan", "Balai Kota", "Kota", "Bermis", "Bidara Cina", "Buaran",
    "Buncit Indah", "Bundaran Senayan", "Cakung Cilincing", "CBD Ciledug", "Cempaka Putih", "Cipinang",
    "Cipulir", "CSW 1", "CSW 2", "Rasuna Said", "Duren Tiga", "Galur", "Gedong Panjang", "Gelanggang Remaja",
    "Glodok", "Halimun", "Jati Padang", "Jembatan Baru", "Jembatan Besi", "Jembatan Dua", "Kalideres",
    "Kampung Melayu", "Kampung Rambutan", "Kampung Sumur", "Cawang Cililitan", "Lapangan Banteng",
    "Bundaran HI Astra", "Cawang Sentral", "Jembatan Merah", "Pejambon", "Cempaka Mas", "Simpang Cempaka",
    "Cempaka Baru", "Pasar Baru", "Gunung Sahari", "Pulo Nangka", "Damai", "Grogol", "Jatinegara",
    "Warung Buncit", "RSPAD", "Cawang Baru", "Makasar", "Ciliwung Arah Timur", "Denpasar Arah Barat",
    "Denpasar Arah Timur", "Grogol Reformasi", "Mambo", "Kebon Nanas", "Simpang Cawang", "Simpang Buaran",
    "Klender", "Flyover Cipinang", "Pancoran Arah Barat", "Kayu Putih Rawasari", "Kebayoran Lama",
    "Kejaksaan Agung", "Cakung", "Petukangan D'MASIV", "Sen Bank Jakarta", "Kelapa Dua Sasak",
    "Senen Raya", "Kramat Sentiong", "Kwitang", "Layur", "Lebak Bulus", "Mampang Prapatan", "Mangga Dua",
    "Masjid Agung", "Mayestik", "Pademangan", "Pakin", "Pal Putih", "Pasar Baru Timur", "Pasar Cempaka Putih",
    "Pasar Enjo", "Pasar Genjing", "Pasar Pulo Gadung", "Pasar Rumput", "Pecenongan", "Pedongkelan", "Pejaten",
    "Pemuda Pramuka", "Pemuda Rawamangun", "Pancoran Tugu", "Penjaringan", "Permata Hijau", "Pesakih",
    "Petojo", "Pinang Ranti", "Pluit", "Polda Metro Jaya", "Pondok Pinang", "Pos Pengumben", "Pulo Gebang",
    "Pulo Mas", "Pulo Mas Bypass", "Puri Beta 2", "Ragunan", "Rawa Barat", "Karet Kuningan", "Kuningan Madya",
    "Karet", "Museum Sejarah Jakarta", "Pramuka Sari", "Underpass Kuningan", "Flyover Kuningan", "Pasar Induk",
    "Kramat Jati", "Underpass Lebak Bulus", "Pondok Indah", "Kebayoran", "Arteri", "Kedoya Panjang", "Kedoya",
    "Pancoran Arah Timur", "Koja", "Halim", "Landasan Pacu", "Mangga Dua Raya", "Pluit Selatan", "Pulo Gadung",
    "Rawa Buaya", "Rawa Selatan", "Raya Bekasi Pulo Gebang", "Seskoal", "Simprug", "Stasiun Klender",
    "Plaza St. Manggarai", "Sumur Bor", "Jaga Jakarta", "Rawa Terate", "Sunter Kelapa Gading", "Taman Kota",
    "Tebet Eco Park Arah Timur", "Tanjung Priok", "Tebet Eco Park Arah Barat", "Tegalan", "Timur St. Manggarai",
    "Ujung Menteng", "Utan Kayu", "Utan Kayu Rawamangun", "Velodrome", "Walikota Jakarta Timur", "Tanah Tinggi",
    "Walikota Jakarta Utara Arah Utara", "Warung Jati", "Sumur Batu", "Roxy", "Pemuda Merdeka", "Kayu Jati",
    "Rawamangun", "Salemba", "Paseban", "Kesatrian", "Trikora", "Tanjung Duren Arah Barat",
    "Tanjung Duren Arah Timur", "Tomang Raya", "Tarakan", "Petamburan", "Jakarta International Stadium",
    "Kodamar", "Sunter Utara", "Tegal Mampang", "Pasar Santa", "Flyover Jatinegara", "Swadarma ParagonCorp",
    "Senen TOYOTA Rangga", "Danau Agung", "Stasiun Tebet", "Ciliwung Arah Barat", "Keselamatan", "Semanggi",
    "Bendungan Hilir", "Flyover Pramuka", "Matraman", "Flyover Raya Bogor", "PGC", "Jembatan Gantung",
    "Juanda", "Matraman Baru", "MH Thamrin", "Tosari", "Velbak", "Taman Sari", "Simpang Pramuka",
    "Bali Mester", "Jati Barat", "Cililitan", "Cikoko Arah Barat", "Cikoko Arah Timur", "Simpang Kuningan",
    "Stasiun Jatinegara", "Widya Chandra Telkomsel Arah Barat", "Sunter Karya", "Mangga Besar", "Sawah Besar",
    "Harmoni", "Kuningan", "Cawang", "Patra Kuningan", "Galunggung", "Tanah Merdeka Arah Timur",
    "Tanah Merdeka Arah Barat", "Pedati Prumpung", "Sunter Boulevard Barat",
    "Walikota Jakarta Utara Arah Selatan", "Plumpang", "Term. Pulo Gebang", "Dukuh Atas",
    "Flyover Pondok Kopi", "Penggilingan", "Kota Harapan Indah 1", "Kota Harapan Indah 2",
    "Pasar Modern Harapan Indah", "Transera Harapan Indah", "Tanah Apit", "Danau Sunter", "Bekasi Barat",
    "Jembatan Item", "Kemayoran", "Summarecon Bekasi", "Terminal Bekasi", "Monumen Nasional",
    "JIEXPO Kemayoran", "Transport Hub Dukuh Atas", "Gerbang Pemuda Arah Barat", "Gerbang Pemuda Arah Timur",
    "Simpang Ragunan Ar-Raudhah", "Widya Chandra Telkomsel Arah Timur", "Kebon Sirih Arah Selatan",
    "Pasar Cakung", "Setiabudi Integritas"
]

# --- INISIALISASI SESSION STATE ---
if 'data_processed' not in st.session_state: st.session_state.data_processed = False
if 'df_master' not in st.session_state: st.session_state.df_master = None
if 'df_most_frequent' not in st.session_state: st.session_state.df_most_frequent = None
if 'df_shapes' not in st.session_state: st.session_state.df_shapes = None
if 'df_gtfs_full' not in st.session_state: st.session_state.df_gtfs_full = None
if 'df_histori_full' not in st.session_state: st.session_state.df_histori_full = None
if 'gtfs_mapping' not in st.session_state: st.session_state.gtfs_mapping = {}
if 'df_stops' not in st.session_state: st.session_state.df_stops = None
if 'df_stop_times' not in st.session_state: st.session_state.df_stop_times = None
if 'df_halte_padat' not in st.session_state: st.session_state.df_halte_padat = None
if 'shape_dist' not in st.session_state: st.session_state.shape_dist = None
if 'df_komplain' not in st.session_state: st.session_state.df_komplain = None
if 'api_download_df' not in st.session_state: st.session_state.api_download_df = None
if 'pkl_bytes' not in st.session_state: st.session_state.pkl_bytes = None
if 'pkl_ready_name' not in st.session_state: st.session_state.pkl_ready_name = None

def extract_drive_id(url):
    match = re.search(r'/folders/([a-zA-Z0-9_-]+)', url)
    if match: return match.group(1)
    match = re.search(r'id=([a-zA-Z0-9_-]+)', url)
    if match: return match.group(1)
    return None

def calc_haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

def format_time(mins):
    if pd.isna(mins) or mins <= 0: return "-"
    h = int(mins // 60)
    m = int(mins % 60)
    return f"{h} jam {m} menit" if h > 0 else f"{m} menit"

def format_speed(speed):
    if pd.isna(speed) or speed <= 0: return "-"
    return f"{speed:.2f} KM/H"

def color_red_distance(val):
    try:
        v = float(val)
        color = 'red' if 0 < v < 0.2 else ''
        return f'color: {color}'
    except: return ''

def color_kepadatan(val, max_val):
    if pd.isna(val) or max_val == 0: return ''
    ratio = min(val / max_val, 1.0)
    r = 255
    g = int(255 * (1 - ratio * 0.8))
    b = int(255 * (1 - ratio * 0.8))
    text_color = "white" if ratio > 0.5 else "black"
    return f'background-color: rgb({r},{g},{b}); color: {text_color}'

def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

def get_iqr_avg(df_sub):
    if df_sub.empty or 'duration_mins' not in df_sub.columns: return 0
    v_dur = df_sub.dropna(subset=['duration_mins'])['duration_mins']
    if v_dur.empty: return 0
    if len(v_dur) == 1: return v_dur.iloc[0]
    q1, q3 = v_dur.quantile(0.25), v_dur.quantile(0.75)
    filt = v_dur[(v_dur >= max(0, q1 - 1.5 * (q3-q1))) & (v_dur <= q3 + 1.5 * (q3-q1))]
    return filt.mean() if not filt.empty else 0

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🚇 Navigasi Menu")
menu = st.sidebar.radio("Pilih Fitur:", ["🔍 Transit Checker", "📥 Data Downloader"])

if menu == "🔍 Transit Checker":
    st.title("🚇 Transit Data vs GTFS Checker & Analytics")
    st.write("Checker trip di Transit dengan trip di GTFS beserta analitik kinerjanya.")

    input_mode = st.radio("Metode Input Data:", ["Proses Data Baru (Raw Data)", "Load Database (.pkl)"], horizontal=True)
    st.markdown("---")
    
    if input_mode == "Load Database (.pkl)":
        st.markdown("### Load Database Memory (.pkl)")
        pkl_file = st.file_uploader("Upload File Database (.pkl) yang sudah di-export sebelumnya", type=["pkl"])
        if st.button("📂 Load Data", type="primary", use_container_width=True):
            if pkl_file is not None:
                with st.spinner("Memuat data dari memori..."):
                    try:
                        data = pickle.load(pkl_file)
                        st.session_state.df_master = data.get('df_master')
                        st.session_state.df_most_frequent = data.get('df_most_frequent')
                        st.session_state.df_shapes = data.get('df_shapes')
                        st.session_state.df_gtfs_full = data.get('df_gtfs_full')
                        st.session_state.df_histori_full = data.get('df_histori_full')
                        st.session_state.df_stops = data.get('df_stops')
                        st.session_state.df_stop_times = data.get('df_stop_times')
                        st.session_state.df_halte_padat = data.get('df_halte_padat')
                        st.session_state.shape_dist = data.get('shape_dist')
                        st.session_state.df_komplain = data.get('df_komplain')
                        st.session_state.gtfs_mapping = data.get('gtfs_mapping', {})
                        st.session_state.data_processed = True
                        st.success("✅ Database berhasil dimuat! Silakan lihat hasil analitik di bawah.")
                    except Exception as e:
                        st.error(f"Gagal memuat file .pkl: {e}")
            else:
                st.error("Upload file .pkl terlebih dahulu.")

    elif input_mode == "Proses Data Baru (Raw Data)":
        # --- UI INPUT (4 KOLOM) ---
        st.markdown("### Masukkan Data")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.info("1. File GTFS")
            gtfs_upload = st.file_uploader("Upload GTFS.zip", type=["zip"])

        with col2:
            st.info("2. Histori DO")
            history_method = st.radio("Metode Histori DO:", ["Upload File", "Link Google Drive"], horizontal=True, key="hist_rad")
            history_uploads, drive_link = None, ""
            if history_method == "Upload File": history_uploads = st.file_uploader("File DO (Excel/CSV)", type=["xlsx", "csv", "xls"], accept_multiple_files=True)
            else: drive_link = st.text_input("Link Folder DO")

        with col3:
            st.info("3. Dispatch Syntra (Opsional)")
            dispatch_method = st.radio("Metode Dispatch:", ["Upload File", "Link Google Drive"], horizontal=True, key="disp_rad")
            dispatch_uploads, dispatch_link = None, ""
            if dispatch_method == "Upload File": dispatch_uploads = st.file_uploader("File Dispatch (Excel/CSV)", type=["xlsx", "csv", "xls"], accept_multiple_files=True)
            else: dispatch_link = st.text_input("Link Folder Dispatch")

        with col4:
            st.info("4. Mikrotrip (Opsional)")
            mikro_method = st.radio("Metode Mikrotrip:", ["Upload File", "Link Google Drive"], horizontal=True, key="mikro_rad")
            mikro_uploads, mikro_link = None, ""
            if mikro_method == "Upload File": mikro_uploads = st.file_uploader("File Mikrotrip (Excel/CSV)", type=["xlsx", "csv", "xls"], accept_multiple_files=True)
            else: mikro_link = st.text_input("Link Folder Mikrotrip")

        process_btn = st.button("🚀 Processing", type="primary", use_container_width=True)

        if process_btn:
            if not gtfs_upload: st.error("Jangan lupa upload file GTFS.zip dulu kawan")
            elif history_method == "Link Google Drive" and not drive_link:
                st.error("Jangan lupa masukin link Drive DO nya dulu kawan")
            elif history_method == "Upload File" and not history_uploads:
                st.error("Jangan lupa upload file DO nya dulu kawan")
            else:
                with st.spinner("Processing..."):
                    temp_dir = "temp_processing"
                    if os.path.exists(temp_dir): shutil.rmtree(temp_dir)
                    os.makedirs(temp_dir)
                    os.makedirs(os.path.join(temp_dir, "gtfs_data"))
                    
                    try:
                        # ==========================================
                        # 1. KOMPLAIN
                        # ==========================================
                        sheet_id = "1jkNtV7BuXsK2ybzIWHvcFUswKDco7xEvTa_8izIGzZc"
                        sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"
                        try:
                            resp_k = requests.get(sheet_url, timeout=30)
                            all_sheets = pd.read_excel(io.BytesIO(resp_k.content), sheet_name=None, engine='openpyxl')
                            df_k, col_rute, col_tgl, col_hour, col_jam = None, None, None, None, None
                            
                            for s_name, s_data in all_sheets.items():
                                c_rute = next((c for c in s_data.columns if str(c).strip().lower() == 'kode rute'), None)
                                c_tgl = next((c for c in s_data.columns if str(c).strip().lower() == 'tanggal'), None)
                                c_hour = next((c for c in s_data.columns if str(c).strip().lower() == 'hour'), None)
                                c_jam = next((c for c in s_data.columns if str(c).strip().lower() == 'jam'), None)
                                
                                if c_rute and c_tgl:
                                    df_k, col_rute, col_tgl, col_hour, col_jam = s_data, c_rute, c_tgl, c_hour, c_jam
                                    break
                                    
                            if df_k is not None:
                                df_k[col_rute] = df_k[col_rute].astype(str).str.strip().str.upper()
                                df_k['tanggal_merge'] = pd.to_datetime(df_k[col_tgl], errors='coerce').dt.date
                                
                                if col_hour:
                                    df_k['jam_komplain'] = pd.to_numeric(df_k[col_hour], errors='coerce').fillna(0).astype(int)
                                elif col_jam:
                                    df_k['jam_komplain'] = pd.to_datetime(df_k[col_jam].astype(str).str.strip(), format='%H:%M', errors='coerce').dt.hour.fillna(0).astype(int)
                                else:
                                    df_k['jam_komplain'] = 0
                                    
                                st.session_state.df_komplain = df_k.dropna(subset=['tanggal_merge'])
                        except: pass

                        # ==========================================
                        # 2. API TRANSIT
                        # ==========================================
                        url_api = "http://transit.transjakarta.co.id:8182/api/v1/master/rute-table"
                        api_mapping = {}
                        set_transit = set()
                        try:
                            resp = requests.get(url_api, timeout=15).json()
                            api_response = resp.get('data', list(resp.values())[0] if resp else []) if isinstance(resp, dict) else []
                            df_transit = pd.DataFrame(api_response)
                            if 'status' in df_transit.columns: df_transit = df_transit[df_transit['status'].astype(str).str.lower() == 'active']
                            id_col = 'rute_trip_id' if 'rute_trip_id' in df_transit.columns else ('trip_id' if 'trip_id' in df_transit.columns else None)
                            if id_col:
                                df_transit[id_col] = df_transit[id_col].astype(str).str.strip().str.upper()
                                set_transit = set(df_transit[id_col])
                                api_name_col = next((col for col in ['rute_name', 'nama_rute', 'name'] if col in df_transit.columns), None)
                                if api_name_col: api_mapping = df_transit.drop_duplicates(id_col).set_index(id_col)[api_name_col].to_dict()
                        except: pass

                        # ==========================================
                        # 3. GTFS
                        # ==========================================
                        with zipfile.ZipFile(gtfs_upload, 'r') as zip_ref:
                            for f_name in ["trips.txt", "shapes.txt", "stops.txt", "stop_times.txt"]:
                                try: zip_ref.extract(f_name, path=os.path.join(temp_dir, "gtfs_data"))
                                except: pass
                        
                        df_gtfs = pd.read_csv(os.path.join(temp_dir, "gtfs_data", "trips.txt"))
                        df_gtfs['trip_id'] = df_gtfs['trip_id'].astype(str).str.strip().str.upper()
                        df_gtfs['route_id'] = df_gtfs['route_id'].astype(str).str.strip().str.upper() if 'route_id' in df_gtfs.columns else "-"
                        gtfs_unique_routes = df_gtfs['route_id'].unique() if 'route_id' in df_gtfs.columns else []
                        set_gtfs = set(df_gtfs['trip_id'])
                        gtfs_name_col = next((col for col in ['trip_short_name', 'trip_headsign', 'route_id'] if col in df_gtfs.columns), 'trip_id')
                        gtfs_mapping = df_gtfs.drop_duplicates('trip_id').set_index('trip_id')[gtfs_name_col].to_dict()
                        st.session_state.gtfs_mapping = gtfs_mapping
                        st.session_state.df_gtfs_full = df_gtfs
                        
                        if os.path.exists(os.path.join(temp_dir, "gtfs_data", "shapes.txt")):
                            df_shapes = pd.read_csv(os.path.join(temp_dir, "gtfs_data", "shapes.txt"))
                            df_shapes['shape_id'] = df_shapes['shape_id'].astype(str).str.strip()
                            df_shapes = df_shapes.dropna(subset=['shape_pt_lat', 'shape_pt_lon'])
                            st.session_state.df_shapes = df_shapes
                            df_s_sorted = df_shapes.sort_values(['shape_id', 'shape_pt_sequence'])
                            df_s_sorted['shift_lat'] = df_s_sorted.groupby('shape_id')['shape_pt_lat'].shift()
                            df_s_sorted['shift_lon'] = df_s_sorted.groupby('shape_id')['shape_pt_lon'].shift()
                            df_s_sorted['dist'] = calc_haversine(df_s_sorted['shift_lat'], df_s_sorted['shift_lon'], df_s_sorted['shape_pt_lat'], df_s_sorted['shape_pt_lon']).fillna(0)
                            st.session_state.shape_dist = df_s_sorted.groupby('shape_id')['dist'].sum().reset_index()

                        if os.path.exists(os.path.join(temp_dir, "gtfs_data", "stops.txt")):
                            df_stops = pd.read_csv(os.path.join(temp_dir, "gtfs_data", "stops.txt")).dropna(subset=['stop_lat', 'stop_lon'])
                            st.session_state.df_stops = df_stops
                                
                        if os.path.exists(os.path.join(temp_dir, "gtfs_data", "stop_times.txt")):
                            df_st = pd.read_csv(os.path.join(temp_dir, "gtfs_data", "stop_times.txt"))
                            df_st['trip_id'] = df_st['trip_id'].astype(str).str.strip().str.upper()
                            st.session_state.df_stop_times = df_st

                        # ==========================================
                        # 4. HISTORI DO, DISPATCH, & MIKROTRIP
                        # ==========================================
                        list_histori = []
                        
                        def filter_columns(cols):
                            return [c for c in cols if any(x in str(c).strip().lower() for x in ['kode trip', 'rute real', 'jam start', 'jam end', 'tanggal', 'kategori', 'jenis do', 'aktual mulai', 'aktual selesai'])]

                        # --- PROSES DO EXCEL & CSV ---
                        if drive_link:
                            f_id = extract_drive_id(drive_link)
                            if f_id:
                                out_f = os.path.join(temp_dir, "hist")
                                gdown.download_folder(id=f_id, output=out_f, quiet=True, use_cookies=False)
                                for f in glob.glob(os.path.join(out_f, "**", "*"), recursive=True):
                                    if os.path.isfile(f):
                                        if "dispatch" in f.lower() or "mikrotrip" in f.lower(): continue
                                        try:
                                            if f.lower().endswith('.csv'):
                                                df_t = pd.read_csv(f, sep=';', on_bad_lines='skip', dtype=str)
                                                if len(df_t.columns) < 3: df_t = pd.read_csv(f, sep=',', on_bad_lines='skip', dtype=str)
                                                df_t.columns = df_t.columns.astype(str).str.strip()
                                                c_kat = next((c for c in df_t.columns if 'kategori' in str(c).lower()), None)
                                                if c_kat: df_t = df_t[df_t[c_kat].astype(str).str.lower().isin(['do reguler', 'do bko'])]
                                                list_histori.append(df_t)
                                            elif f.lower().endswith('.xlsx') or f.lower().endswith('.xls'):
                                                hdr = 0 if 'Kode Trip' in pd.read_excel(f, nrows=3, engine='openpyxl').columns else 1
                                                scols = pd.read_excel(f, nrows=0, header=hdr, engine='openpyxl').columns
                                                df_t = pd.read_excel(f, header=hdr, usecols=filter_columns(scols), engine='openpyxl')
                                                c_kat = next((c for c in df_t.columns if 'kategori' in str(c).lower()), None)
                                                if c_kat: df_t = df_t[df_t[c_kat].astype(str).str.lower().isin(['do reguler', 'do bko'])]
                                                list_histori.append(df_t)
                                        except: pass
                        elif history_uploads:
                            for u_file in history_uploads:
                                try:
                                    if u_file.name.lower().endswith('.csv'):
                                        df_t = pd.read_csv(u_file, sep=';', on_bad_lines='skip', dtype=str)
                                        if len(df_t.columns) < 3: 
                                            u_file.seek(0)
                                            df_t = pd.read_csv(u_file, sep=',', on_bad_lines='skip', dtype=str)
                                        df_t.columns = df_t.columns.astype(str).str.strip()
                                        c_kat = next((c for c in df_t.columns if 'kategori' in str(c).lower()), None)
                                        if c_kat: df_t = df_t[df_t[c_kat].astype(str).str.lower().isin(['do reguler', 'do bko'])]
                                        list_histori.append(df_t)
                                    else:
                                        hdr = 0 if 'Kode Trip' in pd.read_excel(u_file, nrows=3, engine='openpyxl').columns else 1
                                        u_file.seek(0)
                                        scols = pd.read_excel(u_file, nrows=0, header=hdr, engine='openpyxl').columns
                                        u_file.seek(0)
                                        df_t = pd.read_excel(u_file, header=hdr, usecols=filter_columns(scols), engine='openpyxl')
                                        c_kat = next((c for c in df_t.columns if 'kategori' in str(c).lower()), None)
                                        if c_kat: df_t = df_t[df_t[c_kat].astype(str).str.lower().isin(['do reguler', 'do bko'])]
                                        list_histori.append(df_t)
                                except: pass

                        # --- PROSES DISPATCH CSV & EXCEL ---
                        def process_dispatch(df_d):
                            df_d.columns = df_d.columns.astype(str).str.strip()
                            df_d = df_d.rename(columns={c: 'Jenis DO' if 'jenis do' in c.lower() else 'Kode Trip' if 'kode trip' in c.lower() else 'Rute Real' if 'nama trip' in c.lower() else 'Jam Start Do' if 'aktual mulai' in c.lower() else 'Jam End Do' if 'aktual selesai' in c.lower() else 'Tanggal Start DO' if 'tanggal' in c.lower() else c for c in df_d.columns})
                            if 'Jenis DO' in df_d.columns: df_d = df_d[df_d['Jenis DO'].astype(str).str.lower() == 'reguler']
                            return df_d[[c for c in ["Kode Trip", "Rute Real", "Jam Start Do", "Jam End Do", "Tanggal Start DO"] if c in df_d.columns]]

                        if dispatch_link:
                            f_id2 = extract_drive_id(dispatch_link)
                            if f_id2:
                                out_d = os.path.join(temp_dir, "disp")
                                gdown.download_folder(id=f_id2, output=out_d, quiet=True, use_cookies=False)
                                for f in glob.glob(os.path.join(out_d, "**", "*"), recursive=True):
                                    if os.path.isfile(f):
                                        try:
                                            if f.lower().endswith('.csv'):
                                                df_d = pd.read_csv(f, sep=';', dtype=str, on_bad_lines='skip')
                                                if len(df_d.columns) < 3: df_d = pd.read_csv(f, sep=',', dtype=str, on_bad_lines='skip')
                                            elif f.lower().endswith('.xlsx') or f.lower().endswith('.xls'):
                                                df_d = pd.read_excel(f, dtype=str, engine='openpyxl')
                                            else: continue
                                            list_histori.append(process_dispatch(df_d))
                                        except: pass
                        elif dispatch_uploads:
                            for u_file in dispatch_uploads:
                                try:
                                    if u_file.name.lower().endswith('.csv'):
                                        df_d = pd.read_csv(u_file, sep=';', dtype=str, on_bad_lines='skip')
                                        if len(df_d.columns) < 3:
                                            u_file.seek(0)
                                            df_d = pd.read_csv(u_file, sep=',', dtype=str, on_bad_lines='skip')
                                    else:
                                        df_d = pd.read_excel(u_file, dtype=str, engine='openpyxl')
                                    list_histori.append(process_dispatch(df_d))
                                except: pass

                        # --- PROSES MIKROTRIP CSV & EXCEL ---
                        def process_mikrotrip(df_m):
                            df_m.columns = df_m.columns.astype(str).str.strip().str.lower()
                            col_map = {}
                            for c in df_m.columns:
                                c_l = str(c).strip().lower()
                                if 'tanggal' in c_l: col_map[c] = 'Tanggal Start DO'
                                elif 'kode_trip' in c_l: col_map[c] = 'Kode Trip'
                                elif 'namatrip' in c_l: col_map[c] = 'Rute Real'
                                elif 'berangkat' in c_l: col_map[c] = 'Jam Start Do'
                                elif 'tiba' in c_l: col_map[c] = 'Jam End Do'
                            if col_map:
                                df_m = df_m.rename(columns=col_map)
                                if 'Kode Trip' in df_m.columns:
                                    df_out = df_m[[v for v in col_map.values() if v in df_m.columns]].copy()
                                    if 'Rute Real' in df_out.columns:
                                        df_out['Rute Real'] = df_out['Rute Real'].astype(str).str.replace(r'^\[.*?\]\s*', '', regex=True).str.replace(r'\s*>>\s*', ' - ', regex=True)
                                    return df_out
                            return pd.DataFrame()

                        if mikro_link:
                            f_id3 = extract_drive_id(mikro_link)
                            if f_id3:
                                out_m = os.path.join(temp_dir, "mikro")
                                gdown.download_folder(id=f_id3, output=out_m, quiet=True, use_cookies=False)
                                for f in glob.glob(os.path.join(out_m, "**", "*"), recursive=True):
                                    if os.path.isfile(f):
                                        try:
                                            if f.lower().endswith('.csv'):
                                                df_m = pd.read_csv(f, dtype=str, on_bad_lines='skip')
                                                if len(df_m.columns) < 3: df_m = pd.read_csv(f, sep=';', dtype=str, on_bad_lines='skip')
                                            elif f.lower().endswith('.xlsx') or f.lower().endswith('.xls'):
                                                df_m = pd.read_excel(f, dtype=str, engine='openpyxl')
                                            else: continue
                                            list_histori.append(process_mikrotrip(df_m))
                                        except: pass
                        elif mikro_uploads:
                            for u_file in mikro_uploads:
                                try:
                                    if u_file.name.lower().endswith('.csv'):
                                        df_m = pd.read_csv(u_file, dtype=str, on_bad_lines='skip')
                                        if len(df_m.columns) < 3:
                                            u_file.seek(0)
                                            df_m = pd.read_csv(u_file, sep=';', dtype=str, on_bad_lines='skip')
                                    else:
                                        df_m = pd.read_excel(u_file, dtype=str, engine='openpyxl')
                                    list_histori.append(process_mikrotrip(df_m))
                                except: pass

                        # --- GABUNGKAN SEMUA HISTORI ---
                        if list_histori:
                            df_histori = pd.concat(list_histori, ignore_index=True)
                            c_trip = next((c for c in df_histori.columns if 'kode trip' in str(c).lower()), None)
                            if c_trip:
                                df_histori = df_histori.dropna(subset=[c_trip])
                                df_histori = df_histori.rename(columns={c_trip: "trip_id"})
                                df_histori['trip_id'] = df_histori['trip_id'].astype(str).str.strip().str.upper()
                                df_histori = df_histori[df_histori['trip_id'] != '0']
                                
                                df_histori['route_id'] = df_histori['trip_id'].str.split('-').str[0].str.strip()
                                
                                c_real = next((c for c in df_histori.columns if 'rute real' in str(c).lower()), None)
                                if c_real: df_histori['route_name'] = df_histori[c_real].astype(str).str.replace(r'\s*\([^)]*\)$', '', regex=True)
                                else: df_histori['route_name'] = "-"

                                s_cols = [c for c in df_histori.columns if 'jam start' in c.lower() or 'aktual mulai' in c.lower() or 'berangkat' in c.lower()]
                                e_cols = [c for c in df_histori.columns if 'jam end' in c.lower() or 'aktual selesai' in c.lower() or 'tiba' in c.lower()]
                                t_cols = [c for c in df_histori.columns if 'tanggal' in c.lower()]
                                
                                if s_cols and e_cols:
                                    df_histori['j_s_str'] = df_histori[s_cols[0]]
                                    for c in s_cols[1:]: df_histori['j_s_str'] = df_histori['j_s_str'].fillna(df_histori[c])
                                    
                                    df_histori['j_e_str'] = df_histori[e_cols[0]]
                                    for c in e_cols[1:]: df_histori['j_e_str'] = df_histori['j_e_str'].fillna(df_histori[c])
                                    
                                    df_histori['j_s'] = pd.to_datetime(df_histori['j_s_str'].astype(str), errors='coerce')
                                    df_histori['j_e'] = pd.to_datetime(df_histori['j_e_str'].astype(str), errors='coerce')
                                    df_histori['duration_mins'] = (df_histori['j_e'] - df_histori['j_s']).dt.total_seconds() / 60.0
                                    df_histori.loc[df_histori['duration_mins'] < 0, 'duration_mins'] += 1440
                                    
                                    def cat_hr(h):
                                        if pd.isna(h): return "Lainnya"
                                        if 6 <= h < 9: return "Peak Pagi"
                                        elif 9 <= h < 16: return "Off Peak Siang"
                                        elif 16 <= h < 20: return "Peak Sore"
                                        else: return "Off Peak Malam"
                                    df_histori['Kategori Waktu'] = df_histori['j_s'].dt.hour.apply(cat_hr)
                                else:
                                    df_histori['duration_mins'], df_histori['Kategori Waktu'], df_histori['j_s'] = np.nan, "Lainnya", pd.NaT

                                if t_cols: 
                                    df_histori['tgl_str'] = df_histori[t_cols[0]]
                                    for tc in t_cols[1:]: df_histori['tgl_str'] = df_histori['tgl_str'].fillna(df_histori[tc])
                                    
                                    dates_str = df_histori['tgl_str'].astype(str).str.split(' ').str[0]
                                    parsed_dates = pd.to_datetime(dates_str, errors='coerce')
                                    mask_nat = parsed_dates.isna()
                                    if mask_nat.any():
                                        parsed_dates[mask_nat] = pd.to_datetime(dates_str[mask_nat], errors='coerce', dayfirst=True)
                                    df_histori['tanggal_merge'] = parsed_dates.dt.date
                                else: 
                                    df_histori['tanggal_merge'] = pd.NaT
                                
                                set_histori = set(df_histori['trip_id'])
                                st.session_state.df_histori_full = df_histori

                                if st.session_state.df_stops is not None and st.session_state.df_stop_times is not None:
                                    t_usage = df_histori['trip_id'].value_counts().reset_index()
                                    t_usage.columns = ['trip_id', 'usage_count']
                                    st_s = pd.merge(st.session_state.df_stop_times, st.session_state.df_stops, on='stop_id')
                                    m_st = pd.merge(t_usage, st_s.drop_duplicates(['trip_id', 'stop_name']), on='trip_id')
                                    
                                    df_hp = m_st.groupby('stop_name').agg({'usage_count': 'sum', 'stop_lat': 'mean', 'stop_lon': 'mean'}).reset_index().sort_values('usage_count', ascending=False)
                                    df_hp['is_halte'] = df_hp['stop_name'].isin(LIST_HALTE)
                                    st.session_state.df_halte_padat = df_hp
                            else: set_histori = set(); st.session_state.df_histori_full = pd.DataFrame()
                        else: set_histori = set(); st.session_state.df_histori_full = pd.DataFrame()

                        # ==========================================
                        # 5. KOMPARASI & PRIME TRIPS
                        # ==========================================
                        master_data = []
                        histori_counts = df_histori['trip_id'].value_counts().to_dict() if not st.session_state.df_histori_full.empty else {}
                        for t_id in (set_transit | set_gtfs | set_histori):
                            if t_id == '0': continue
                            master_data.append({
                                'Trip_ID': t_id, 'Route': t_id.split('-')[0],
                                'Nama Trip GTFS': str(gtfs_mapping.get(t_id, "-")),
                                'Nama Trip Transit': str(api_mapping.get(t_id, "-")),
                                'Di_API': t_id in set_transit, 'Di_GTFS': t_id in set_gtfs, 'Digunakan': t_id in set_histori,
                                'Jumlah Trip': histori_counts.get(t_id, 0)
                            })
                        st.session_state.df_master = pd.DataFrame(master_data).sort_values('Trip_ID').reset_index(drop=True)

                        most_freq_list = []
                        if not st.session_state.df_histori_full.empty:
                            df_h = st.session_state.df_histori_full
                            df_h['Jenis Layanan'] = df_h['route_id'].map(MASTER_LAYANAN).fillna("Lainnya")
                            t_counts = df_h.groupby(['route_id', 'trip_id']).size().reset_index(name='Usage Count')
                            
                            for r_id in gtfs_unique_routes:
                                r_data = t_counts[t_counts['route_id'] == r_id].sort_values('Usage Count', ascending=False)
                                if not r_data.empty:
                                    pts = r_data.iloc[0]['trip_id'].split('-')
                                    top_t = r_data.head(2) if (len(pts)>1 and pts[-1].startswith('R')) else r_data.head(1)
                                    for _, row in top_t.iterrows():
                                        t_id = row['trip_id']
                                        df_c = df_h[(df_h['trip_id'] == t_id) & (df_h['Kategori Waktu'].isin(['Peak Pagi', 'Peak Sore']))]
                                        avg_m = get_iqr_avg(df_c)
                                                
                                        avg_time_str = format_time(avg_m)
                                        avg_speed_str = "-"
                                        if st.session_state.shape_dist is not None:
                                            shape_id = str(df_gtfs[df_gtfs['trip_id'] == t_id]['shape_id'].iloc[0]).strip() if not df_gtfs[df_gtfs['trip_id'] == t_id].empty else None
                                            if shape_id:
                                                dist_row = st.session_state.shape_dist[st.session_state.shape_dist['shape_id'] == shape_id]
                                                if not dist_row.empty and avg_m > 0:
                                                    calc_speed = dist_row['dist'].iloc[0] / (avg_m / 60.0)
                                                    if 5 <= calc_speed <= 90:
                                                        avg_speed_str = format_speed(calc_speed)

                                        most_freq_list.append({
                                            'Route_ID': r_id, 'Trip_ID': t_id, 'Usage Count': int(row['Usage Count']),
                                            'Avg Waktu Tempuh': avg_time_str, 'Avg Kecepatan': avg_speed_str,
                                            'Jenis Layanan': MASTER_LAYANAN.get(r_id, "Lainnya"), 'Avg_Mins_Peak': avg_m
                                        })
                        st.session_state.df_most_frequent = pd.DataFrame(most_freq_list).sort_values('Trip_ID').reset_index(drop=True)
                        st.session_state.data_processed = True
                        st.success("✅ Proses Selesai!")

                    except Exception as e:
                        st.error(f"Error: {e}")
                    finally:
                        if os.path.exists(temp_dir): shutil.rmtree(temp_dir)

    # ==========================================
    # TAMPILAN HASIL CHECKER & ANALITIK
    # ==========================================
    if st.session_state.data_processed:
        tab_master, tab_freq, tab_speed, tab_lintasan, tab_halte, tab_chart, tab_komplain, tab_bus = st.tabs([
            "📋 Tabel Checker", "🔥 Prime Trip", "⏱️ Travel Speed", "🛣️ Lintasan Trip",
            "🚏 Halte Padat", "📊 Analitik Operasional", "📉 Analisis Komplain & Waktu", "🚌 Jumlah Bus Beredar"
        ])
        
        with tab_master:
            st.markdown("**Filter:**")
            f_col1, f_col2, f_col3 = st.columns(3)
            show_gtfs_only = f_col1.checkbox("Trip GTFS Only", value=False)
            show_api_only = f_col2.checkbox("Trip Transit Only", value=False)
            show_unused = f_col3.checkbox("Unused Trip", value=False)
            df_display = st.session_state.df_master.copy()
            if show_gtfs_only: df_display = df_display[(df_display['Di_GTFS'] == True) & (df_display['Di_API'] == False)]
            if show_api_only: df_display = df_display[(df_display['Di_API'] == True) & (df_display['Di_GTFS'] == False)]
            if show_unused: df_display = df_display[(df_display['Di_GTFS'] == True) & (df_display['Di_API'] == True) & (df_display['Digunakan'] == False)]
            
            st.dataframe(df_display, use_container_width=True, height=600)
            
        with tab_freq:
            df_mf_view = st.session_state.df_most_frequent.copy()
            if 'Avg_Mins_Peak' in df_mf_view.columns: df_mf_view = df_mf_view.drop(columns=['Avg_Mins_Peak'])
            layanan_filter = ["Semua Layanan"] + sorted(df_mf_view['Jenis Layanan'].unique().tolist())
            pilih_layanan = st.selectbox("Filter Jenis Layanan:", layanan_filter, key="layanan_prime")
            if pilih_layanan != "Semua Layanan": df_mf_view = df_mf_view[df_mf_view['Jenis Layanan'] == pilih_layanan]
            st.dataframe(df_mf_view, use_container_width=True, height=600)

        with tab_speed:
            st.markdown("### Analisis Performa Kecepatan Jaringan (Travel Speed)")
            st.write("Analisis kecepatan ini mengkorelasikan seluruh data DO dengan jarak rute riil (Shapes GTFS) untuk melihat rata-rata kecepatan per rute dan jenis layanan.")
            
            if st.session_state.df_histori_full is not None and st.session_state.shape_dist is not None:
                df_h = st.session_state.df_histori_full.copy()
                df_shape_d = st.session_state.shape_dist.copy()
                df_gtfs = st.session_state.df_gtfs_full.copy()
                
                waktu_filter = ["Semua Waktu", "Peak Pagi", "Off Peak Siang", "Peak Sore", "Off Peak Malam"]
                pilih_waktu = st.selectbox("Pilih Kategori Waktu:", waktu_filter)
                if pilih_waktu != "Semua Waktu": df_h = df_h[df_h['Kategori Waktu'] == pilih_waktu]
                
                if not df_h.empty:
                    df_h['Jenis Layanan'] = df_h['route_id'].map(MASTER_LAYANAN).fillna("Lainnya")
                    
                    speed_list = []
                    for t_id, grp in df_h.groupby('trip_id'):
                        avg_m = get_iqr_avg(grp)
                        if avg_m > 0:
                            shape_id = str(df_gtfs[df_gtfs['trip_id'] == t_id]['shape_id'].iloc[0]).strip() if not df_gtfs[df_gtfs['trip_id'] == t_id].empty else None
                            if shape_id:
                                dist_row = df_shape_d[df_shape_d['shape_id'] == shape_id]
                                if not dist_row.empty:
                                    calc_speed = dist_row['dist'].iloc[0] / (avg_m / 60.0)
                                    if 5 <= calc_speed <= 90:
                                        speed_list.append({
                                            'Trip_ID': t_id, 'Route_ID': t_id.split('-')[0],
                                            'Jenis Layanan': MASTER_LAYANAN.get(t_id.split('-')[0], "Lainnya"),
                                            'Total Usage': len(grp), 'Avg Mins': avg_m,
                                            'Distance (KM)': dist_row['dist'].iloc[0],
                                            'Speed (KM/H)': calc_speed
                                        })
                    
                    df_speed = pd.DataFrame(speed_list)
                    
                    if not df_speed.empty:
                        layanan_speed = ["Semua Layanan"] + sorted(df_speed['Jenis Layanan'].unique().tolist())
                        pilih_lay_speed = st.selectbox("Pilih Jenis Layanan:", layanan_speed)
                        if pilih_lay_speed != "Semua Layanan": df_speed = df_speed[df_speed['Jenis Layanan'] == pilih_lay_speed]
                        
                        col_sp1, col_sp2 = st.columns(2)
                        with col_sp1:
                            st.markdown("#### Top 10 Trip Tercepat")
                            df_fast = df_speed.sort_values('Speed (KM/H)', ascending=True).tail(10)
                            fig_f = px.bar(df_fast, x='Speed (KM/H)', y='Trip_ID', orientation='h', color='Speed (KM/H)', color_continuous_scale="Blues")
                            st.plotly_chart(fig_f, use_container_width=True)
                            
                        with col_sp2:
                            st.markdown("#### Top 10 Trip Terlambat")
                            df_slow = df_speed.sort_values('Speed (KM/H)', ascending=True).head(10)
                            fig_s = px.bar(df_slow, x='Speed (KM/H)', y='Trip_ID', orientation='h', color='Speed (KM/H)', color_continuous_scale="Reds_r")
                            st.plotly_chart(fig_s, use_container_width=True)

                        st.markdown("#### Rekapitulasi Rata-Rata Kecepatan Berdasarkan Layanan")
                        df_agg_layanan = df_speed.groupby('Jenis Layanan')['Speed (KM/H)'].mean().reset_index().sort_values('Speed (KM/H)', ascending=False)
                        st.dataframe(df_agg_layanan.style.format({'Speed (KM/H)': "{:.2f}"}), use_container_width=True)

                        st.markdown("#### Data Tabel Kecepatan (Lengkap)")
                        st.dataframe(df_speed.sort_values('Trip_ID').reset_index(drop=True).style.format({'Speed (KM/H)': "{:.2f}", 'Distance (KM)': "{:.2f}", 'Avg Mins': "{:.1f}"}), use_container_width=True, height=400)
                    else: st.warning("Tidak ada data waktu tempuh valid yang dapat dikorelasikan dengan jarak rute.")
                else: st.warning("Data histori kosong untuk filter waktu ini.")

        with tab_lintasan:
            if st.session_state.df_shapes is not None and st.session_state.df_gtfs_full is not None:
                valid_routes = sorted(st.session_state.df_gtfs_full[st.session_state.df_gtfs_full['shape_id'].notna()]['route_id'].unique())
                col_rt, col_tp = st.columns(2)
                with col_rt: selected_route_lintasan = st.selectbox("Pilih Route ID:", ["Semua Route"] + list(valid_routes))
                
                valid_trips = sorted(st.session_state.df_gtfs_full[(st.session_state.df_gtfs_full['shape_id'].notna()) & (st.session_state.df_gtfs_full['route_id'] == selected_route_lintasan)]['trip_id'].unique()) if selected_route_lintasan != "Semua Route" else sorted(st.session_state.df_gtfs_full[st.session_state.df_gtfs_full['shape_id'].notna()]['trip_id'].unique())
                    
                with col_tp:
                    prime_trips_set = set(st.session_state.df_most_frequent['Trip_ID'].dropna())
                    def format_lintasan_option(t_id):
                        name = st.session_state.gtfs_mapping.get(t_id, "-")
                        base_str = f"{t_id} ({name})"
                        return f"🔥 {base_str} (Prime)" if t_id in prime_trips_set else base_str
                    selected_trip = st.selectbox("Pilih Kode Trip:", valid_trips, format_func=format_lintasan_option)
                
                if selected_trip:
                    usage, avg_daily, total_panjang = 0, 0.0, 0
                    df_h_filter = pd.DataFrame()
                    if st.session_state.df_histori_full is not None:
                        df_h_filter = st.session_state.df_histori_full[st.session_state.df_histori_full['trip_id'] == selected_trip].copy()
                        usage = len(df_h_filter)
                        if 'tanggal_merge' in df_h_filter.columns:
                            df_valid_dates = df_h_filter.dropna(subset=['tanggal_merge'])
                            if not df_valid_dates.empty: avg_daily = df_valid_dates.groupby('tanggal_merge').size().mean()
                    
                    shape_id = str(st.session_state.df_gtfs_full[st.session_state.df_gtfs_full['trip_id'] == selected_trip]['shape_id'].iloc[0]).strip()
                    df_shape_f = st.session_state.df_shapes[st.session_state.df_shapes['shape_id'] == shape_id].sort_values('shape_pt_sequence').copy()
                    if not df_shape_f.empty:
                        df_shape_f['dist'] = calc_haversine(df_shape_f['shape_pt_lat'].shift(), df_shape_f['shape_pt_lon'].shift(), df_shape_f['shape_pt_lat'], df_shape_f['shape_pt_lon'])
                        total_panjang = df_shape_f['dist'].sum()
                    
                    col_st1, col_st2, col_st3 = st.columns(3)
                    col_st1.metric("Total Penggunaan", f"{usage} trip")
                    col_st2.metric("Rata-rata Harian", f"{avg_daily:.1f} trip/hari")
                    col_st3.metric("Panjang Lintasan", f"{total_panjang:.2f} km")

                    st.markdown("##### ⏱️ Analisis Waktu Tempuh & Kecepatan")
                    c_pagi, c_siang, c_sore, c_malam = st.columns(4)
                    cats_mapping = {"Peak Pagi (06:00-08:59)": "Peak Pagi", "Off-Peak Siang (09:00-15:59)": "Off Peak Siang", "Peak Sore (16:00-19:59)": "Peak Sore", "Off-Peak Malam (20:00-05:59)": "Off Peak Malam"}
                    cols_cat = [c_pagi, c_siang, c_sore, c_malam]
                    for i, (label, cat_val) in enumerate(cats_mapping.items()):
                        df_c = df_h_filter[df_h_filter['Kategori Waktu'] == cat_val] if not df_h_filter.empty and 'Kategori Waktu' in df_h_filter.columns else pd.DataFrame()
                        avg_m = get_iqr_avg(df_c)
                        speed_val = (total_panjang / (avg_m / 60.0)) if avg_m > 0 and total_panjang > 0 else 0
                        speed_str = format_speed(speed_val) if 5 <= speed_val <= 90 else "-"
                        cols_cat[i].metric(label, format_time(avg_m), speed_str, delta_color="off")
                    
                    df_stops_t = pd.DataFrame()
                    if not df_shape_f.empty:
                        ScatterClass = go.Scattermap if hasattr(go, 'Scattermap') else go.Scattermapbox
                        fig_lin = go.Figure()
                        fig_lin.add_trace(ScatterClass(mode="lines", lat=df_shape_f['shape_pt_lat'], lon=df_shape_f['shape_pt_lon'], line=dict(color='#e74c3c', width=4), name="Jalur Rute", hoverinfo="skip"))
                        
                        if st.session_state.df_stop_times is not None and st.session_state.df_stops is not None:
                            df_st_trip = st.session_state.df_stop_times[st.session_state.df_stop_times['trip_id'] == selected_trip]
                            if not df_st_trip.empty:
                                df_stops_t = pd.merge(df_st_trip, st.session_state.df_stops, on='stop_id', how='inner').sort_values('stop_sequence')
                                fig_lin.add_trace(ScatterClass(mode="markers", lat=df_stops_t['stop_lat'], lon=df_stops_t['stop_lon'], marker=dict(size=10, color='#2980b9'), hovertext=df_stops_t['stop_name'], name="Halte", hoverinfo="text"))
                        layout_key = "map" if hasattr(go, 'Scattermap') else "mapbox"
                        fig_lin.update_layout(**{layout_key: dict(style="carto-positron", center=dict(lat=df_shape_f['shape_pt_lat'].mean(), lon=df_shape_f['shape_pt_lon'].mean()), zoom=11.5), "margin": {"r":0,"t":40,"l":0,"b":0}, "showlegend": False})
                        st.plotly_chart(fig_lin, use_container_width=True)

                    with st.expander("📊 Lihat Grafik Penggunaan Harian", expanded=False):
                        if not df_h_filter.empty and 'tanggal_merge' in df_h_filter.columns:
                            df_trend = df_h_filter.dropna(subset=['tanggal_merge']).groupby('tanggal_merge').size().reset_index(name='Jumlah_Trip')
                            df_trend['tanggal_merge'] = df_trend['tanggal_merge'].astype(str)
                            if not df_trend.empty:
                                fig_trend = px.line(df_trend, x='tanggal_merge', y='Jumlah_Trip', title="Tren Penggunaan Trip Setiap Hari", markers=True)
                                
                                peak_idx = df_trend['Jumlah_Trip'].idxmax()
                                peak_row = df_trend.loc[peak_idx]
                                fig_trend.add_annotation(x=peak_row['tanggal_merge'], y=peak_row['Jumlah_Trip'], text=f"PEAK ({peak_row['Jumlah_Trip']})", showarrow=True, arrowhead=1, ax=0, ay=-40, font=dict(color="red", size=12))
                                
                                st.plotly_chart(fig_trend, use_container_width=True)

                    with st.expander("📦 Lihat Analisis Outlier Waktu Tempuh Keseluruhan (Boxplot)", expanded=False):
                        if not df_h_filter.empty:
                            df_box = df_h_filter.dropna(subset=['duration_mins'])
                            if not df_box.empty:
                                fig_box = px.box(df_box, x='duration_mins', title="Boxplot Distribusi Waktu Tempuh (Menit)")
                                st.plotly_chart(fig_box, use_container_width=True)
                                
                    if not df_stops_t.empty:
                        with st.expander("📝 Lihat Daftar Halte yang Dilewati", expanded=False):
                            df_stops_t['Jarak Antar Segmen (km)'] = calc_haversine(df_stops_t['stop_lat'].shift(), df_stops_t['stop_lon'].shift(), df_stops_t['stop_lat'], df_stops_t['stop_lon']).fillna(0)
                            max_padat = 0
                            if st.session_state.df_halte_padat is not None:
                                padat_dict = st.session_state.df_halte_padat.set_index('stop_name')['usage_count'].to_dict()
                                df_stops_t['Kepadatan Halte (Trip/Bulan)'] = df_stops_t['stop_name'].map(padat_dict).fillna(0).astype(int)
                                max_padat = df_stops_t['Kepadatan Halte (Trip/Bulan)'].max()
                                if pd.isna(max_padat): max_padat = 0
                            else: df_stops_t['Kepadatan Halte (Trip/Bulan)'] = 0
                            
                            display_df = df_stops_t[['stop_sequence', 'stop_name', 'Jarak Antar Segmen (km)', 'Kepadatan Halte (Trip/Bulan)']].rename(columns={'stop_sequence': 'Urutan', 'stop_name': 'Nama Halte'})
                            display_df = display_df.sort_values('Urutan')
                            
                            if hasattr(display_df.style, 'map'):
                                styled_df = display_df.style.format({'Jarak Antar Segmen (km)': '{:.2f}'}).map(lambda x: color_kepadatan(x, max_padat), subset=['Kepadatan Halte (Trip/Bulan)']).map(color_red_distance, subset=['Jarak Antar Segmen (km)'])
                            else:
                                styled_df = display_df.style.format({'Jarak Antar Segmen (km)': '{:.2f}'}).applymap(lambda x: color_kepadatan(x, max_padat), subset=['Kepadatan Halte (Trip/Bulan)']).applymap(color_red_distance, subset=['Jarak Antar Segmen (km)'])
                            
                            st.dataframe(styled_df, use_container_width=True)

        with tab_halte:
            st.markdown("### Peta & Top 20 Titik Pemberhentian Terpadat")
            if st.session_state.df_halte_padat is not None and not st.session_state.df_halte_padat.empty:
                df_hp = st.session_state.df_halte_padat.copy()
                
                st.markdown("#### Peta Kepadatan Halte/Bus Stop")
                filter_map = st.radio("Tampilkan di Peta:", ["Semuanya", "Halte Saja", "Bus Stop Saja"], horizontal=True)
                
                df_hp_map = df_hp.dropna(subset=['stop_lat', 'stop_lon'])
                
                if filter_map == "Halte Saja": df_hp_map = df_hp_map[df_hp_map['is_halte'] == True]
                elif filter_map == "Bus Stop Saja": df_hp_map = df_hp_map[df_hp_map['is_halte'] == False]
                
                if not df_hp_map.empty:
                    try:
                        fig_map = px.density_mapbox(
                            df_hp_map, lat="stop_lat", lon="stop_lon", z="usage_count", 
                            radius=15, center=dict(lat=df_hp_map['stop_lat'].mean(), lon=df_hp_map['stop_lon'].mean()), 
                            zoom=10, mapbox_style="carto-positron", hover_name="stop_name"
                        )
                    except AttributeError:
                        fig_map = px.density_map(
                            df_hp_map, lat="stop_lat", lon="stop_lon", z="usage_count", 
                            radius=15, center=dict(lat=df_hp_map['stop_lat'].mean(), lon=df_hp_map['stop_lon'].mean()), 
                            zoom=10, map_style="carto-positron", hover_name="stop_name"
                        )
                    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                    st.plotly_chart(fig_map, use_container_width=True)
                else:
                    st.warning("Tidak ada titik koordinat yang dapat dipetakan untuk filter ini.")

                df_halte_brt = df_hp[df_hp['is_halte'] == True].sort_values('usage_count', ascending=False).head(20)
                df_bus_stop = df_hp[df_hp['is_halte'] == False].sort_values('usage_count', ascending=False).head(20)

                col_h1, col_h2 = st.columns(2)
                with col_h1:
                    st.markdown("**Top 20 Halte BRT**")
                    if not df_halte_brt.empty:
                        fig_brt = px.bar(df_halte_brt, x='usage_count', y='stop_name', orientation='h', color='usage_count', color_continuous_scale="Reds")
                        fig_brt.update_layout(yaxis={'categoryorder':'total ascending'}, margin={"r":0,"t":10,"l":0,"b":0})
                        st.plotly_chart(fig_brt, use_container_width=True)
                    else: st.info("Tidak ada data Halte BRT.")
                with col_h2:
                    st.markdown("**Top 20 Bus Stop / NFP**")
                    if not df_bus_stop.empty:
                        fig_bs = px.bar(df_bus_stop, x='usage_count', y='stop_name', orientation='h', color='usage_count', color_continuous_scale="Blues")
                        fig_bs.update_layout(yaxis={'categoryorder':'total ascending'}, margin={"r":0,"t":10,"l":0,"b":0})
                        st.plotly_chart(fig_bs, use_container_width=True)
                    else: st.info("Tidak ada data Bus Stop.")
                    
                st.markdown("---")
                st.markdown("### Tabel Daftar Analitik Seluruh Halte & Bus Stop")
                if st.session_state.df_histori_full is not None and not st.session_state.df_histori_full.empty and st.session_state.df_stop_times is not None and st.session_state.df_stops is not None:
                    df_h_temp = st.session_state.df_histori_full[['trip_id', 'route_id', 'tanggal_merge']].copy()
                    df_st_temp = pd.merge(st.session_state.df_stop_times, st.session_state.df_stops, on='stop_id')[['trip_id', 'stop_name']].drop_duplicates()
                    df_merged = pd.merge(df_h_temp, df_st_temp, on='trip_id', how='inner')
                    
                    if not df_merged.empty:
                        routes_per_stop = df_merged.groupby('stop_name')['route_id'].unique().apply(lambda x: ', '.join(sorted(x))).reset_index(name='Rute yang Melintas')
                        dominant_route = df_merged.groupby('stop_name')['route_id'].agg(lambda x: x.mode()[0] if not x.mode().empty else "-").reset_index(name='Rute Paling Dominan')
                        total_usage = df_merged.groupby('stop_name').size().reset_index(name='Jumlah Digunakan (Total)')
                        
                        jml_hari = df_merged['tanggal_merge'].nunique()
                        if jml_hari == 0: jml_hari = 1
                        total_usage['Rata-rata Bus Melintas Harian'] = (total_usage['Jumlah Digunakan (Total)'] / jml_hari).round(1)
                        
                        df_table_halte = pd.merge(total_usage, routes_per_stop, on='stop_name')
                        df_table_halte = pd.merge(df_table_halte, dominant_route, on='stop_name')
                        df_table_halte = df_table_halte.rename(columns={'stop_name': 'Nama Halte/Bus Stop'})
                        
                        df_table_halte = df_table_halte.sort_values('Rute Paling Dominan').reset_index(drop=True)
                        st.dataframe(df_table_halte, use_container_width=True)
                    else:
                        st.info("Data histori tidak mencukupi untuk memuat detail keseluruhan tabel ini.")
                else:
                    st.info("Data histori atau GTFS belum lengkap untuk memuat tabel analitik.")

                with st.expander("📉 Peta & Grafik Halte Tersepi (Jarang Digunakan)", expanded=False):
                    col_s1, col_s2 = st.columns(2)
                    df_halte_brt_sepi = df_hp[df_hp['is_halte'] == True].sort_values('usage_count', ascending=True).head(20)
                    df_bus_stop_sepi = df_hp[df_hp['is_halte'] == False].sort_values('usage_count', ascending=True).head(20)

                    with col_s1:
                        st.markdown("**Bottom 20 Halte BRT**")
                        if not df_halte_brt_sepi.empty:
                            fig_brt_sepi = px.bar(df_halte_brt_sepi, x='usage_count', y='stop_name', orientation='h', color='usage_count', color_continuous_scale="Reds")
                            fig_brt_sepi.update_layout(yaxis={'categoryorder':'total descending'}, margin={"r":0,"t":10,"l":0,"b":0})
                            st.plotly_chart(fig_brt_sepi, use_container_width=True)
                    with col_s2:
                        st.markdown("**Bottom 20 Bus Stop / NFP**")
                        if not df_bus_stop_sepi.empty:
                            fig_bs_sepi = px.bar(df_bus_stop_sepi, x='usage_count', y='stop_name', orientation='h', color='usage_count', color_continuous_scale="Blues")
                            fig_bs_sepi.update_layout(yaxis={'categoryorder':'total descending'}, margin={"r":0,"t":10,"l":0,"b":0})
                            st.plotly_chart(fig_bs_sepi, use_container_width=True)

        with tab_chart:
            st.markdown("### Kepadatan Operasional (Berdasarkan Histori)")
            if st.session_state.df_histori_full is not None:
                df_h = st.session_state.df_histori_full.copy()
                if not df_h.empty:
                    df_h['Jenis Layanan'] = df_h['route_id'].map(MASTER_LAYANAN).fillna("Lainnya")
                    df_h['Nama Rute Tampil'] = df_h['route_name'] + " (" + df_h['trip_id'] + ")"
                    selected_layanan = st.selectbox("Filter Layanan:", ["Semua Layanan"] + sorted(df_h['Jenis Layanan'].unique().tolist()), key="chart_layanan")
                    df_chart = df_h[df_h['Jenis Layanan'] == selected_layanan] if selected_layanan != "Semua Layanan" else df_h
                    if not df_chart.empty:
                        route_perf = df_chart.groupby('Nama Rute Tampil').size().reset_index(name='Total').sort_values('Total', ascending=False).head(20)
                        fig_bar = px.bar(route_perf, x='Total', y='Nama Rute Tampil', orientation='h', color='Total', color_continuous_scale="Blues")
                        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}, margin={"r":0,"t":10,"l":0,"b":0})
                        st.plotly_chart(fig_bar, use_container_width=True)

            st.markdown("---")
            st.markdown("### Analisis Segmen Halte (Jarak Terlalu Pendek)")
            st.write("Mendeteksi segmen antar halte yang jaraknya kurang dari batas tertentu.")
            
            batas_jarak = st.slider("Batas Jarak Jauh Segmen (KM):", min_value=0.05, max_value=1.0, value=0.20, step=0.05)
            
            if st.session_state.df_stop_times is not None and st.session_state.df_stops is not None and st.session_state.df_histori_full is not None and not st.session_state.df_histori_full.empty:
                df_hist = st.session_state.df_histori_full
                st_merged = pd.merge(st.session_state.df_stop_times, st.session_state.df_stops, on='stop_id', how='inner')
                st_merged = st_merged.sort_values(['trip_id', 'stop_sequence'])
                
                st_merged['next_stop'] = st_merged.groupby('trip_id')['stop_name'].shift(-1)
                st_merged['next_lat'] = st_merged.groupby('trip_id')['stop_lat'].shift(-1)
                st_merged['next_lon'] = st_merged.groupby('trip_id')['stop_lon'].shift(-1)
                
                segments = st_merged.dropna(subset=['next_stop']).copy()
                segments['distance_km'] = calc_haversine(segments['stop_lat'], segments['stop_lon'], segments['next_lat'], segments['next_lon'])
                
                active_trips = df_hist['trip_id'].unique()
                segments = segments[segments['trip_id'].isin(active_trips)]
                
                short_segments = segments[segments['distance_km'] < batas_jarak].copy()
                
                if not short_segments.empty:
                    short_segments['Segmen'] = short_segments['stop_name'] + " -> " + short_segments['next_stop']
                    
                    seg_grouped = short_segments.groupby('Segmen').agg(
                        Jumlah_Trip_Terdampak=('trip_id', 'nunique'),
                        Trip_ID=('trip_id', lambda x: ', '.join(sorted(set(x))))
                    ).reset_index()
                    
                    seg_grouped = seg_grouped.rename(columns={'Jumlah_Trip_Terdampak': 'Jumlah Trip Terdampak'})
                    seg_grouped = seg_grouped.sort_values('Trip_ID').reset_index(drop=True)
                    
                    st.dataframe(seg_grouped, use_container_width=True)
                else:
                    st.success("Tidak ada segmen antar halte yang berada di bawah batas jarak tersebut.")
            else:
                st.warning("Data GTFS atau Histori belum lengkap untuk analisis segmen.")

        with tab_komplain:
            st.markdown("### Korelasi Kinerja Operasional & Keluhan Pelanggan")
            if st.session_state.df_histori_full is not None and not st.session_state.df_histori_full.empty:
                df_h_all = st.session_state.df_histori_full.copy()
                selected_route_komplain = st.selectbox("Pilih Route ID untuk dianalisis:", sorted(df_h_all['route_id'].unique()), key="komplain_rute")
                
                if selected_route_komplain:
                    df_h_rute = df_h_all[df_h_all['route_id'] == selected_route_komplain].copy()
                    
                    st.markdown("#### 📌 Ringkasan Metrik Rute")
                    filter_waktu = st.radio("Filter Waktu Operasional:", ["Semua Rentang Waktu", "Peak Hour Saja"], horizontal=True)
                    
                    if filter_waktu == "Peak Hour Saja":
                        df_metric_filtered = df_h_rute[df_h_rute['j_s'].dt.hour.isin([6,7,8,16,17,18,19])]
                    else:
                        df_metric_filtered = df_h_rute
                    
                    avg_wait = df_metric_filtered['duration_mins'].mean() if not df_metric_filtered.empty else 0
                    prime_trip_count = len(df_metric_filtered)
                    
                    k1, k2 = st.columns(2)
                    k1.metric("Rata-rata Waktu Tempuh (Avg)", format_time(avg_wait))
                    k2.metric("Jumlah Trip Terlaksana", prime_trip_count)
                    st.markdown("---")

                    analisis_mode = st.radio("Mode Analisis:", ["Tren Harian", "Rincian Per Jam (Pilih Tanggal)"], horizontal=True)
                    
                    if analisis_mode == "Tren Harian":
                        if 'tanggal_merge' in df_metric_filtered.columns:
                            df_valid = df_metric_filtered.dropna(subset=['tanggal_merge', 'duration_mins'])
                            
                            prime_trips_for_route = []
                            if st.session_state.df_most_frequent is not None:
                                prime_trips_for_route = st.session_state.df_most_frequent[st.session_state.df_most_frequent['Route_ID'] == selected_route_komplain]['Trip_ID'].tolist()
                            
                            df_valid['Kategori Trip'] = df_valid['trip_id'].apply(lambda x: 'Prime Trip' if x in prime_trips_for_route else 'Trip Lainnya')
                            daily_counts = df_valid.groupby(['tanggal_merge', 'Kategori Trip']).size().unstack(fill_value=0).reset_index()
                            
                            if 'Prime Trip' not in daily_counts.columns: daily_counts['Prime Trip'] = 0
                            if 'Trip Lainnya' not in daily_counts.columns: daily_counts['Trip Lainnya'] = 0
                            daily_counts['Total Trip'] = daily_counts['Prime Trip'] + daily_counts['Trip Lainnya']
                            
                            df_prime_only = df_valid[df_valid['Kategori Trip'] == 'Prime Trip']
                            if not df_prime_only.empty:
                                daily_trip_time = df_prime_only.groupby(['tanggal_merge', 'trip_id']).apply(get_iqr_avg).reset_index(name='mean_time')
                                daily_time = daily_trip_time.groupby('tanggal_merge')['mean_time'].sum().reset_index(name='Waktu Tempuh (Mnt)')
                            else:
                                daily_time = pd.DataFrame(columns=['tanggal_merge', 'Waktu Tempuh (Mnt)'])
                            
                            df_plot = pd.merge(daily_counts, daily_time, on='tanggal_merge', how='outer').fillna(0)
                            df_plot['Komplain'] = 0
                            
                            if st.session_state.df_komplain is not None:
                                df_k = st.session_state.df_komplain
                                c_rute = next((c for c in df_k.columns if str(c).strip().lower() == 'kode rute'), None)
                                if c_rute:
                                    df_k_r = df_k[df_k[c_rute] == selected_route_komplain]
                                    if not df_k_r.empty:
                                        d_komp = df_k_r.groupby('tanggal_merge').size().reset_index(name='Komplain')
                                        df_plot = pd.merge(df_plot.drop(columns=['Komplain']), d_komp, on='tanggal_merge', how='left').fillna(0)
                            
                            df_plot = df_plot.sort_values('tanggal_merge')
                            df_plot['tanggal_str'] = pd.to_datetime(df_plot['tanggal_merge']).dt.strftime('%d-%m-%Y')
                            
                            fig = go.Figure()
                            # Area Chart untuk Kumulatif Seluruh Trip
                            fig.add_trace(go.Scatter(x=df_plot['tanggal_str'], y=df_plot['Total Trip'], fill='tozeroy', mode='none', name='Kumulatif Seluruh Trip', fillcolor='rgba(46, 204, 113, 0.3)', yaxis='y1'))
                            fig.add_trace(go.Scatter(x=df_plot['tanggal_str'], y=df_plot['Prime Trip'], mode='lines+markers', name='Prime Trip (Total)', line=dict(color='#3498db', width=2), yaxis='y1'))
                            fig.add_trace(go.Scatter(x=df_plot['tanggal_str'], y=df_plot['Trip Lainnya'], mode='lines+markers', name='Trip Lainnya (Total)', opacity=0.7, line=dict(color='#95a5a6', width=2), yaxis='y1'))
                            fig.add_trace(go.Scatter(x=df_plot['tanggal_str'], y=df_plot['Waktu Tempuh (Mnt)'], mode='lines+markers', name='Waktu Tempuh', line=dict(color='#f39c12', width=3), yaxis='y2'))
                            
                            avg_time_val = df_plot['Waktu Tempuh (Mnt)'].mean()
                            if avg_time_val > 0:
                                fig.add_hline(y=avg_time_val, line_dash="dash", line_color="#f39c12", yref="y2", annotation_text=f"Avg Waktu: {avg_time_val:.0f} Mnt", annotation_position="top left", annotation_font_color="#f39c12")

                            # Bar Chart hanya untuk Komplain
                            fig.add_trace(go.Bar(x=df_plot['tanggal_str'], y=df_plot['Komplain'], name='Jumlah Komplain', marker_color='rgba(231, 76, 60, 0.7)', yaxis='y3'))

                            y3_max = df_plot['Komplain'].max() + 2 if df_plot['Komplain'].max() > 0 else 5
                            fig.update_layout(
                                title=dict(text="Tren Kinerja & Komplain (Harian)"),
                                xaxis=dict(title=dict(text="Tanggal"), type='category', domain=[0.0, 0.85]),
                                yaxis=dict(title=dict(text="Volume Trip", font=dict(color="#2ecc71")), tickfont=dict(color="#2ecc71"), rangemode="tozero"),
                                yaxis2=dict(title=dict(text="Waktu Tempuh (Menit)", font=dict(color="#f39c12")), tickfont=dict(color="#f39c12"), anchor="x", overlaying="y", side="right", rangemode="tozero"),
                                yaxis3=dict(title=dict(text="Jumlah Komplain", font=dict(color="#e74c3c")), tickfont=dict(color="#e74c3c"), anchor="free", overlaying="y", side="right", position=0.95, range=[0, y3_max], dtick=1, rangemode="tozero"),
                                hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                            )
                            st.plotly_chart(fig, use_container_width=True)

                    else:
                        if 'tanggal_merge' in df_metric_filtered.columns:
                            available_dates = sorted(df_metric_filtered['tanggal_merge'].dropna().unique())
                            if available_dates:
                                selected_date = st.selectbox("Pilih Tanggal:", available_dates)
                                df_h_date = df_metric_filtered.dropna(subset=['j_s', 'duration_mins'])
                                df_h_date = df_h_date[df_h_date['tanggal_merge'] == selected_date].copy()
                                df_jam = pd.DataFrame({'Jam': range(24)})
                                
                                if not df_h_date.empty:
                                    df_h_date['Jam_Mulai'] = df_h_date['j_s'].dt.hour
                                    hourly_counts = df_h_date.groupby('Jam_Mulai').size().reset_index(name='Total Trip')
                                    hourly_time = df_h_date.groupby('Jam_Mulai').apply(get_iqr_avg).reset_index()
                                    hourly_time.columns = ['Jam_Mulai', 'Waktu Tempuh (Mnt)']
                                    df_jam = pd.merge(df_jam, hourly_counts, left_on='Jam', right_on='Jam_Mulai', how='left').fillna(0)
                                    df_jam = pd.merge(df_jam, hourly_time, left_on='Jam', right_on='Jam_Mulai', how='left').fillna(0)
                                else: 
                                    df_jam['Waktu Tempuh (Mnt)'] = 0
                                    df_jam['Total Trip'] = 0
                                    
                                df_jam['Komplain'] = 0
                                if st.session_state.df_komplain is not None:
                                    df_k = st.session_state.df_komplain
                                    c_rute = next((c for c in df_k.columns if str(c).strip().lower() == 'kode rute'), None)
                                    if c_rute:
                                        df_k_d = df_k[(df_k[c_rute] == selected_route_komplain) & (df_k['tanggal_merge'] == selected_date)]
                                        if not df_k_d.empty and 'jam_komplain' in df_k_d.columns:
                                            h_komp = df_k_d.groupby('jam_komplain').size().reset_index(name='Komplain')
                                            df_jam = pd.merge(df_jam.drop(columns=['Komplain']), h_komp, left_on='Jam', right_on='jam_komplain', how='left').fillna(0)
                                            
                                df_jam['Jam_Str'] = df_jam['Jam'].astype(str).str.zfill(2) + ":00"
                                
                                fig2 = go.Figure()
                                fig2.add_trace(go.Scatter(x=df_jam['Jam_Str'], y=df_jam['Total Trip'], fill='tozeroy', mode='none', name='Volume Trip', fillcolor='rgba(46, 204, 113, 0.3)', yaxis='y1'))
                                fig2.add_trace(go.Scatter(x=df_jam['Jam_Str'], y=df_jam['Waktu Tempuh (Mnt)'], mode='lines+markers', name='Waktu Tempuh', line=dict(color='#f39c12', width=3, shape='spline'), yaxis='y2'))
                                fig2.add_trace(go.Bar(x=df_jam['Jam_Str'], y=df_jam['Komplain'], name='Komplain', marker_color='rgba(231, 76, 60, 0.7)', yaxis='y3'))

                                avg_time_jam = df_jam[df_jam['Waktu Tempuh (Mnt)'] > 0]['Waktu Tempuh (Mnt)'].mean()
                                if pd.notna(avg_time_jam) and avg_time_jam > 0:
                                    fig2.add_hline(y=avg_time_jam, line_dash="dash", line_color="#f39c12", yref="y2", annotation_text=f"Avg Waktu: {avg_time_jam:.0f} Mnt", annotation_position="top left", annotation_font_color="#f39c12")

                                y3_max_jam = df_jam['Komplain'].max() + 2 if df_jam['Komplain'].max() > 0 else 3
                                fig2.update_layout(
                                    title=dict(text=f"Distribusi Waktu Tempuh, Volume, & Komplain Per Jam ({selected_date})"),
                                    xaxis=dict(title=dict(text="Jam Operasional"), type='category', tickangle=-45, domain=[0.0, 0.85]),
                                    yaxis=dict(title=dict(text="Volume Trip", font=dict(color="#2ecc71")), tickfont=dict(color="#2ecc71"), rangemode="tozero"),
                                    yaxis2=dict(title=dict(text="Waktu Tempuh (Menit)", font=dict(color="#f39c12")), tickfont=dict(color="#f39c12"), anchor="x", overlaying="y", side="right", rangemode="tozero"),
                                    yaxis3=dict(title=dict(text="Jumlah Komplain", font=dict(color="#e74c3c")), tickfont=dict(color="#e74c3c"), anchor="free", overlaying="y", side="right", position=0.95, range=[0, y3_max_jam], dtick=1, rangemode="tozero"),
                                    hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                                )
                                st.plotly_chart(fig2, use_container_width=True)

        with tab_bus:
            st.markdown("### Analisis Jumlah Bus Beredar")
            st.write("Tabel ini menghitung jumlah bus yang sedang beroperasi pada jam tertentu. Perhitungan didasarkan pada waktu mulai trip (start) ditambah dengan rata-rata waktu tempuh (average travel time) dari trip tersebut.")
            
            if st.session_state.df_histori_full is not None and not st.session_state.df_histori_full.empty:
                df_bus = st.session_state.df_histori_full.copy()
                df_bus = df_bus.dropna(subset=['j_s', 'tanggal_merge', 'duration_mins'])
                
                if not df_bus.empty:
                    avg_dur_df = df_bus.groupby('trip_id')['duration_mins'].mean().reset_index(name='avg_dur')
                    df_bus = df_bus.merge(avg_dur_df, on='trip_id', how='left')
                    
                    df_bus['estimasi_selesai'] = df_bus['j_s'] + pd.to_timedelta(df_bus['avg_dur'], unit='m')
                    
                    df_bus['start_d'] = df_bus['j_s'].dt.date
                    df_bus['end_d'] = df_bus['estimasi_selesai'].dt.date
                    df_bus['start_h'] = df_bus['j_s'].dt.hour
                    df_bus['end_h'] = df_bus['estimasi_selesai'].dt.hour
                    df_bus['Jenis Layanan'] = df_bus['route_id'].map(MASTER_LAYANAN).fillna("Lainnya")
                    
                    available_dates = sorted(df_bus['tanggal_merge'].unique())
                    available_hours = list(range(24))
                    
                    col_b1, col_b2 = st.columns(2)
                    with col_b1:
                        pilih_tgl_bus = st.selectbox("Pilih Tanggal:", ["Semua Tanggal (Rata-rata)"] + [str(d) for d in available_dates], key="bus_tgl")
                    with col_b2:
                        pilih_jam_bus = st.selectbox("Pilih Jam Operasional:", available_hours, index=5, key="bus_jam")
                        
                    same_day = df_bus['start_d'] == df_bus['end_d']
                    diff_day = df_bus['start_d'] < df_bus['end_d']
                    
                    hourly_counts = []
                    if pilih_tgl_bus == "Semua Tanggal (Rata-rata)":
                        for h in range(24):
                            cond_same_h = same_day & (df_bus['start_h'] <= h) & (df_bus['end_h'] >= h)
                            cond_diff_h = diff_day & ((h >= df_bus['start_h']) | (h <= df_bus['end_h']))
                            active_h = df_bus[cond_same_h | cond_diff_h]
                            
                            if h in [23, 0, 1, 2, 3, 4]:
                                active_h = active_h[(active_h['Jenis Layanan'] == 'BRT') | (active_h['route_id'].isin(['JAK.36', 'JAK.75', 'JAK.47', 'JAK.52']))]
                            
                            if not active_h.empty:
                                unique_dates_h = active_h['tanggal_merge'].nunique()
                                avg_active_h = len(active_h) / unique_dates_h if unique_dates_h > 0 else 0
                                hourly_counts.append({'Jam': f"{h:02d}:00", 'Jumlah Bus': avg_active_h})
                            else:
                                hourly_counts.append({'Jam': f"{h:02d}:00", 'Jumlah Bus': 0})
                    else:
                        df_bus_date = df_bus[df_bus['tanggal_merge'].astype(str) == pilih_tgl_bus]
                        same_day_d = df_bus_date['start_d'] == df_bus_date['end_d']
                        diff_day_d = df_bus_date['start_d'] < df_bus_date['end_d']
                        
                        for h in range(24):
                            cond_same_h = same_day_d & (df_bus_date['start_h'] <= h) & (df_bus_date['end_h'] >= h)
                            cond_diff_h = diff_day_d & ((h >= df_bus_date['start_h']) | (h <= df_bus_date['end_h']))
                            active_h = df_bus_date[cond_same_h | cond_diff_h]
                            
                            if h in [23, 0, 1, 2, 3, 4]:
                                active_h = active_h[(active_h['Jenis Layanan'] == 'BRT') | (active_h['route_id'].isin(['JAK.36', 'JAK.75', 'JAK.47', 'JAK.52']))]
                                
                            hourly_counts.append({'Jam': f"{h:02d}:00", 'Jumlah Bus': len(active_h)})
                            
                    df_hourly_trend = pd.DataFrame(hourly_counts)
                    fig_bus_trend = px.line(df_hourly_trend, x='Jam', y='Jumlah Bus', markers=True, title=f"Tren Seluruh Bus Beredar per Jam ({pilih_tgl_bus})", line_shape="spline")
                    fig_bus_trend.update_layout(yaxis_title="Total Bus Aktif", xaxis_title="Jam Operasional")
                    st.plotly_chart(fig_bus_trend, use_container_width=True)

                    st.markdown(f"#### Rincian Rute Beroperasi pada Jam {pilih_jam_bus}:00")
                    
                    cond_same = same_day & (df_bus['start_h'] <= pilih_jam_bus) & (df_bus['end_h'] >= pilih_jam_bus)
                    cond_diff = diff_day & ((pilih_jam_bus >= df_bus['start_h']) | (pilih_jam_bus <= df_bus['end_h']))
                    
                    df_active = df_bus[cond_same | cond_diff].copy()
                    
                    if pilih_jam_bus in [23, 0, 1, 2, 3, 4]:
                        df_active = df_active[(df_active['Jenis Layanan'] == 'BRT') | (df_active['route_id'].isin(['JAK.36', 'JAK.75', 'JAK.47', 'JAK.52']))]
                        
                    if pilih_tgl_bus == "Semua Tanggal (Rata-rata)":
                        if not df_active.empty:
                            daily_count = df_active.groupby(['route_id', 'tanggal_merge']).size().reset_index(name='count')
                            avg_count = daily_count.groupby('route_id')['count'].mean().reset_index(name='Jumlah Bus Beredar')
                            avg_count['Jumlah Bus Beredar'] = avg_count['Jumlah Bus Beredar'].round(1)
                            avg_count['Jenis Layanan'] = avg_count['route_id'].map(MASTER_LAYANAN).fillna("Lainnya")
                            avg_count = avg_count[['route_id', 'Jenis Layanan', 'Jumlah Bus Beredar']].sort_values('route_id').reset_index(drop=True)
                            st.dataframe(avg_count, use_container_width=True)
                        else:
                            st.warning(f"Tidak ada bus yang beredar pada jam {pilih_jam_bus}:00 secara keseluruhan.")
                    else:
                        df_active_date = df_active[df_active['tanggal_merge'].astype(str) == pilih_tgl_bus]
                        if not df_active_date.empty:
                            count_date = df_active_date.groupby('route_id').size().reset_index(name='Jumlah Bus Beredar')
                            count_date['Jenis Layanan'] = count_date['route_id'].map(MASTER_LAYANAN).fillna("Lainnya")
                            count_date = count_date[['route_id', 'Jenis Layanan', 'Jumlah Bus Beredar']].sort_values('route_id').reset_index(drop=True)
                            st.dataframe(count_date, use_container_width=True)
                        else:
                            st.warning(f"Tidak ada bus yang beredar pada tanggal {pilih_tgl_bus} di jam {pilih_jam_bus}:00.")
                else:
                    st.warning("Data operasional tidak memiliki waktu yang valid.")
            else:
                st.warning("Data histori belum diunggah.")

        # ==========================================
        # EXPORT DATABASE BINER (.PKL) UNTUK PUBLIC DASHBOARD
        # ==========================================
        st.markdown("---")
        st.subheader("📦 Export Database Memory (.pkl)")
        st.write("Ekspor seluruh hasil komparasi bulan ini menjadi satu file biner. File ini yang akan dibaca otomatis oleh Public Dashboard.")
        
        export_month = st.text_input("Nama File / Bulan (Contoh: September_2026)", "September_2026")
        
        if st.button("Siapkan File .pkl untuk Diunduh", type="primary"):
            with st.spinner("Sedang memproses file database..."):
                export_data = {
                    'df_master': st.session_state.df_master,
                    'df_most_frequent': st.session_state.df_most_frequent,
                    'df_shapes': st.session_state.df_shapes,
                    'df_gtfs_full': st.session_state.df_gtfs_full,
                    'df_histori_full': st.session_state.df_histori_full,
                    'df_stops': st.session_state.df_stops,
                    'df_stop_times': st.session_state.df_stop_times,
                    'df_halte_padat': st.session_state.df_halte_padat,
                    'shape_dist': st.session_state.shape_dist,
                    'df_komplain': st.session_state.df_komplain,
                    'gtfs_mapping': st.session_state.gtfs_mapping
                }
                st.session_state.pkl_bytes = pickle.dumps(export_data)
                st.session_state.pkl_ready_name = f"Database_{export_month}.pkl"
                
        if st.session_state.pkl_bytes is not None:
            st.success(f"File {st.session_state.pkl_ready_name} siap diunduh!")
            st.download_button(
                label=f"⬇️ Download {st.session_state.pkl_ready_name}", 
                data=st.session_state.pkl_bytes, 
                file_name=st.session_state.pkl_ready_name, 
                mime="application/octet-stream",
                type="primary"
            )

elif menu == "📥 Data Downloader":
    st.title("📥 Data Downloader")
    st.write("Download master data rute Transit menjadi file Excel.")
    
    if st.button("🌐 Download Data API Master"):
        with st.spinner("Processing..."):
            try:
                resp = requests.get("http://transit.transjakarta.co.id:8182/api/v1/master/rute-table", timeout=20).json()
                api_response = resp['data'] if isinstance(resp, dict) and 'data' in resp else resp
                st.session_state.api_download_df = pd.DataFrame(api_response)
                st.success(f"Berhasil menarik {len(st.session_state.api_download_df)} baris data!")
            except Exception as e: st.error(f"Error: {e}")
                
    if st.session_state.api_download_df is not None:
        st.dataframe(st.session_state.api_download_df.head(5), use_container_width=True)
        st.download_button(label="📥 Download Data Master Rute Transit (.xlsx)", data=to_excel(st.session_state.api_download_df), file_name='Master_Rute_Transit.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', type="primary")