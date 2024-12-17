from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Dokter(Base):
    __tablename__ = "tb_doctor"

    id_dokter = Column(Integer, primary_key=True, index=True)
    nama_dokter = Column(String, nullable=False)
    spesialisasi = Column(String, nullable=False)
    nomor_hp = Column(String, nullable=False)
    jadwal_praktik = Column(DateTime, nullable=False)

    def to_dict(self):
        return {
            "id_dokter": self.id_dokter,
            "nama_dokter": self.nama_dokter,
            "spesialisasi": self.spesialisasi,
            "nomor_hp": self.nomor_hp,
            "jadwal_praktik": self.jadwal_praktik.isoformat() if self.jadwal_praktik else None,
        }
