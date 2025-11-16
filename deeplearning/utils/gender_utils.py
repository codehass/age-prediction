import shutil
from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parents[2]


def split_utkface_by_gender(base_dir: Path):
    """
    Splits UTKFace images into 'male' and 'female' folders
    based on the gender label in the filename (0 = male, 1 = female).

    Args:
        base_dir (Path): Path to the root project directory containing 'data'.
    """

    GLOBAL_DATA = base_dir / "data"
    UTK_FACE_DATA_PATH = GLOBAL_DATA / "data-global" / "UTKFace"
    GENDER_DIR = GLOBAL_DATA / "gender-data"
    FEMALE_DATA_PATH = GENDER_DIR / "female"
    MALE_DATA_PATH = GENDER_DIR / "male"

    # Create gender directories if they don't exist
    FEMALE_DATA_PATH.mkdir(parents=True, exist_ok=True)
    MALE_DATA_PATH.mkdir(parents=True, exist_ok=True)

    # Mapping: label → destination folder
    gender_map = {"1": FEMALE_DATA_PATH, "0": MALE_DATA_PATH}

    for image_file in UTK_FACE_DATA_PATH.iterdir():
        images_ext = ["png", "jpg", "peng"]
        file_extension = image_file.name.split(".")[-1]

        if file_extension not in images_ext:
            print(f"Skipping mal file type: {image_file.name}")
            continue

        if not image_file.is_file():
            continue

        parts = image_file.name.split("_")
        if len(parts) < 2:
            print(f"Skipping malformed filename: {image_file.name}")
            continue

        gender_label = parts[1]

        # Skip images with unknown gender labels
        if gender_label not in gender_map:
            print(f"Skipping unknown label file: {image_file.name}")
            continue

        destination_folder = gender_map[gender_label]
        destination_path = destination_folder / image_file.name

        if not destination_path.exists():
            shutil.copy(image_file, destination_path)
