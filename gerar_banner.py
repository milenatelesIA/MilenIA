#!/usr/bin/env python3
"""Gera o banner JPEG para Google Forms - Mentoria Ser Ter Fazer"""

from PIL import Image, ImageDraw, ImageFont
import math

# Dimensões padrão Google Forms
W, H = 1600, 400

# Cores
AZUL_PRINCIPAL = (62, 155, 234)    # #3E9BEA
AZUL_SECUNDARIO = (91, 155, 213)   # #5B9BD5
GRAFITE = (45, 55, 72)             # #2D3748
FUNDO_CLARO = (240, 247, 252)      # #F0F7FC
BRANCO = (255, 255, 255)

img = Image.new("RGB", (W, H))
draw = ImageDraw.Draw(img)

# --- Fundo gradiente horizontal ---
for x in range(W):
    t = x / W
    if t < 0.5:
        # Azul principal -> azul secundário
        s = t / 0.5
        r = int(AZUL_PRINCIPAL[0] + (AZUL_SECUNDARIO[0] - AZUL_PRINCIPAL[0]) * s)
        g = int(AZUL_PRINCIPAL[1] + (AZUL_SECUNDARIO[1] - AZUL_PRINCIPAL[1]) * s)
        b = int(AZUL_PRINCIPAL[2] + (AZUL_SECUNDARIO[2] - AZUL_PRINCIPAL[2]) * s)
    else:
        # Azul secundário -> fundo claro
        s = (t - 0.5) / 0.5
        r = int(AZUL_SECUNDARIO[0] + (FUNDO_CLARO[0] - AZUL_SECUNDARIO[0]) * s)
        g = int(AZUL_SECUNDARIO[1] + (FUNDO_CLARO[1] - AZUL_SECUNDARIO[1]) * s)
        b = int(AZUL_SECUNDARIO[2] + (FUNDO_CLARO[2] - AZUL_SECUNDARIO[2]) * s)
    draw.line([(x, 0), (x, H)], fill=(r, g, b))

# --- Círculos decorativos translúcidos (lado direito) ---
def draw_circle_outline(draw, cx, cy, radius, color, width=2):
    draw.ellipse(
        [cx - radius, cy - radius, cx + radius, cy + radius],
        outline=color, width=width
    )

circle_color = (255, 255, 255, 30)
# Simular transparência misturando com cor de fundo local
for radius, alpha in [(150, 18), (100, 15), (50, 12)]:
    cx, cy = W - 250, H // 2
    bg_t = cx / W
    if bg_t < 0.5:
        s = bg_t / 0.5
        bg_r = int(AZUL_PRINCIPAL[0] + (AZUL_SECUNDARIO[0] - AZUL_PRINCIPAL[0]) * s)
        bg_g = int(AZUL_PRINCIPAL[1] + (AZUL_SECUNDARIO[1] - AZUL_PRINCIPAL[1]) * s)
        bg_b = int(AZUL_PRINCIPAL[2] + (AZUL_SECUNDARIO[2] - AZUL_PRINCIPAL[2]) * s)
    else:
        s = (bg_t - 0.5) / 0.5
        bg_r = int(AZUL_SECUNDARIO[0] + (FUNDO_CLARO[0] - AZUL_SECUNDARIO[0]) * s)
        bg_g = int(AZUL_SECUNDARIO[1] + (FUNDO_CLARO[1] - AZUL_SECUNDARIO[1]) * s)
        bg_b = int(AZUL_SECUNDARIO[2] + (FUNDO_CLARO[2] - AZUL_SECUNDARIO[2]) * s)
    a = alpha / 255
    c = (
        int(bg_r + (255 - bg_r) * a),
        int(bg_g + (255 - bg_g) * a),
        int(bg_b + (255 - bg_b) * a),
    )
    draw_circle_outline(draw, cx, cy, radius, c, width=2)

# --- Hexágonos decorativos ---
def draw_hexagon(draw, cx, cy, size, color):
    points = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        px = cx + size * math.cos(angle)
        py = cy + size * math.sin(angle)
        points.append((px, py))
    draw.polygon(points, outline=color, width=2)

hex_positions = [
    (1050, 70, 14), (980, 180, 10), (1100, 300, 12),
    (700, 50, 8), (800, 330, 10), (1150, 120, 9),
]
for hx, hy, hs in hex_positions:
    bg_t = hx / W
    if bg_t < 0.5:
        s = bg_t / 0.5
        bg_r = int(AZUL_PRINCIPAL[0] + (AZUL_SECUNDARIO[0] - AZUL_PRINCIPAL[0]) * s)
        bg_g = int(AZUL_PRINCIPAL[1] + (AZUL_SECUNDARIO[1] - AZUL_PRINCIPAL[1]) * s)
        bg_b = int(AZUL_PRINCIPAL[2] + (AZUL_SECUNDARIO[2] - AZUL_PRINCIPAL[2]) * s)
    else:
        s = (bg_t - 0.5) / 0.5
        bg_r = int(AZUL_SECUNDARIO[0] + (FUNDO_CLARO[0] - AZUL_SECUNDARIO[0]) * s)
        bg_g = int(AZUL_SECUNDARIO[1] + (FUNDO_CLARO[1] - AZUL_SECUNDARIO[1]) * s)
        bg_b = int(AZUL_SECUNDARIO[2] + (FUNDO_CLARO[2] - AZUL_SECUNDARIO[2]) * s)
    a = 0.10
    c = (
        int(bg_r + (255 - bg_r) * a),
        int(bg_g + (255 - bg_g) * a),
        int(bg_b + (255 - bg_b) * a),
    )
    draw_hexagon(draw, hx, hy, hs, c)

# --- Linha vertical decorativa (accent) ---
line_x = 80
line_top = H // 2 - 90
line_bottom = H // 2 + 90
for y in range(line_top, line_bottom):
    t = (y - line_top) / (line_bottom - line_top)
    alpha = int(200 * (1 - abs(2 * t - 1)))  # Fade nas pontas
    a = alpha / 255
    c = (
        int(AZUL_PRINCIPAL[0] + (255 - AZUL_PRINCIPAL[0]) * a),
        int(AZUL_PRINCIPAL[1] + (255 - AZUL_PRINCIPAL[1]) * a),
        int(AZUL_PRINCIPAL[2] + (255 - AZUL_PRINCIPAL[2]) * a),
    )
    draw.line([(line_x, y), (line_x + 4, y)], fill=c)

# --- Faixa inferior gradiente ---
strip_h = 6
for x in range(W):
    t = x / W
    r = int(GRAFITE[0] + (AZUL_PRINCIPAL[0] - GRAFITE[0]) * t)
    g = int(GRAFITE[1] + (AZUL_PRINCIPAL[1] - GRAFITE[1]) * t)
    b = int(GRAFITE[2] + (AZUL_PRINCIPAL[2] - GRAFITE[2]) * t)
    draw.line([(x, H - strip_h), (x, H)], fill=(r, g, b))

# --- Pontos decorativos (canto inferior direito) ---
dot_start_x = W - 140
dot_start_y = H - 80
for row in range(3):
    for col in range(5):
        dx = dot_start_x + col * 18
        dy = dot_start_y + row * 18
        draw.ellipse([dx - 2, dy - 2, dx + 2, dy + 2], fill=(200, 215, 230))

# --- Fontes ---
def get_font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()

font_subtitle = get_font(20, bold=False)
font_mentoria = get_font(78, bold=True)
font_stf = get_font(72, bold=True)
font_name = get_font(24, bold=True)
font_title = get_font(14, bold=False)
font_badge = get_font(13, bold=True)

X_LEFT = 120

# --- "Programa de" ---
draw.text((X_LEFT, 42), "PROGRAMA DE", fill=FUNDO_CLARO, font=font_subtitle)

# --- "MENTORIA" ---
draw.text((X_LEFT, 72), "MENTORIA", fill=FUNDO_CLARO, font=font_mentoria)

# --- "SER TER FAZER" ---
draw.text((X_LEFT, 160), "SER TER FAZER", fill=GRAFITE, font=font_stf)

# --- Linha divisória ---
divider_y = 248
draw.rectangle([X_LEFT, divider_y, X_LEFT + 100, divider_y + 4], fill=FUNDO_CLARO)

# --- Nome ---
draw.text((X_LEFT, 265), "Dra. Milena Teles", fill=FUNDO_CLARO, font=font_name)

# --- Credenciais ---
draw.text(
    (X_LEFT, 298),
    "Endocrinologista  |  Pesquisadora  |  Professora  |  Mentora em IA Aplicada à Medicina",
    fill=(210, 225, 240),
    font=font_title,
)

# --- Badge "Inscreva-se" ---
badge_x, badge_y = W - 200, 35
badge_w, badge_h = 130, 36
draw.rounded_rectangle(
    [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h],
    radius=18,
    fill=(255, 255, 255, 40),
    outline=(220, 230, 240),
    width=1,
)
bbox = draw.textbbox((0, 0), "INSCREVA-SE", font=font_badge)
tw = bbox[2] - bbox[0]
th = bbox[3] - bbox[1]
draw.text(
    (badge_x + (badge_w - tw) // 2, badge_y + (badge_h - th) // 2 - 2),
    "INSCREVA-SE",
    fill=FUNDO_CLARO,
    font=font_badge,
)

# --- Salvar ---
output = "/home/user/MilenIA/banner-mentoria.jpg"
img.save(output, "JPEG", quality=95)
print(f"Banner salvo em: {output}")
print(f"Tamanho: {img.size[0]}x{img.size[1]}px")
