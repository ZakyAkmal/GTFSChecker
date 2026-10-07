import streamlit as st
import pandas as pd
import io
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pickle
import requests

st.set_page_config(page_title="Public Dashboard Transit", page_icon="📊", layout="wide")

# ==========================================
# DATA STATIS: JENIS LAYANAN & DAFTAR HALTE
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
    "4C": "IPLK", "4E": "Rusun", "4F": "IPLK", "4K": "IPLK", "5B": "IPLK", "51ST": "IPLK",
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
    "Kejaksaan Agung", "Cakung", "Petukangan D'MASIV", "Senen Bank Jakarta", "Kelapa Dua Sasak",
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
if 'api_download_df' not in st.session_state: st.session_state.api_download_df = None

# --- FUNGSI UTILITAS ---
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
    v_dur = v_dur[v_dur <= 300]
    if v_dur.empty: return 0
    if len(v_dur) == 1: return v_dur.iloc[0]
    q1, q3 = v_dur.quantile(0.25), v_dur.quantile(0.75)
    filt = v_dur[(v_dur >= max(0, q1 - 1.5 * (q3-q1))) & (v_dur <= q3 + 1.5 * (q3-q1))]
    return filt.mean() if not filt.empty else 0

# --- FUNGSI CACHE MAGIC (ANTI LEMOT) ---
@st.cache_data(show_spinner=False)
def load_database(file_bytes):
    return pickle.loads(file_bytes)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🚇 Navigasi Menu")
menu = st.sidebar.radio("Pilih Fitur:", ["📊 Public Dashboard", "📥 Data Downloader"])

if menu == "📊 Public Dashboard":
    # --- UI UTAMA DASHBOARD ---
    st.title("🚇 Dashboard Analitik Transit (Viewer)")
    st.write("Silakan unggah file database `.pkl` yang telah diekspor dari aplikasi Checker.")
    st.markdown("---")

    pkl_file = st.file_uploader("Upload File Database (.pkl) 📦", type=["pkl"])

    if pkl_file is not None:
        with st.spinner("🚀 Memuat data ke dalam RAM Server (Hanya 1x saat pertama kali upload)..."):
            try:
                data = load_database(pkl_file.getvalue())
                
                df_master = data.get('df_master')
                df_most_frequent = data.get('df_most_frequent')
                df_shapes = data.get('df_shapes')
                df_gtfs_full = data.get('df_gtfs_full')
                df_histori_full = data.get('df_histori_full')
                df_stops = data.get('df_stops')
                df_stop_times = data.get('df_stop_times')
                df_halte_padat = data.get('df_halte_padat')
                shape_dist = data.get('shape_dist')
                df_komplain = data.get('df_komplain')
                gtfs_mapping = data.get('gtfs_mapping', {})
                
                st.success("✅ Database berhasil dimuat! Perpindahan Tab dan Dropdown sekarang akan sangat cepat.")
                
                # ==========================================
                # MULAI DARI SINI ADALAH KODE VISUALISASI UTUH
                # ==========================================
                tab_master, tab_freq, tab_speed, tab_lintasan, tab_halte, tab_chart, tab_komplain_ui, tab_bus = st.tabs([
                    "📋 Tabel Checker", "🔥 Prime Trip", "⏱️ Travel Speed", "🛣️ Lintasan Trip",
                    "🚏 Halte Padat", "📊 Analitik Operasional", "📉 Analisis Komplain & Waktu", "🚌 Jumlah Bus Beredar"
                ])
                
                with tab_master:
                    st.markdown("**Filter:**")
                    f_col1, f_col2, f_col3 = st.columns(3)
                    show_gtfs_only = f_col1.checkbox("Trip GTFS Only", value=False)
                    show_api_only = f_col2.checkbox("Trip Transit Only", value=False)
                    show_unused = f_col3.checkbox("Unused Trip", value=False)
                    df_display = df_master.copy()
                    if show_gtfs_only: df_display = df_display[(df_display['Di_GTFS'] == True) & (df_display['Di_API'] == False)]
                    if show_api_only: df_display = df_display[(df_display['Di_API'] == True) & (df_display['Di_GTFS'] == False)]
                    if show_unused: df_display = df_display[(df_display['Di_GTFS'] == True) & (df_display['Di_API'] == True) & (df_display['Digunakan'] == False)]
                    
                    st.dataframe(df_display, use_container_width=True, height=600)
                    
                with tab_freq:
                    df_mf_view = df_most_frequent.copy()
                    if 'Avg_Mins_Peak' in df_mf_view.columns: df_mf_view = df_mf_view.drop(columns=['Avg_Mins_Peak'])
                    layanan_filter = ["Semua Layanan"] + sorted(df_mf_view['Jenis Layanan'].unique().tolist())
                    pilih_layanan = st.selectbox("Filter Jenis Layanan:", layanan_filter, key="layanan_prime")
                    if pilih_layanan != "Semua Layanan": df_mf_view = df_mf_view[df_mf_view['Jenis Layanan'] == pilih_layanan]
                    st.dataframe(df_mf_view, use_container_width=True, height=600)

                with tab_speed:
                    st.markdown("### Analisis Performa Kecepatan Jaringan (Travel Speed)")
                    st.write("Analisis kecepatan ini mengkorelasikan seluruh data DO dengan jarak rute riil (Shapes GTFS) untuk melihat rata-rata kecepatan per rute dan jenis layanan.")
                    
                    if df_histori_full is not None and shape_dist is not None:
                        df_h = df_histori_full.copy()
                        df_shape_d = shape_dist.copy()
                        df_gtfs = df_gtfs_full.copy()
                        
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
                    if df_shapes is not None and df_gtfs_full is not None:
                        valid_routes = sorted(df_gtfs_full[df_gtfs_full['shape_id'].notna()]['route_id'].unique())
                        col_rt, col_tp = st.columns(2)
                        with col_rt: selected_route_lintasan = st.selectbox("Pilih Route ID:", ["Semua Route"] + list(valid_routes))
                        
                        valid_trips = sorted(df_gtfs_full[(df_gtfs_full['shape_id'].notna()) & (df_gtfs_full['route_id'] == selected_route_lintasan)]['trip_id'].unique()) if selected_route_lintasan != "Semua Route" else sorted(df_gtfs_full[df_gtfs_full['shape_id'].notna()]['trip_id'].unique())
                            
                        with col_tp:
                            prime_trips_set = set(df_most_frequent['Trip_ID'].dropna())
                            def format_lintasan_option(t_id):
                                name = gtfs_mapping.get(t_id, "-")
                                base_str = f"{t_id} ({name})"
                                return f"🔥 {base_str} (Prime)" if t_id in prime_trips_set else base_str
                            selected_trip = st.selectbox("Pilih Kode Trip:", valid_trips, format_func=format_lintasan_option)
                        
                        if selected_trip:
                            usage, avg_daily, total_panjang = 0, 0.0, 0
                            df_h_filter = pd.DataFrame()
                            if df_histori_full is not None:
                                df_h_filter = df_histori_full[df_histori_full['trip_id'] == selected_trip].copy()
                                usage = len(df_h_filter)
                                if 'tanggal_merge' in df_h_filter.columns:
                                    df_valid_dates = df_h_filter.dropna(subset=['tanggal_merge'])
                                    if not df_valid_dates.empty: avg_daily = df_valid_dates.groupby('tanggal_merge').size().mean()
                            
                            shape_id = str(df_gtfs_full[df_gtfs_full['trip_id'] == selected_trip]['shape_id'].iloc[0]).strip()
                            df_shape_f = df_shapes[df_shapes['shape_id'] == shape_id].sort_values('shape_pt_sequence').copy()
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
                                
                                if df_stop_times is not None and df_stops is not None:
                                    df_st_trip = df_stop_times[df_stop_times['trip_id'] == selected_trip]
                                    if not df_st_trip.empty:
                                        df_stops_t = pd.merge(df_st_trip, df_stops, on='stop_id', how='inner').sort_values('stop_sequence')
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
                                    if not df_shape_f.empty:
                                        df_shape_f['cum_dist'] = df_shape_f['dist'].cumsum()
                                        stop_cum_dists = []
                                        for _, row in df_stops_t.iterrows():
                                            dists = (df_shape_f['shape_pt_lat'] - row['stop_lat'])**2 + (df_shape_f['shape_pt_lon'] - row['stop_lon'])**2
                                            closest_idx = dists.idxmin()
                                            stop_cum_dists.append(df_shape_f.loc[closest_idx, 'cum_dist'])
                                        df_stops_t['cum_dist'] = stop_cum_dists
                                        df_stops_t = df_stops_t.sort_values('cum_dist')
                                        df_stops_t['Jarak Antar Segmen (km)'] = df_stops_t['cum_dist'].diff().fillna(0)
                                        df_stops_t.loc[df_stops_t['Jarak Antar Segmen (km)'] < 0, 'Jarak Antar Segmen (km)'] = 0
                                    else:
                                        df_stops_t['Jarak Antar Segmen (km)'] = calc_haversine(df_stops_t['stop_lat'].shift(), df_stops_t['stop_lon'].shift(), df_stops_t['stop_lat'], df_stops_t['stop_lon']).fillna(0)
                                    
                                    max_padat = 0
                                    if df_halte_padat is not None:
                                        padat_dict = df_halte_padat.set_index('stop_name')['usage_count'].to_dict()
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
                    if df_halte_padat is not None and not df_halte_padat.empty:
                        df_hp = df_halte_padat.copy()
                        
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
                        with col_
