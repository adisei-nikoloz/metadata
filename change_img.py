from PIL import Image, ImageDraw, ImageFont
import piexif
from datetime import datetime

def add_text_and_update_exif(image_path, output_path, text, new_datetime, software, position=(10, 10), font_size=20):
    """
    ფოტოზე ტექსტის დამატება და EXIF 'DateTimeOriginal', 'DateTimeDigitized' და 'Software' ველის განახლება.

    Args:
        image_path (str): საწყისი სურათის გზის მისამართი.
        output_path (str): განახლებული სურათის შენახვის გზის მისამართი.
        text (str): სურათზე დასაწერი ტექსტი.
        new_datetime (str): EXIF-ის ახალი თარიღი და დრო.
        software (str): 'Software' ველში ჩასაწერი ინფორმაცია.
        position (tuple): ტექსტის კოორდინატები სურათზე.
        font_size (int): ტექსტის შრიფტის ზომა.
    """
    try:
        # სურათის გახსნა
        image = Image.open(image_path)

        # ტექსტის დამატება სურათზე
        draw = ImageDraw.Draw(image)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            # შრიფტის გაჩერების შემთხვევაში, გამოიყენება დეფოლტი შრიფტი
            font = ImageFont.load_default()
        draw.text(position, text, fill="black", font=font)

        # EXIF მონაცემების ჩატვირთვა და განახლება
        exif_data = image.info.get("exif", None)
        if exif_data:
            exif_dict = piexif.load(exif_data)
        else:
            exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}}

        # შესაბამისი EXIF ველების განახლება
        new_datetime_bytes = new_datetime.encode('ascii')
        software_bytes = software.encode('ascii')

        exif_dict["0th"][piexif.ImageIFD.DateTime] = new_datetime_bytes
        exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = new_datetime_bytes
        exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = new_datetime_bytes
        exif_dict["0th"][piexif.ImageIFD.Software] = software_bytes

        # EXIF ველების სწორად ფორმატირება
        for ifd in exif_dict:
            if isinstance(exif_dict[ifd], dict):
                exif_dict[ifd] = {k: (str(v).encode('ascii') if isinstance(v, int) else v) for k, v in exif_dict[ifd].items()}

        # EXIF მონაცემების ვალიდაცია და კონვერტაცია
        exif_bytes = piexif.dump(exif_dict)

        # განახლებული სურათის შენახვა ახალი EXIF მონაცემებით
        image.save(output_path, exif=exif_bytes)
        print(f"სურათი ტექსტით და განახლებული EXIF მონაცემებით შენახულია: {output_path}")

    except Exception as e:
        print(f"მოხდა შეცდომა: {e}")

# მაგალითის გამოყენება
if __name__ == "__main__":
    # საწყისი და მიზნობრივი სურათების გზის მისამართი
    input_image = r"C:\Users\DESKTOP.GE\Desktop\pyphoto\photos_folder\IMG_20241225_152718.jpg"
    output_image = r"C:\Users\DESKTOP.GE\Desktop\mobile xiaomi redmi9\IMG_20241225_152719.jpg"

    # EXIF-ის ახალი თარიღი და დრო
    current_datetime = datetime.now().strftime("%Y:%m:%d %H:%M:%S")

    # დასაწერი ტექსტი
    text_to_add = "გადაღებულია " + datetime.now().strftime("%Y-%m-%d %H:%M")

    # 'Software' ველში ჩასაწერი ინფორმაცია
    software_info = "Viber"

    # ფუნქციის გამოძახება
    add_text_and_update_exif(input_image, output_image, text_to_add, current_datetime, software_info, position=(50, 50), font_size=30)
