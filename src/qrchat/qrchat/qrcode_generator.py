import qrcode
import os
from .settings import MEDIA_ROOT
from uuid import UUID

def generate_qrcode(url:str, room_uuid:UUID) -> str:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=40,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    file_path = os.path.join(MEDIA_ROOT, "qrcodes", f"room_qrcode_{room_uuid}.png")
    img.save(file_path)

    return f"/media/qrcodes/room_qrcode_{room_uuid}.png"

def delete_qrcode(room_uuid:UUID) -> None:
    file_path = os.path.join(MEDIA_ROOT, "qrcodes", f"room_qrcode_{room_uuid}.png")
    if os.path.exists(file_path):
        os.remove(file_path)