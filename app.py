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
                        with col_h2:
                            st.markdown("**Top 20 Bus Stop / NFP**")
                            if not df_bus_stop.empty:
                                fig_bs = px.bar(df_bus_stop, x='usage_count', y='stop_name', orientation='h', color='usage_count', color_continuous_scale="Blues")
                                fig_bs.update_layout(yaxis={'categoryorder':'total ascending'}, margin={"r":0,"t":10,"l":0,"b":0})
                                st.plotly_chart(fig_bs, use_container_width=True)
                            else: st.info("Tidak ada data Bus Stop.")
                            
                        st.markdown("---")
                        st.markdown("### Tabel Daftar Analitik Seluruh Halte & Bus Stop")
                        if df_histori_full is not None and not df_histori_full.empty and df_stop_times is not None and df_stops is not None:
                            df_h_temp = df_histori_full[['trip_id', 'route_id', 'tanggal_merge']].copy()
                            df_st_temp = pd.merge(df_stop_times, df_stops, on='stop_id')[['trip_id', 'stop_name']].drop_duplicates()
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
                    if df_histori_full is not None:
                        df_h = df_histori_full.copy()
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
                    
                    if df_stop_times is not None and df_stops is not None and df_histori_full is not None and not df_histori_full.empty:
                        df_hist = df_histori_full
                        st_merged = pd.merge(df_stop_times, df_stops, on='stop_id', how='inner')
                        st_merged = st_merged.sort_values(['trip_id', 'stop_sequence'])
                        
                        if df_shapes is not None:
                            trip_shape_map = df_gtfs_full.set_index('trip_id')['shape_id'].to_dict()
                            df_shapes_c = df_shapes.copy()
                            df_shapes_c = df_shapes_c.sort_values(['shape_id', 'shape_pt_sequence'])
                            df_shapes_c['shift_lat'] = df_shapes_c.groupby('shape_id')['shape_pt_lat'].shift()
                            df_shapes_c['shift_lon'] = df_shapes_c.groupby('shape_id')['shape_pt_lon'].shift()
                            df_shapes_c['dist'] = calc_haversine(df_shapes_c['shift_lat'], df_shapes_c['shift_lon'], df_shapes_c['shape_pt_lat'], df_shapes_c['shape_pt_lon']).fillna(0)
                            df_shapes_c['cum_dist'] = df_shapes_c.groupby('shape_id')['dist'].cumsum()
                            shape_dict = {k: v for k, v in df_shapes_c.groupby('shape_id')}
                            
                            active_trips = df_hist['trip_id'].unique()
                            st_merged = st_merged[st_merged['trip_id'].isin(active_trips)].copy()
                            st_merged['shape_id'] = st_merged['trip_id'].map(trip_shape_map)
                            
                            def get_cum_dist(row):
                                s_id = row['shape_id']
                                if pd.isna(s_id) or s_id not in shape_dict:
                                    return 0
                                s_grp = shape_dict[s_id]
                                dists = (s_grp['shape_pt_lat'] - row['stop_lat'])**2 + (s_grp['shape_pt_lon'] - row['stop_lon'])**2
                                return s_grp.loc[dists.idxmin(), 'cum_dist']
                                
                            st_merged['cum_dist'] = st_merged.apply(get_cum_dist, axis=1)
                            st_merged['next_stop'] = st_merged.groupby('trip_id')['stop_name'].shift(-1)
                            st_merged['next_cum_dist'] = st_merged.groupby('trip_id')['cum_dist'].shift(-1)
                            
                            segments = st_merged.dropna(subset=['next_stop']).copy()
                            segments['distance_km'] = (segments['next_cum_dist'] - segments['cum_dist']).abs()
                        else:
                            st_merged['next_stop'] = st_merged.groupby('trip_id')['stop_name'].shift(-1)
                            st_merged['next_lat'] = st_merged.groupby('trip_id')['stop_lat'].shift(-1)
                            st_merged['next_lon'] = st_merged.groupby('trip_id')['stop_lon'].shift(-1)
                            
                            active_trips = df_hist['trip_id'].unique()
                            segments = st_merged[st_merged['trip_id'].isin(active_trips)].copy()
                            segments = segments.dropna(subset=['next_stop'])
                            segments['distance_km'] = calc_haversine(segments['stop_lat'], segments['stop_lon'], segments['next_lat'], segments['next_lon'])
                        
                        short_segments = segments[segments['distance_km'] < batas_jarak].copy()
                        
                        if not short_segments.empty:
                            is_halte_1 = short_segments['stop_name'].isin(LIST_HALTE)
                            is_halte_2 = short_segments['next_stop'].isin(LIST_HALTE)
                            short_segments = short_segments[~(is_halte_1 & is_halte_2)]
                            
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

                with tab_komplain_ui:
                    st.markdown("### Korelasi Kinerja Operasional & Keluhan Pelanggan")
                    if df_histori_full is not None and not df_histori_full.empty:
                        df_h_all = df_histori_full.copy()
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
                                    if df_most_frequent is not None:
                                        prime_trips_for_route = df_most_frequent[df_most_frequent['Route_ID'] == selected_route_komplain]['Trip_ID'].tolist()
                                    
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
                                    
                                    if df_komplain is not None:
                                        df_k = df_komplain
                                        c_rute = next((c for c in df_k.columns if str(c).strip().lower() == 'kode rute'), None)
                                        if c_rute:
                                            df_k_r = df_k[df_k[c_rute] == selected_route_komplain]
                                            if not df_k_r.empty:
                                                d_komp = df_k_r.groupby('tanggal_merge').size().reset_index(name='Komplain')
                                                df_plot = pd.merge(df_plot.drop(columns=['Komplain']), d_komp, on='tanggal_merge', how='left').fillna(0)
                                    
                                    df_plot = df_plot.sort_values('tanggal_merge')
                                    df_plot['tanggal_str'] = pd.to_datetime(df_plot['tanggal_merge']).dt.strftime('%d-%m-%Y')
                                    
                                    fig = go.Figure()
                                    fig.add_trace(go.Scatter(x=df_plot['tanggal_str'], y=df_plot['Total Trip'], fill='tozeroy', mode='none', name='Kumulatif Seluruh Trip', fillcolor='rgba(46, 204, 113, 0.3)', yaxis='y1'))
                                    fig.add_trace(go.Scatter(x=df_plot['tanggal_str'], y=df_plot['Prime Trip'], mode='lines+markers', name='Prime Trip (Total)', line=dict(color='#3498db', width=2), yaxis='y1'))
                                    fig.add_trace(go.Scatter(x=df_plot['tanggal_str'], y=df_plot['Trip Lainnya'], mode='lines+markers', name='Trip Lainnya (Total)', opacity=0.7, line=dict(color='#95a5a6', width=2), yaxis='y1'))
                                    fig.add_trace(go.Scatter(x=df_plot['tanggal_str'], y=df_plot['Waktu Tempuh (Mnt)'], mode='lines+markers', name='Waktu Tempuh', line=dict(color='#f39c12', width=3), yaxis='y2'))
                                    
                                    avg_time_val = df_plot['Waktu Tempuh (Mnt)'].mean()
                                    if avg_time_val > 0:
                                        fig.add_hline(y=avg_time_val, line_dash="dash", line_color="#f39c12", yref="y2", annotation_text=f"Avg Waktu: {avg_time_val:.0f} Mnt", annotation_position="top left", annotation_font_color="#f39c12")

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
                                        if df_komplain is not None:
                                            df_k = df_komplain
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
                    
                    if df_histori_full is not None and not df_histori_full.empty:
                        df_bus = df_histori_full.copy()
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
            except Exception as e:
                st.error(f"Gagal memuat memori file .pkl: {e}")

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
