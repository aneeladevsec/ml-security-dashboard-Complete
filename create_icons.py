#!/usr/bin/env python3
"""
Generate simple icon PNG files for Chrome extension
"""
import struct
import zlib

def create_simple_png(width, height, filename):
    """Create a simple colored PNG file"""
    # PNG header
    png_header = b'\x89PNG\r\n\x1a\n'
    
    # IHDR chunk (image header)
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)  # 8-bit RGB
    ihdr_chunk = b'IHDR' + ihdr_data
    ihdr_checksum = zlib.crc32(ihdr_chunk) & 0xffffffff
    ihdr = struct.pack('>I', len(ihdr_data)) + ihdr_chunk + struct.pack('>I', ihdr_checksum)
    
    # IDAT chunk (image data) - simple gradient
    raw_data = b''
    for y in range(height):
        raw_data += b'\x00'  # Filter type
        for x in range(width):
            # Create a simple shield/lock pattern
            r = int(26 + (x / width) * 50)   # Dark blue
            g = int(26 + (y / height) * 80)   # Blue-ish
            b = int(46 + (x / width) * 100)   # Purple-ish
            raw_data += bytes([r, g, b])
    
    compressed = zlib.compress(raw_data)
    idat_checksum = zlib.crc32(b'IDAT' + compressed) & 0xffffffff
    idat = struct.pack('>I', len(compressed)) + b'IDAT' + compressed + struct.pack('>I', idat_checksum)
    
    # IEND chunk (image end)
    iend_checksum = zlib.crc32(b'IEND') & 0xffffffff
    iend = struct.pack('>I', 0) + b'IEND' + struct.pack('>I', iend_checksum)
    
    # Combine all chunks
    png_data = png_header + ihdr + idat + iend
    
    with open(filename, 'wb') as f:
        f.write(png_data)
    
    print(f"Created {filename} ({len(png_data)} bytes)")

# Create icons
create_simple_png(16, 16, 'chrome-extension/icons/icon16.png')
create_simple_png(48, 48, 'chrome-extension/icons/icon48.png')
create_simple_png(128, 128, 'chrome-extension/icons/icon128.png')

print("✅ All icon files created successfully!")
