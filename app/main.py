# doctor_services/app/main.py
from flask import Flask, request, jsonify, abort
from database import get_db
from crud import create_dokter, get_dokter, get_dokter_by_id, update_dokter, delete_dokter
from sqlalchemy.orm import Session
from flask import Flask, jsonify
from models import Dokter
from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/db_healthcare'

# Inisialisasi Database
db = SQLAlchemy(app)


#tambah data
@app.route("/doctors/", methods=["POST"])
def add_doctor():
    print(f"Request JSON: {request.get_json()}")  # Log data yang diterima

    nama = request.get_json().get("nama_dokter")
    spesialisasi = request.get_json().get("spesialisasi")
    nomor_hp = request.get_json().get("nomor_hp")

    # Pastikan semua field yang diperlukan ada
    if not nama or not spesialisasi or not nomor_hp:
        abort(400, description="Missing required fields: nama, spesialisasi, nomor_hp")

    try:
        # Menggunakan waktu saat ini dari server
        jadwal_praktik_datetime = datetime.now()
    except Exception as e:
        print(f"Error: {e}")
        abort(500, description="Error saat mendapatkan waktu saat ini")

    try:
        # Membuat dokter baru dengan waktu saat ini
        new_dokter = Dokter(
            nama_dokter=nama,
            spesialisasi=spesialisasi,
            nomor_hp=nomor_hp,
            jadwal_praktik=jadwal_praktik_datetime  # Menggunakan waktu sekarang
        )
        db.session.add(new_dokter)
        db.session.commit()
        db.session.refresh(new_dokter)
        return jsonify({"message": "Dokter berhasil ditambahkan", "id_dokter": new_dokter.id_dokter}), 201
    except Exception as e:
        print(f"Error: {e}")
        abort(500, description="Gagal menambahkan dokter")

#mengambil semua data dokter
@app.route("/doctors/", methods=["GET"])
def read_doctors():
    doctors = db.session.query(Dokter).all()  # Menggunakan db.session
    return jsonify([
        {
            "id_dokter": doctor.id_dokter,
            "nama_dokter": doctor.nama_dokter,
            "spesialisasi": doctor.spesialisasi,
            "nomor_hp": doctor.nomor_hp,
            "jadwal_praktik": doctor.jadwal_praktik
        } for doctor in doctors
    ])



# Endpoint untuk mendapatkan dokter berdasarkan ID
@app.route("/doctors/<int:dokter_id>", methods=["GET"])
def read_doctor(dokter_id):
    db = next(get_db())
    doctor = get_dokter_by_id(db, dokter_id)
    if not doctor:
        abort(404, description="Dokter tidak ditemukan")
    return jsonify({
        "id_dokter": doctor.id_dokter,
        "nama_dokter": doctor.nama_dokter,
        "spesialisasi": doctor.spesialisasi,
        "nomor_hp": doctor.nomor_hp,
        "jadwal_praktik": doctor.jadwal_praktik
    })

@app.route('/doctors/<int:id>', methods=['PUT'])
def update_doctor(id):
    db = next(get_db())  # Mengambil sesi database
    data = request.get_json()  # Mengambil data JSON dari request

    # Validasi data masuk
    if not data:
        return jsonify({"error": "Data tidak valid! Missing JSON payload"}), 400
    if 'nama_dokter' not in data or 'spesialisasi' not in data:
        return jsonify({"error": "Missing required fields: 'nama_dokter' or 'spesialisasi'"}), 400

    # Query dokter berdasarkan ID
    doctor = db.query(Dokter).filter(Dokter.id_dokter == id).first()

    # Periksa apakah dokter ditemukan
    if doctor is None:
        return jsonify({"error": "Dokter tidak ditemukan!"}), 404

    # Update data dokter
    doctor.nama_dokter = data['nama_dokter']
    doctor.spesialisasi = data['spesialisasi']
    if 'nomor_hp' in data:
        doctor.nomor_hp = data['nomor_hp']
    if 'jadwal_praktik' in data:
        try:
            from datetime import datetime
            doctor.jadwal_praktik = datetime.strptime(data['jadwal_praktik'], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid date format for 'jadwal_praktik'. Use YYYY-MM-DD."}), 400

    # Commit perubahan ke database
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        return jsonify({"error": f"Failed to update doctor: {str(e)}"}), 500

    # Return response dengan data yang diperbarui
    return jsonify({
        "id_dokter": doctor.id_dokter,
        "nama_dokter": doctor.nama_dokter,
        "spesialisasi": doctor.spesialisasi,
        "nomor_hp": doctor.nomor_hp,
        "jadwal_praktik": doctor.jadwal_praktik.isoformat() if doctor.jadwal_praktik else None
    }), 200

# Endpoint untuk menghapus dokter
@app.route("/doctors/<int:doctor_id>", methods=["DELETE"])
def delete_doctor_info(doctor_id):
    db = next(get_db())  # Mengambil sesi database

    # Query dokter berdasarkan ID
    doctor = db.query(Dokter).filter(Dokter.id_dokter == doctor_id).first()

    # Periksa apakah dokter ditemukan
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    try:
        # Hapus data dokter
        db.delete(doctor)
        db.commit()
        return jsonify({"message": "Hapus data dokter berhasil"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": f"Failed to delete doctor: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)
