from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates

def scale_glyph(glyph, scale_x):
    # Apply X scaling. Glyph is updated in-place
    if glyph.isComposite():
        for component in glyph.components:
            component.transform = (component.transform[0] * scale_x,  # Scale X in transform matrix
                                   component.transform[1],  # Scale Y in transform matrix
                                   component.transform[2],  # Skew
                                   component.transform[3],  # Scale X in Y-axis direction
                                   component.transform[4],  # Translate X
                                   component.transform[5])  # Translate Y

    elif glyph.numberOfContours > 0:
        glyph.coordinates = GlyphCoordinates((cx * scale_x, cy) for cx, cy in glyph.coordinates)

def rename_font_name_record(name_record, new_family_name):
    # Update the name table entries
    if name_record.nameID in [1, 4, 16]:    # 1 = Font Family, 4 = Full Name, 16 = Preferred Family
        name_record.string = new_family_name.encode(name_record.getEncoding())
    return name_record

def scale_hmtx(font, scale_x):
    # Also scale font spacing
    hmtx = font['hmtx']
    for glyph_name in font.getGlyphOrder():
        advanceWidth, leftSideBearing = hmtx[glyph_name]
        hmtx[glyph_name] = (int(advanceWidth * scale_x), leftSideBearing)

def scale_kerning(font, scale_x):
    # Not necessary for Noto Sans JP
    if 'kern' in font:
        for kern_table in font['kern'].kernTables:
            for pair, value in kern_table.kernTable.items():
                kern_table.kernTable[pair] = int(value * scale_x)

def scale_glyphs_and_spacing(font_path, output_path, scale_x, new_family_name):
    font = TTFont(font_path)
    glyf_table = font['glyf']
    for name in glyf_table.glyphs.keys():
        # NOTE: font['glyf'].glyphs is lazy-loaded, `items()` won't do
        scale_glyph(glyf_table[name], scale_x)

    scale_hmtx(font, scale_x)
    scale_kerning(font, scale_x)

    font['name'].names = [rename_font_name_record(record, new_family_name)
                                        for record in font['name'].names]
    font.save(output_path)
    print(f"Saved scaled font to {output_path}")


input_font = "NotoSansJP-VariableFont_wght.ttf"
output_font = "NotoSansJP-Condensed.ttf"
scale_x = 0.82  # Horizontal scaling factor
new_family_name = "Noto Sans JP Condensed"  # New font family name


scale_glyphs_and_spacing(input_font, output_font, scale_x, new_family_name)

"""
pip install fonttools brotli
fonttools ttLib.woff2 compress NotoSansJP-Condensed.ttf
"""
