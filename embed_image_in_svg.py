"""
Bettet Raum_Render.jpg (oder .png) als Base64 direkt in Raum_Render.svg ein.

Warum das noetig ist:
Browser blockieren externe Bildreferenzen (xlink:href="Raum_Render.png")
innerhalb einer SVG-Datei, wenn diese SVG per <img src="..."> eingebunden
wird. Das eingebettete Base64-Bild macht die SVG-Datei komplett
in sich geschlossen, wodurch das Bild garantiert sichtbar bleibt.

Verwendung:
1. Dieses Skript, Raum_Render.svg und dein Bild (jpg oder png) in denselben
   Ordner legen.
2. Unten bei IMAGE_FILENAME den exakten Dateinamen deines Bildes eintragen.
3. Im Terminal ausführen:  python embed_image_in_svg.py
4. Ergebnis: Raum_Render_embedded.svg wird erzeugt.
5. Diese neue Datei statt der alten Raum_Render.svg in deinem Website-Ordner
   verwenden (ggf. umbenennen zu Raum_Render.svg).
"""

import base64
import re
import os

SVG_INPUT = "Raum_Render.svg"
SVG_OUTPUT = "Raum_Render_embedded.svg"
IMAGE_FILENAME = "Raum_Render.png"   # <-- ggf. anpassen: .jpg oder .png

MIME_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
}

def main():
    if not os.path.exists(SVG_INPUT):
        raise FileNotFoundError(f"{SVG_INPUT} nicht gefunden. Liegt die Datei im selben Ordner?")
    if not os.path.exists(IMAGE_FILENAME):
        raise FileNotFoundError(f"{IMAGE_FILENAME} nicht gefunden. Liegt die Datei im selben Ordner?")

    ext = os.path.splitext(IMAGE_FILENAME)[1].lower()
    mime = MIME_TYPES.get(ext)
    if not mime:
        raise ValueError(f"Unbekanntes Bildformat: {ext}. Erlaubt: .jpg, .jpeg, .png")

    with open(IMAGE_FILENAME, "rb") as f:
        image_bytes = f.read()

    b64_data = base64.b64encode(image_bytes).decode("ascii")
    data_uri = f"data:{mime};base64,{b64_data}"

    with open(SVG_INPUT, "r", encoding="utf-8") as f:
        svg_content = f.read()

    # Ersetzt jedes xlink:href="....jpg/.png/.jpeg" durch die eingebetteten Bilddaten
    pattern = r'xlink:href="[^"]*\.(?:jpg|jpeg|png)"'
    new_svg_content, count = re.subn(pattern, f'xlink:href="{data_uri}"', svg_content, flags=re.IGNORECASE)

    if count == 0:
        print("WARNUNG: Keine xlink:href-Bildreferenz in der SVG gefunden.")
        print("Pruefe, ob dein <image>-Tag wirklich xlink:href=\"Raum_Render.png\" o.ae. enthaelt.")
    else:
        print(f"{count} Bildreferenz(en) erfolgreich eingebettet.")

    with open(SVG_OUTPUT, "w", encoding="utf-8") as f:
        f.write(new_svg_content)

    size_kb = len(new_svg_content) / 1024
    print(f"Fertig: {SVG_OUTPUT} erstellt ({size_kb:.1f} KB).")
    print("Diese Datei jetzt als Raum_Render.svg in deinem Website-Ordner verwenden.")

if __name__ == "__main__":
    main()
