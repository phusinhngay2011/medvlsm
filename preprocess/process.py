from pathlib import Path

from tqdm import tqdm
from utils import (
    convert_busi_filename,
    convert_to_binary_mask,
    copy,
    extract_and_remove_strings,
    find_path,
    get_all_images,
    load_json,
    remove_folders,
    load_json,
    remove_folders,
)

data_root = Path("./data")
anns_path = Path("anns")
images_path = Path("images")
masks_path = Path("masks")
origin_data_path = Path("origin")

supported_datasets = [
    "bkai_polyp",
    "busi",
    "camus",
    "chexlocalize",
    "clinicdb_polyp",
    "colondb_polyp",
    "cvc300_polyp",
    "dfu",
    "etis_polyp",
    "isic",
    "kvasir_polyp",
]

jsons = {
    dataset: {
        "train": data_root / dataset / anns_path / "train.json",
        "test": data_root / dataset / anns_path / "test.json",
        "valid": data_root / dataset / anns_path / "val.json",
    }
    for dataset in supported_datasets
}

datasets = [
    # "bkai_polyp",
    "busi",
]


def process_one_dataset(name):
    assert name in supported_datasets, "Dataset %s not supported" % name
    # Load jsons
    train = load_json(jsons[name]["train"])
    valid = load_json(jsons[name]["valid"])
    test = load_json(jsons[name]["test"])

    # Merge jsons
    data = train.copy()
    data.extend(valid)
    data.extend(test)

    assert len(data) == len(valid) + len(test) + len(train), "Missing data"
    # Refresh
    remove_folders(
        [str(data_root / name / masks_path), str(data_root / name / images_path)]
    )

    if name == "bkai_polyp":
        imgs = get_all_images(data_root / name / origin_data_path / "train")
        imgs.extend(get_all_images(data_root / name / origin_data_path / "test"))
        gts = get_all_images(data_root / name / origin_data_path / "train_gt")

        for item in tqdm(data, desc=f"Process {name}"):
            img_id = item["segment_id"]
            img_origin_path = find_path(imgs, img_id)
            gt_origin_path = find_path(gts, img_id)

            if img_origin_path is None:
                raise ValueError(f"Image {img_origin_path} not found")

            if gt_origin_path is None:
                raise ValueError(f"Ground truth {gt_origin_path} not found")

            copy(
                img_origin_path,
                data_root
                / name
                / images_path
                / Path(img_id + "." + img_origin_path.rsplit(".")[-1]),
            )

            convert_to_binary_mask(
                gt_origin_path,
                data_root
                / name
                / masks_path
                / Path(img_id + "." + gt_origin_path.rsplit(".")[-1]),
            )

        # print(imgs)
        pass

    elif name == "busi":
        imgs = get_all_images(data_root / name / origin_data_path)
        imgs, gts = extract_and_remove_strings(imgs, substr="_mask")

        for item in tqdm(data, desc=f"Process {name}"):
            img_id = item["segment_id"].split("_")
            img_id = f"{img_id[1]} ({img_id[0]})"
            img_origin_path = find_path(imgs, img_id)
            gt_origin_path = find_path(gts, img_id)

            if img_origin_path is None:
                raise ValueError(f"Image {img_origin_path} not found")

            if gt_origin_path is None:
                raise ValueError(f"Ground truth {gt_origin_path} not found")

            copy(
                img_origin_path,
                data_root
                / name
                / images_path
                / Path(convert_busi_filename(img_origin_path)),
            )

            convert_to_binary_mask(
                gt_origin_path,
                data_root
                / name
                / masks_path
                / Path(convert_busi_filename(gt_origin_path)),
            )

    elif name == "camus":
        pass

    elif name == "chexlocalize":
        pass

    elif name == "clinicdb_polyp":
        pass

    elif name == "colondb_polyp":
        pass

    elif name == "cvc300_polyp":
        pass

    elif name == "dfu":
        pass

    elif name == "etis_polyp":
        pass

    elif name == "isic":
        pass

    elif name == "kvasir_polyp":
        pass

    else:
        raise ValueError(f"{name} is not a valid dataset name")


if __name__ == "__main__":
    for name in tqdm(datasets, desc="Processing "):
        process_one_dataset(name)
