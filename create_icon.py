#!/usr/bin/env python3
"""Create a simple microphone icon for the Audio Monitor app."""

from PIL import Image, ImageDraw
import subprocess
import os

def create_icon(size):
    """Create a microphone icon at the given size."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Scale factor
    s = size / 512

    # Background circle gradient effect (blue)
    center = size // 2
    radius = int(220 * s)

    # Draw gradient background circle
    for i in range(radius, 0, -1):
        alpha = 255
        # Gradient from darker to lighter blue
        ratio = i / radius
        r = int(30 + (70 - 30) * (1 - ratio))
        g = int(100 + (150 - 100) * (1 - ratio))
        b = int(200 + (255 - 200) * (1 - ratio))
        draw.ellipse(
            [center - i, center - i, center + i, center + i],
            fill=(r, g, b, alpha)
        )

    # Microphone body (white/light gray)
    mic_width = int(80 * s)
    mic_height = int(140 * s)
    mic_top = int(120 * s)
    mic_left = center - mic_width // 2
    mic_right = center + mic_width // 2
    mic_bottom = mic_top + mic_height

    # Mic body rounded rectangle
    draw.rounded_rectangle(
        [mic_left, mic_top, mic_right, mic_bottom],
        radius=int(40 * s),
        fill=(255, 255, 255, 255)
    )

    # Microphone grille lines
    line_color = (180, 180, 180, 255)
    for y_offset in [0.25, 0.4, 0.55]:
        y = mic_top + int(mic_height * y_offset)
        draw.line(
            [mic_left + int(15 * s), y, mic_right - int(15 * s), y],
            fill=line_color,
            width=max(1, int(3 * s))
        )

    # Microphone stand arc
    arc_top = mic_bottom - int(20 * s)
    arc_width = int(120 * s)
    arc_left = center - arc_width // 2
    arc_right = center + arc_width // 2
    arc_bottom = mic_bottom + int(60 * s)

    draw.arc(
        [arc_left, arc_top, arc_right, arc_bottom],
        start=0, end=180,
        fill=(255, 255, 255, 255),
        width=int(12 * s)
    )

    # Stand vertical line
    stand_top = arc_bottom - int(20 * s)
    stand_bottom = int(380 * s)
    draw.line(
        [center, stand_top, center, stand_bottom],
        fill=(255, 255, 255, 255),
        width=int(12 * s)
    )

    # Stand base
    base_width = int(80 * s)
    draw.line(
        [center - base_width // 2, stand_bottom, center + base_width // 2, stand_bottom],
        fill=(255, 255, 255, 255),
        width=int(12 * s)
    )

    return img

def main():
    # Create iconset directory
    iconset_path = '/tmp/AppIcon.iconset'
    os.makedirs(iconset_path, exist_ok=True)

    # Icon sizes needed for macOS
    sizes = [16, 32, 64, 128, 256, 512]

    for size in sizes:
        # Standard resolution
        icon = create_icon(size)
        icon.save(f'{iconset_path}/icon_{size}x{size}.png')

        # Retina resolution (@2x)
        if size <= 256:
            icon_2x = create_icon(size * 2)
            icon_2x.save(f'{iconset_path}/icon_{size}x{size}@2x.png')

    # Convert iconset to icns
    output_path = '/Users/gabrycina/Desktop/AudioMonitor.app/Contents/Resources/AppIcon.icns'
    subprocess.run(['iconutil', '-c', 'icns', iconset_path, '-o', output_path], check=True)

    print(f"Icon created: {output_path}")

    # Cleanup
    import shutil
    shutil.rmtree(iconset_path)

if __name__ == '__main__':
    main()
