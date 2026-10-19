# Asset audit

Every visual asset needs a traceable record before it is placed in HTML.
Store entries as a JSON array in asset-manifest.json. Add role (subject/photo/decoration/logo/font). The original reference is separate and cannot be a runtime asset. All source paths are real local files, with actual SHA-256 values; reference/screenshot files cannot be renamed or split to bypass this contract.

```json
{
  "id": "hero-plant",
  "source": "assets/source/hero-plant.png",
  "sha256": "...",
  "kind": "transparent-cutout",
  "intrinsic": {"width": 1200, "height": 1200},
  "alphaBounds": {"x": 94, "y": 48, "width": 1008, "height": 1090},
  "sourceCrop": {"x": 0, "y": 0, "width": 1200, "height": 1200},
  "destination": {"x": 164, "y": 154, "width": 488, "height": 536},
  "scaleMode": "explicit-size",
  "objectPosition": "0 0",
  "confidence": "measured",
  "provenance": "user-supplied"
}
```

Record whether the asset came from the user, imagegen, a licensed stock source, or a flattened screenshot. Keep the original file unchanged. If an alpha channel was manually created, mark it as inferred and do not use it to claim absolute identity.
