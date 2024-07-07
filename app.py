import os
import math
import gradio as gr
from Helper_functions import *
from Kaggle_API import API_Connection
from GoogleDrive_API import GoogleDrive_API

DEFAULT_VALUES = {
    "input_image": None,
    "edit_instruction": "",
    "steps": 100,
    "randomize_seed": "Fix Seed",
    "seed": 1371,
    "randomize_cfg": "Fix CFG",
    "text_cfg_scale": 7.5,
    "image_cfg_scale": 1.5,
    "resolution": 512,
    "edited_image": None
}
HELP_TEXT = """
If you're not getting what you want, there may be a few reasons:
1. Is the image not changing enough? Your Image CFG weight may be too high. This value dictates how similar the output should be to the input. It's possible your edit requires larger changes from the original image, and your Image CFG weight isn't allowing that. Alternatively, your Text CFG weight may be too low. This value dictates how much to listen to the text instruction. The default Image CFG of 1.5 and Text CFG of 7.5 are a good starting point, but aren't necessarily optimal for each edit. Try:
    * Decreasing the Image CFG weight
    * Incerasing the Text CFG weight
2. Conversely, is the image changing too much, such that the details in the original image aren't preserved? Try:
    * Increasing the Image CFG weight
    * Decreasing the Text CFG weight
3. Try generating results with different random seeds by setting "Randomize Seed" and running generation multiple times. You can also try setting "Randomize CFG" to sample new Text CFG and Image CFG values each time.
4. Rephrasing the instruction sometimes improves results (e.g., "turn him into a dog" vs. "make him a dog" vs. "as a dog").
5. Increasing the number of steps sometimes improves results.
6. Do faces look weird? The Stable Diffusion autoencoder has a hard time with faces that are small in the image. Try:
    * Cropping the image so the face takes up a larger portion of the frame.
"""


def generate_button_clicked(*args):
    # set kaggle-api variables
    kaggle_username = os.environ["kaggle_username"]
    kaggle_key = os.environ["kaggle_key"]

    input_keys = list(DEFAULT_VALUES.keys())
    values = dict(zip(input_keys, list(args)))

    for key in values:
        if values[key] is None:
            values[key] = DEFAULT_VALUES[key]

    if values["randomize_seed"]:
        values["seed"] = random.randint(1, 100000)

    if values["randomize_cfg"]:
        values["text_cfg_scale"] = round(random.uniform(6.0, 9.0), ndigits=2)
        values["image_cfg_scale"] = round(random.uniform(1.2, 1.8), ndigits=2)

    # parameters for the model
    input_image = values["input_image"]
    edit_instruction = values["edit_instruction"]
    steps = values["steps"]
    seed = values["seed"]
    cfgtext = values["text_cfg_scale"]
    cfgimage = values["image_cfg_scale"]
    resolution = 2 ** int(math.log2(values["resolution"]))

    if input_image is None:
        raise gr.Error("Missing Input: input_image")
    if len(edit_instruction) == 0: # perform no edit
        return [input_image, seed, cfgtext, cfgimage]

    GoogleDrive_connection_Path = ""
    # GoogleDrive_connection_Path = "service_account.json"
    GoogleDrive_connection = GoogleDrive_API(GoogleDrive_connection_Path)
    api_connection = API_Connection(GoogleDrive_connection, kaggle_username, kaggle_key)

    create_folder("local_dataset")

    image_ID = get_random_str(4)
    input_image_name = rf"input_image_{image_ID}.png"
    output_image_name = rf"output_image_{image_ID}.png"

    input_image.save(rf"local_dataset\{input_image_name}")

    status, img = api_connection.generate_image(
        input_image_name, edit_instruction, output_image_name,
        steps, seed, cfgtext, cfgimage, resolution
    )
    print(rf"End Time : {get_current_time()}")
    if not status:
        raise gr.Error(img)

    return [img, seed, cfgtext, cfgimage]


def reset_button_clicked():
    return list(DEFAULT_VALUES.values())


def main():
    with gr.Blocks(theme="AmirMoris/GP_Themes") as demo:
        toggle_theme = gr.Button(value="Toggle Theme")
        with gr.Row():
            input_image = gr.Image(label="Input Image", type="pil", interactive=True)
            edited_image = gr.Image(label=f"Edited Image", type="pil", interactive=False)

        with gr.Row():
            with gr.Column(scale=3):
                instruction = gr.Textbox(lines=1, label="Edit Instruction", interactive=True)
            with gr.Column(scale=1, min_width=100):
                with gr.Row():
                    generate_button = gr.Button("Generate")
                with gr.Row():
                    reset_button = gr.Button("Reset")

        with gr.Row():
            steps = gr.Number(value=DEFAULT_VALUES["steps"], precision=0, label="Steps", interactive=True)
            randomize_seed = gr.Radio(
                ["Fix Seed", "Randomize Seed"],
                value=DEFAULT_VALUES["randomize_seed"],
                type="index",
                show_label=False,
                interactive=True,
            )
            seed = gr.Number(value=DEFAULT_VALUES["seed"], precision=0, label="Seed", interactive=True)
            randomize_cfg = gr.Radio(
                ["Fix CFG", "Randomize CFG"],
                value=DEFAULT_VALUES["randomize_cfg"],
                type="index",
                show_label=False,
                interactive=True,
            )
            text_cfg_scale = gr.Number(value=DEFAULT_VALUES["text_cfg_scale"], label=f"Text CFG", interactive=True)
            image_cfg_scale = gr.Number(value=DEFAULT_VALUES["image_cfg_scale"], label=f"Image CFG", interactive=True)
            resolution = gr.Number(value=DEFAULT_VALUES["resolution"], label=f"Resolution", interactive=True)

        gr.Markdown(HELP_TEXT)

        generate_button.click(
            fn=generate_button_clicked,
            inputs=[
                input_image,
                instruction,
                steps,
                randomize_seed,
                seed,
                randomize_cfg,
                text_cfg_scale,
                image_cfg_scale,
                resolution
            ],
            outputs=[edited_image, seed, text_cfg_scale, image_cfg_scale],
        )
        reset_button.click(
            fn=reset_button_clicked,
            outputs=[
                input_image,
                instruction,
                steps,
                randomize_seed,
                seed,
                randomize_cfg,
                text_cfg_scale,
                image_cfg_scale,
                resolution,
                edited_image
            ],
        )
        toggle_theme.click(
            None,
            js=
            """
            () => {
                document.body.classList.toggle('dark');
            }
            """,
        )


    # Launch Gradio interface
    demo.queue(max_size=1)
    demo.launch(share=True)


if __name__ == "__main__":
    main()