import tempfile
import unittest
import json
from pathlib import Path

from PIL import Image

from measure_ink_core import measure
from validate_prototype import source_ink_evidence_errors


class MeasureInkCoreTests(unittest.TestCase):
    def test_light_ink_uses_native_image_coordinates(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "sample.png"
            image = Image.new("RGB", (40, 30), (40, 150, 100))
            for y in range(8, 13):
                for x in range(11, 19):
                    image.putpixel((x, y), (248, 250, 245))
            image.save(path)
            result = measure(path, (7, 5, 25, 20), "light")
            self.assertEqual(result["bounds"], {"x": 11, "y": 8, "width": 8, "height": 5})
            self.assertEqual(result["pixelCount"], 40)

    def test_dark_ink_does_not_include_light_panel(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "sample.png"
            image = Image.new("RGB", (40, 30), (180, 220, 205))
            for y in range(10, 16):
                for x in range(20, 24):
                    image.putpixel((x, y), (7, 92, 72))
            image.save(path)
            result = measure(path, (15, 5, 30, 20), "dark")
            self.assertEqual(result["bounds"], {"x": 20, "y": 10, "width": 4, "height": 6})
            self.assertEqual(result["pixelCount"], 24)

    def test_pixel_core_evidence_is_recomputed_from_locked_source(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / "reference.png"
            image = Image.new("RGB", (40, 30), (180, 220, 205))
            for y in range(10, 16):
                for x in range(20, 24):
                    image.putpixel((x, y), (7, 92, 72))
            image.save(source)
            result = measure(source, (15, 5, 30, 20), "dark")
            evidence = {"layers": [{"id": "label", "source": result}]}
            (root / "ink.json").write_text(json.dumps(evidence))
            layer = {"id": "label", "type": "text",
                     "referenceInkBounds": result["bounds"],
                     "referenceInkMethod": "high-contrast-pixel-core",
                     "referenceInkEvidence": "ink.json"}
            self.assertEqual(source_ink_evidence_errors(root, layer, source), [])
            evidence["layers"][0]["source"]["bounds"]["x"] = 19
            (root / "ink.json").write_text(json.dumps(evidence))
            self.assertTrue(any("bounds not found" in error
                                for error in source_ink_evidence_errors(root, layer, source)))


if __name__ == "__main__":
    unittest.main()
