from PIL import Image
import piexif

def print_exif(image_path):
    """
    ფოტოს EXIF მონაცემების ამოღება და ბეჭდვა.

    Args:
        image_path (str): სურათის გზის მისამართი.
    """
    try:
        # სურათის გახსნა
        image = Image.open(image_path)

        # EXIF მონაცემების ჩატვირთვა
        exif_data = image.info.get("exif", None)
        if exif_data:
            exif_dict = piexif.load(exif_data)
            for ifd in exif_dict:
                print(f"IFD: {ifd}")
                for tag in exif_dict[ifd]:
                    tag_name = piexif.TAGS[ifd][tag]["name"]
                    tag_value = exif_dict[ifd][tag]
                    print(f"    {tag_name}: {tag_value}")
        else:
            print("EXIF მონაცემები არ მოიძებნა სურათში.")

    except Exception as e:
        print(f"მოხდა შეცდომა: {e}")

# მაგალითის გამოყენება
image_path = r"C:\Users\DESKTOP.GE\Desktop\pyphoto\photos_folder\IMG_20241225_152719.jpg"
print_exif(image_path)
