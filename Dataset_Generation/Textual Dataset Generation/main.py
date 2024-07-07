import json
import pandas as pd

color_changes = [
    ("black", "Change * color to black"),
    ("white", "Change * color to white"),
    ("red", "Change * color to red"),
    ("blue", "Change * color to blue"),
    ("orange", "Change * color to orange"),
    ("purple", "Change * color to purple"),
]

scene_changes = [
    ("by the beach", "put * by the beach"),
    ("in the desert", "put * in the desert"),
    ("* in a festival", "put it in a festival"),
    ("on a table", "put * on a table"),
    ("in a forest", "put * in a forest"),
    ("on a roof", "put * on a roof"),
    ("in the air", "make * in the air"),
    ("in hands", "put * in someone`s hands"),
    ("covered with water", "put * in water"),
]

season_changes = [
    ("in snow", "add snow effects"),
    ("in spring", "add spring effects"),
    ("in summer", "add summer effects"),
    ("in autumn", "add autumn effects"),
    ("during daytime", "make the scene in daytime"),
    ("during nighttime", "make the period in nighttime"),
]

background_changes = [
    ("in front of a mountain", "add mountain in the background"),
    ("in front of the pyramids", "add the pyramids in the background"),
]

PRODUCTS = [
    "t-shirt",
    "shirt",
    "dress",
    "pants",
    "shoe",
    "watch",
    "vase",
    "sneaker",
    "headphone",
    "bottle",
    "perfume",
    "vase",
    "cup",
    "camera",
    "phone",
    "mobile",
    "bag",
    "earpod",
    "earbud",
    "heel",
]


def find_words(lst, input):
    found_words = []
    for w in lst:
        indx = input.find(w)
        if indx != -1:
            if indx + len(w) + 1 < len(input) and input[indx + len(w) + 1] == "s":
                w += "s"

            found_words.append(w)

    return found_words


def perform_color_changes(input, mixed_color=False):
    if input.endswith("s"):
        input = input[:-1]

    original_input = input
    result = []
    found_words = find_words(PRODUCTS, input)

    # remove colors to avoid repeated consecutive colors
    for change, _ in color_changes:
        changee = " "
        if mixed_color == True:
            changee = change + "-"

        input = input.replace(str(" " + change + " "), changee).replace("  ", " ")

    for word in found_words:
        for change, change_text in color_changes:
            edit = change_text.replace("*", word)
            changed = str(change + " " + word)
            output = input.replace(word, changed)

            result.append({"caption": original_input, "edit": edit, "output": output})

    return result


def perform_scene_changes(input):
    original_input = input
    for change, _ in scene_changes:
        input = input.replace(change, "")

    result = []
    found_words = find_words(PRODUCTS, input)
    for word in found_words:
        for change, change_text in scene_changes:
            edit = change_text
            edit = edit.replace("*", word)

            output = input + " " + change

            result.append(
                {
                    "caption": original_input,
                    "edit": edit,
                    "output": output.replace("  ", " "),
                }
            )

    return result


def perform_affects_changes(input):
    original_input = input
    for change, _ in background_changes:
        input = input.replace(change, "")

    result = []
    found_words = find_words(PRODUCTS, input)

    for _ in found_words:
        for change, change_text in season_changes:
            edit = change_text
            output = input + " " + change

            result.append(
                {
                    "caption": original_input,
                    "edit": edit,
                    "output": output.replace("  ", " "),
                }
            )

        break
    return result


def perform_background_changes(input):
    original_input = input
    for change, _ in background_changes:
        input = input.replace(change, "")

    result = []
    found_words = find_words(PRODUCTS, input)

    for _ in found_words:
        for change, change_text in background_changes:
            edit = change_text
            output = input + " " + change

            result.append(
                {
                    "caption": original_input,
                    "edit": edit,
                    "output": output.replace("  ", " "),
                }
            )
        break

    return result


def get_rows(input):  # return: list of dictionary
    input = input.lower().replace("-", " ")
    # remove brands
    input = input.replace("nike ", "")
    result = []

    color_changes_result = perform_color_changes(input, False)
    for new_row in color_changes_result:
        result.append(new_row)

    scene_changes_result = perform_scene_changes(input)
    for new_row in scene_changes_result:
        result.append(new_row)

    affects_changes_result = perform_affects_changes(input)
    for new_row in affects_changes_result:
        result.append(new_row)

    background_changes_result = perform_background_changes(input)
    for new_row in background_changes_result:
        result.append(new_row)

    return result


def statistics(strs):
    total = 0
    stat = {}
    for product in PRODUCTS:
        cntr = sum(product.lower() in s.lower() for s in strs)
        total += cntr
        stat[product] = cntr

    stat = dict(sorted(stat.items(), key=lambda item: item[1], reverse=True))

    return stat, total


def load_dataset(path):

    dataset = pd.read_csv(path)
    return dataset


def save_dataset(data, file_path):
    with open(file_path, "w") as file:
        for idx in range(len(data)):
            json_string = json.dumps(data[idx]) + ("\n" if idx < len(data) - 1 else "")
            file.write(json_string)


def insert_row(df, new_data: list):
    # Create a DataFrame with the new row data
    new_data = pd.DataFrame(new_data, columns=df.columns)
    # Append the new row to the existing DataFrame
    df = df.append(new_data, ignore_index=True)
    return df


def main():
    input_dataset = load_dataset("Dataset/input_dataset.csv")
    outout_dataset = []

    for val in input_dataset["caption"]:
        newData = get_rows(val)
        if len(newData) > 0:
            outout_dataset += newData

    stat, total = statistics([item["caption"] for item in outout_dataset])
    stat = pd.DataFrame([stat]).transpose()

    print(rf"TOTAL : {total}")
    print(stat)

    save_dataset(outout_dataset, "Dataset/textual_dataset.jsonl")


if __name__ == "__main__":
    main()
