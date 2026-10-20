"""Shared visual measurements for strict validation and diagnostics."""

from runtime_support import ensure_pillow
ensure_pillow()
from PIL import ImageChops, ImageFilter


def normalized_edge_disagreement(reference, actual, box, *, tolerance_px=1):
    """Fraction of contour pixels lacking a match within the tolerance radius."""
    def edges(image):
        return image.convert("L").crop(box).filter(ImageFilter.FIND_EDGES).point(
            lambda value: 255 if value > 48 else 0
        )

    ref_edges, actual_edges = edges(reference), edges(actual)
    ref_count = ref_edges.histogram()[255]
    actual_count = actual_edges.histogram()[255]
    if ref_count + actual_count == 0:
        return 0.0
    width = tolerance_px * 2 + 1
    ref_near = ref_edges.filter(ImageFilter.MaxFilter(width))
    actual_near = actual_edges.filter(ImageFilter.MaxFilter(width))
    ref_missing = ImageChops.subtract(ref_edges, actual_near).histogram()[255]
    actual_missing = ImageChops.subtract(actual_edges, ref_near).histogram()[255]
    return (ref_missing + actual_missing) / (ref_count + actual_count)
