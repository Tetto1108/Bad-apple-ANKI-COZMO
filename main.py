import os
import re
import time
from PIL import Image
import pycozmo

# -----------------------------
# CONFIGURACIÓN
# -----------------------------
CARPETA = "images"   # RUTA DE LOS FRAMES
FPS = 15
FRAME_TIME = 0.4 / FPS
W, H = 84, 48   # RAW Nokia 5110
COZMO_W, COZMO_H = 128, 32

# -----------------------------
# Util: leer RAW -> PIL image
# -----------------------------
def cargar_frame_raw(path):
    with open(path, "rb") as f:
        data = f.read()
    if len(data) != 504:
        raise ValueError(f"Archivo inválido (no es RAW 504 bytes): {path} (tamaño {len(data)})")
    img = Image.new("1", (W, H))
    px = img.load()
    idx = 0
    for page in range(6):
        for x in range(W):
            byte = data[idx]
            idx += 1
            for bit in range(8):
                y = page * 8 + bit
                if y < H:
                    px[x, y] = 1 if (byte >> bit) & 1 else 0
    return img

def adaptar_para_cozmo(img):
    return img.resize((COZMO_W, COZMO_H), Image.NEAREST)

# -----------------------------
# Encontrar y ordenar archivos
# -----------------------------
def encontrar_archivos(folder):
    entries = os.listdir(folder)
    candidates = []
    pattern = re.compile(r"(\d{5})")  # busca 5 dígitos
    for e in entries:
        name = e.strip()
        low = name.lower()
        if low.endswith(".raw") or low.endswith(".bmp.raw"):
            m = pattern.search(name)
            num = None
            if m:
                num = int(m.group(1))
            candidates.append((num if num is not None else 10**9, name))
    # ordenar por número 
    candidates.sort(key=lambda x: x[0])
    return [c[1] for c in candidates]

# -----------------------------
# Reportar huecos en la secuencia numérica
# -----------------------------
def reportar_huecos(nombres):
    nums = []
    pat = re.compile(r"(\d{5})")
    for n in nombres:
        m = pat.search(n)
        if m:
            nums.append(int(m.group(1)))
    if not nums:
        print("No se detectaron archivos con número en el nombre.")
        return
    nums_sorted = sorted(nums)
    faltantes = []
    for a in range(nums_sorted[0], nums_sorted[-1]+1):
        if a not in nums_sorted:
            faltantes.append(a)
    if faltantes:
        print(f"Huecos detectados: {len(faltantes)} archivos faltantes. Ejemplos: {faltantes[:10]}")
    else:
        print("No hay huecos en la secuencia numérica.")

# -----------------------------
# Reproducir animación en Cozmo
# -----------------------------
def reproducir(archivos, folder):
    rutas = [os.path.join(folder, a) for a in archivos]
    with pycozmo.connect(enable_procedural_face=False) as cli:
        cli.set_head_angle(1.0)
        time.sleep(0.5)
        print("Reproduciendo animación...")
        try:
            while True:
                for ruta in rutas:
                    try:
                        raw_img = cargar_frame_raw(ruta)
                        img = adaptar_para_cozmo(raw_img)
                        cli.display_image(img)
                        time.sleep(FRAME_TIME)
                    except Exception as e:
                        print(f"ERROR al procesar {ruta}: {e}")
        except KeyboardInterrupt:
            print("\nDetenido por usuario. Saliendo...")

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    print("Carpeta usada:", os.path.abspath(CARPETA))
    archivos = encontrar_archivos(CARPETA)
    if not archivos:
        print("No se encontraron archivos .raw en la carpeta especificada.")
        print("Asegúrate de que los nombres tengan extensión .raw o .bmp.raw")
    else:
        print(f"Se encontraron {len(archivos)} archivos RAW (primeros 20):")
        for a in archivos[:20]:
            print("  ", a)
        reportar_huecos(archivos)
        resp = input("¿Reproducir estos archivos en Cozmo? (s/n): ").strip().lower()
        if resp == "s":
            reproducir(archivos, CARPETA)
        else:
            print("Abortado por el usuario.")
