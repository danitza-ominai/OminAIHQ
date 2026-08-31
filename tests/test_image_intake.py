"""Pruebas exhaustivas para la Ingesta y Saneamiento de Imagenes (PZ-009C).

Valida deteccion de encabezados PNG y JPEG, proteccion contra bombas de descompresion,
stripping de metadatos EXIF/GPS, tratamiento de incertidumbre visual e integracion en HQRuntime.
"""

import struct
import unittest
import zlib

import app.hq_runtime as hq_runtime
import app.image_intake as image_intake


def _build_minimal_png(width: int, height: int, include_exif: bool = False) -> bytes:
    """Construye en memoria los bytes de un archivo PNG sintético valido."""
    header = b"\x89PNG\r\n\x1a\n"
    # IHDR chunk: 13 bytes (width: 4, height: 4, bit depth: 1, color type: 1, compression: 1, filter: 1, interlace: 1)
    ihdr_data = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    ihdr_crc = struct.pack(">I", zlib.crc32(b"IHDR" + ihdr_data) & 0xFFFFFFFF)
    ihdr_chunk = struct.pack(">I", len(ihdr_data)) + b"IHDR" + ihdr_data + ihdr_crc

    exif_chunk = b""
    if include_exif:
        exif_data = b"Exif\x00\x00GPS:LAT=19.4326,LON=-99.1332;CAMERA=NikonD850"
        exif_crc = struct.pack(">I", zlib.crc32(b"eXIf" + exif_data) & 0xFFFFFFFF)
        exif_chunk = struct.pack(">I", len(exif_data)) + b"eXIf" + exif_data + exif_crc

    # IDAT chunk minimo (1 pixel RGB)
    raw_pixel = b"\x00\xff\x00\x00"  # filter byte 0 + red pixel
    idat_data = zlib.compress(raw_pixel)
    idat_crc = struct.pack(">I", zlib.crc32(b"IDAT" + idat_data) & 0xFFFFFFFF)
    idat_chunk = struct.pack(">I", len(idat_data)) + b"IDAT" + idat_data + idat_crc

    # IEND chunk
    iend_crc = struct.pack(">I", zlib.crc32(b"IEND") & 0xFFFFFFFF)
    iend_chunk = struct.pack(">I", 0) + b"IEND" + iend_crc

    return header + ihdr_chunk + exif_chunk + idat_chunk + iend_chunk


def _build_minimal_jpeg(width: int, height: int, include_exif: bool = False) -> bytes:
    """Construye en memoria los bytes de un archivo JPEG sintético basico."""
    header = b"\xff\xd8"
    app1 = b""
    if include_exif:
        exif_content = b"Exif\x00\x00DatosSensiblesGPS"
        seg_len = len(exif_content) + 2
        app1 = b"\xff\xe1" + struct.pack(">H", seg_len) + exif_content

    # Marcador SOF0: longitud 8, precision 8, alto, ancho, 3 componentes
    sof0_len = 8 + 3 * 3
    sof0 = b"\xff\xc0" + struct.pack(">H", sof0_len) + b"\x08" + struct.pack(">HH", height, width) + b"\x03\x01\x11\x00\x02\x11\x01\x03\x11\x01"
    eoi = b"\xff\xd9"
    return header + app1 + sof0 + eoi


class TestImageIntake(unittest.TestCase):
    """Suite de pruebas para PZ-009C (Image Intake)."""

    def setUp(self) -> None:
        self.manager = image_intake.ImageIntakeManager()
        self.runtime = hq_runtime.HQRuntime(image_intake_manager=self.manager)

    def test_ac01_png_valid_corrupt_decompression_bomb_and_invalid_ext(self) -> None:
        """AC-01: Imagen valida, corrupta, bomba de descompresion y extension invalida."""
        # 1. PNG valido de 800x600
        png_bytes = _build_minimal_png(800, 600)
        ok1, rec1, _ = self.manager.process_image("diagrama.png", png_bytes, "MSN-001")
        self.assertTrue(ok1)
        self.assertEqual(rec1["width"], 800)
        self.assertEqual(rec1["height"], 600)

        # 2. Extension no permitida (.gif)
        ok_ext, _, err_ext = self.manager.process_image("animacion.gif", b"GIF89a", "MSN-001")
        self.assertFalse(ok_ext)
        self.assertIn("Formato de imagen no soportado", err_ext)

        # 3. Bomba de descompresion (dimensiones gigantes 20000x20000)
        bomb_png = _build_minimal_png(20000, 20000)
        ok_bomb, _, err_bomb = self.manager.process_image("bomb.png", bomb_png, "MSN-001")
        self.assertFalse(ok_bomb)
        self.assertIn("Bomba de descompresion detectada", err_bomb)

        # 4. Archivo corrupto (dice PNG pero contiene datos invalidos)
        ok_corrupt, _, err_corrupt = self.manager.process_image("corrupto.png", b"\x89PNG\r\n\x1a\nTRUNCATED", "MSN-001")
        self.assertFalse(ok_corrupt)
        self.assertIn("corrupto", err_corrupt)

        # 5. JPEG de 4 bytes truncado FF D8 FF D9 sin SOF
        ok_jpeg_trunc, _, err_jpeg_trunc = self.manager.process_image("truncado.jpg", b"\xff\xd8\xff\xd9", "MSN-001")
        self.assertFalse(ok_jpeg_trunc)
        self.assertIn("corrupto", err_jpeg_trunc.lower())

    def test_ac02_visual_uncertainty_is_flagged(self) -> None:
        """AC-02: La observacion visual no se declara como hecho definitivo sino con flag de incertidumbre."""
        png_bytes = _build_minimal_png(400, 300)
        ok, rec, _ = self.manager.process_image("mockup.png", png_bytes, "MSN-001", observed_caption="Captura preliminar de interfaz")
        self.assertTrue(ok)
        self.assertEqual(rec["visual_uncertainty_flag"], "OBSERVACION_PRELIMINAR_NO_CONFIRMADA")

    def test_ac03_exif_metadata_stripped_from_sanitized_copy(self) -> None:
        """AC-03: Los metadatos EXIF / GPS son eliminados de la copia saneada."""
        # 1. PNG con EXIF
        png_with_exif = _build_minimal_png(200, 200, include_exif=True)
        self.assertIn(b"GPS", png_with_exif)

        ok_png, rec_png, _ = self.manager.process_image("foto.png", png_with_exif, "MSN-001")
        self.assertTrue(ok_png)
        self.assertNotIn(b"GPS", rec_png["sanitized_bytes"])
        self.assertNotEqual(rec_png["sha256_original"], rec_png["sha256_sanitized"])

        # 2. JPEG con EXIF
        jpeg_with_exif = _build_minimal_jpeg(300, 200, include_exif=True)
        self.assertIn(b"DatosSensiblesGPS", jpeg_with_exif)

        ok_jpg, rec_jpg, _ = self.manager.process_image("foto.jpg", jpeg_with_exif, "MSN-001")
        self.assertTrue(ok_jpg)
        self.assertNotIn(b"DatosSensiblesGPS", rec_jpg["sanitized_bytes"])

    def test_ac05_runtime_integration(self) -> None:
        """AC-05: El ImageIntakeManager se encuentra accesible en HQRuntime."""
        self.assertIsNotNone(self.runtime.image_intake)
        self.assertIsInstance(self.runtime.image_intake, image_intake.ImageIntakeManager)


if __name__ == "__main__":
    unittest.main()
