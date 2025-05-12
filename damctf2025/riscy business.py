file_path = "esp_ota_client.elf"

rodata_vaddr = 0x42060120
rodata_offset = 0x0cc120
target_vaddr = 0x42064048
relative_offset = target_vaddr - rodata_vaddr
absolute_offset = rodata_offset + relative_offset
extract_length = 32  

with open(file_path, "rb") as f:
    f.seek(absolute_offset)
    raw_data = f.read(extract_length)

ascii_result = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in raw_data)
hex_result = ' '.join(f'{b:02x}' for b in raw_data)

print(ascii_result, hex_result)