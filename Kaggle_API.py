import time

from Helper_functions import *


class API_Connection:
    def __init__(self, gd_connection, kaggle_username: str = "", kaggle_key: str = ""):
        os.environ["KAGGLE_USERNAME"] = kaggle_username
        os.environ["KAGGLE_KEY"] = kaggle_key

        self.GoogleDrive_connection = gd_connection

        self.NOTEBOOK_ID = "amirmorris/pix2pix-model"
        self.DATASET_NAME = "dataset"

    def pull_kaggle_notebook(self, notebook_path: str):
        command = rf"kaggle kernels pull {self.NOTEBOOK_ID} -p {notebook_path} -m"
        return execute_terminal_command(command)

    def push_kaggle_notebook(self, notebook_path: str):
        command = rf"kaggle kernels push -p {notebook_path}"
        return execute_terminal_command(command)

    def get_notebook_status(self):
        command = rf"kaggle kernels status {self.NOTEBOOK_ID}"
        return execute_terminal_command(command)

    def run(self, notebook_path: str):
        self.pull_kaggle_notebook(notebook_path)
        return self.push_kaggle_notebook(notebook_path)

    def generate_image(self, input_image_name: str, edit_instruction: str, output_image_name: str,
                       steps: int, seed: int, cfgtext: float, cfgimage: float, resolution: int
                       ):

        if len(input_image_name) == 0:
            return False, rf"Missing Input: input_image"

        if len(edit_instruction) == 0:
            return False, rf"Missing Input: edit_instruction"

        if len(output_image_name) == 0:
            return False, rf"Output Error: Missing output_image path"

        current_time = get_current_time()
        print(rf"Start Time : {current_time}")

        dataset_path = correct_path(self.DATASET_NAME)
        notebook_path = correct_path("notebook")

        create_folder(dataset_path)

        # copy image to the dataset
        copy_file(rf"local_dataset\{input_image_name}", rf"{dataset_path}\{input_image_name}")

        data = [
            {
                "time": current_time,
                "edit_instruction": edit_instruction,
                "input_image_path": input_image_name,
                "output_image_path": output_image_name,
                "steps": steps,
                "seed": seed,
                "cfg-text": cfgtext,
                "cfg-image": cfgimage,
                "resolution": resolution
            }
        ]

        write_file(data, dataset_path, "data.json")

        # update dataset
        self.GoogleDrive_connection.upload_file("data.json", rf"{self.DATASET_NAME}\data.json")
        self.GoogleDrive_connection.upload_file(input_image_name, rf"{self.DATASET_NAME}\{input_image_name}")

        # run notebook
        print(self.run(notebook_path))

        number_of_checks = 0
        while True:
            status = str(self.get_notebook_status()).replace("\n", "")
            print(rf"- status no #{number_of_checks} : {status}")
            number_of_checks += 1
            if "complete" in status:
                break

            if "error" in status:
                return False, "notebook status error"
            if "cancelAcknowledged" in status:
                return False, "notebook status cancelAcknowledged"
            time.sleep(120)

        # get output
        self.GoogleDrive_connection.download_file(
            output_image_name, rf"{dataset_path}\{output_image_name}"
        )
        output_image = read_image(rf"{dataset_path}\{output_image_name}")

        if output_image is None:
            return False, "An error occured while running, no output image found"

        return True, output_image


def main():
    pass


if __name__ == "__main__":
    main()