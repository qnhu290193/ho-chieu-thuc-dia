# -*- coding: utf-8 -*-
"""Ghép du-lieu.json + khung.html -> «Ho chieu thuc dia.html».
Sửa nội dung trong du-lieu.json rồi chạy:  python ghep.py
(Ghép xong nên chạy lại: python <gốc>/0-LOI-CHUNG/cong-cu/giong_viet.py thu "Ho chieu thuc dia.html" để thu câu mới.)"""
import json, re, sys
from pathlib import Path

D = Path(__file__).resolve().parent
du = json.loads((D / "du-lieu.json").read_text(encoding="utf-8"))
khung = (D / "khung.html").read_text(encoding="utf-8")

# Ảnh thật (Wikimedia Commons, giấy phép mở) — nhúng thẳng vào file để chạy không mạng
import base64
na = D / "anh-that" / "nguon-anh.json"
if na.exists():
    for x in du["diem"]: x["anh"] = []
    for a in json.loads(na.read_text(encoding="utf-8")):
        b = base64.b64encode((D / a["tep"]).read_bytes()).decode()
        d0 = next(x for x in du["diem"] if x["id"] == a["id"])
        d0["anh"].append({k: a[k] for k in ("chu_thich", "tac_gia", "giay_phep", "link_giay_phep", "nguon")} | {"src": "data:image/jpeg;base64," + b})

cau = []
def them(t):
    t = re.sub(r"\s+", " ", str(t)).strip()
    if t and t not in cau:
        cau.append(t)

for d in du["diem"]:
    them(d["chao"])
    for q in d.get("hoi_dap", []):
        them(q["goi_y"]); them(q["dap"])
    for h in d["hs"]:
        them(h["noi"])
    for c in d["cau"]:
        them(c["hoi"])
them("Chính xác! Giỏi lắm!")
them("Chưa đúng rồi, thử lại nhé!")
them("Tuyệt vời! Tổ mình được đóng dấu hộ chiếu!")

ra = D / "Ho chieu thuc dia.html"
cu = ra.read_text(encoding="utf-8") if ra.exists() else ""
khoi_giong = re.search(r"<script>/\*GIONG-VIET-BAT\*/.*?/\*GIONG-VIET-HET\*/</script>\n?", cu, re.S)

s = khung.replace("/*__DU_LIEU__*/null", json.dumps(du, ensure_ascii=False))
s = s.replace("/*__BANDO__*/null", (D / "ban-do-34-tinh.json").read_text(encoding="utf-8"))
s = s.replace("/*__CAU_DOC__*/[]", json.dumps(cau, ensure_ascii=False))
if khoi_giong:   # giữ giọng đã thu
    s = s.replace("</body>", khoi_giong.group(0) + "</body>", 1)
ra.write_text(s, encoding="utf-8")
print("Đã ghép:", ra.name, "·", len(du["diem"]), "điểm đến ·", sum(len(x.get("anh",[])) for x in du["diem"]), "ảnh thật ·", len(cau), "câu đọc", "· giữ giọng cũ" if khoi_giong else "")
