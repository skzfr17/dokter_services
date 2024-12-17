from sqlalchemy.orm import Session
from models import Dokter
from datetime import datetime, date

# Fungsi untuk membuat data dokter baru
def create_dokter(db: Session, nama_dokter: str, spesialisasi: str, nomor_hp: str, jadwal_praktik):
    # Validasi dan konversi jadwal_praktik jika perlu
    if isinstance(jadwal_praktik, str):
        try:
            jadwal_praktik = datetime.strptime(jadwal_praktik, "%Y-%m-%d").date()
        except ValueError as e:
            raise ValueError(f"Error parsing jadwal_praktik: {e}")
    elif not isinstance(jadwal_praktik, date):
        raise TypeError("jadwal_praktik harus berupa objek date atau string dengan format YYYY-MM-DD.")

    # Membuat objek Dokter baru
    new_dokter = Dokter(
        nama_dokter=nama_dokter,
        spesialisasi=spesialisasi,
        nomor_hp=nomor_hp,
        jadwal_praktik=jadwal_praktik
    )
    db.add(new_dokter)
    db.commit()
    db.refresh(new_dokter)
    return new_dokter

# Fungsi untuk mengambil semua data dokter
def get_dokter(db: Session):
    return db.query(Dokter).all()

# Fungsi untuk mengambil data dokter berdasarkan ID
def get_dokter_by_id(db: Session, dokter_id: int):
    return db.query(Dokter).filter(Dokter.id_dokter == dokter_id).first()

# Fungsi untuk memperbarui data dokter
def update_dokter(db: Session, dokter_id: int, nama: str, spesialisasi: str, nomor_hp: str, jadwal_praktik: date):
    db_doctor = db.query(Dokter).filter(Dokter.id_dokter == dokter_id).first()
    if db_doctor:
        # Validasi jadwal_praktik
        if isinstance(jadwal_praktik, str):
            try:
                jadwal_praktik = datetime.strptime(jadwal_praktik, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Format tanggal jadwal_praktik harus YYYY-MM-DD.")
        elif not isinstance(jadwal_praktik, date):
            raise TypeError("jadwal_praktik harus berupa objek date atau string dengan format YYYY-MM-DD.")

        # Perbarui data dokter
        db_doctor.nama_dokter = nama
        db_doctor.spesialisasi = spesialisasi
        db_doctor.nomor_hp = nomor_hp
        db_doctor.jadwal_praktik = jadwal_praktik
        db.commit()
        db.refresh(db_doctor)
    return db_doctor

# Fungsi untuk menghapus data dokter
def delete_dokter(db: Session, dokter_id: int):
    db_doctor = db.query(Dokter).filter(Dokter.id_dokter == dokter_id).first()
    if db_doctor:
        db.delete(db_doctor)
        db.commit()
        return True
    return False
