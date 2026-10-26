"""Image header dimensions without an imaging dependency or pixel modification."""
import struct


def dimensions(raw):
    if raw.startswith(b'\x89PNG\r\n\x1a\n') and len(raw) >= 24:
        return struct.unpack('>II', raw[16:24])
    if raw.startswith(b'\xff\xd8'):
        i = 2; orientation = 1
        while i + 4 < len(raw):
            if raw[i] != 255:
                i += 1
                continue
            marker = raw[i + 1]; i += 2
            if marker in (0, 255) or 0xd0 <= marker <= 0xd9:
                continue
            length = int.from_bytes(raw[i:i+2], 'big')
            if length < 2:
                break
            if marker == 0xe1:
                payload=raw[i+2:i+length]
                if payload.startswith(b'Exif\0\0'):
                    tiff=payload[6:];order='little'if tiff[:2]==b'II'else'big'
                    try:
                        offset=int.from_bytes(tiff[4:8],order)
                        count=int.from_bytes(tiff[offset:offset+2],order)
                        for j in range(min(count,1024)):
                            entry=tiff[offset+2+12*j:offset+14+12*j]
                            if int.from_bytes(entry[:2],order)==0x112:
                                orientation=int.from_bytes(entry[8:10],order);break
                    except (ValueError,IndexError):
                        pass
            if marker in (0xc0,0xc1,0xc2,0xc3,0xc5,0xc6,0xc7,0xc9,0xca,0xcb,0xcd,0xce,0xcf):
                h, w = struct.unpack('>HH', raw[i+3:i+7])
                return (h,w)if orientation in(5,6,7,8)else(w,h)
            i += length
    if raw.startswith(b'RIFF') and raw[8:12] == b'WEBP':
        kind, data = raw[12:16], raw[20:]
        if kind == b'VP8X' and len(data) >= 10:
            return int.from_bytes(data[4:7], 'little')+1, int.from_bytes(data[7:10], 'little')+1
        if kind == b'VP8L' and len(data) >= 5 and data[0] == 0x2f:
            bits = int.from_bytes(data[1:5], 'little')
            return (bits & 0x3fff)+1, ((bits >> 14) & 0x3fff)+1
        if kind == b'VP8 ':
            i = data.find(b'\x9d\x01\x2a')
            if i >= 0 and len(data) >= i+7:
                return int.from_bytes(data[i+3:i+5], 'little') & 0x3fff, int.from_bytes(data[i+5:i+7], 'little') & 0x3fff
    raise ValueError('image dimensions unavailable: expected a valid PNG, JPEG or WebP header')
