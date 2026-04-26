from PIL import Image
import os

def smart_remove_bg(input_path, output_path):
    print(f"Processing: {input_path}")
    try:
        if not os.path.exists(input_path):
            print("Error: Input file not found!")
            return

        img = Image.open(input_path)
        img = img.convert("RGBA")
        datas = img.getdata()

        newData = []
        for item in datas:
            # Smart Detection:
            # If pixel is very bright (white/off-white/light-gray artifact) -> Transparent
            # Threshold 210 covers "dirty whites" from JPEG compression
            if item[0] > 210 and item[1] > 210 and item[2] > 210:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)

        img.putdata(newData)
        img.save(output_path, "PNG")
        print(f"SUCCESS: Generated {output_path}")
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")

if __name__ == "__main__":
    base_dir = r"C:\Users\rguti\Petral.MARK\GeekSoft_Portal"
    input_file = os.path.join(base_dir, "logo_geek.png")
    output_file = os.path.join(base_dir, "logo_geek_transparent.png")
    
    smart_remove_bg(input_file, output_file)
