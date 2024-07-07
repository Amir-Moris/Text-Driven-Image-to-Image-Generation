# Text-Driven Image-to-Image Generation

### [Deployment](https://huggingface.co/spaces/Graduation-Proect-Team/Text_Driven_Image_to_Image_Generation) | [Dataset](https://huggingface.co/datasets/Graduation-Proect-Team/Text-Driven-I2I-Generation-Dataset)

This work aims to apply a deep learning model to update images based on text input, essential for social media, advertising, and content creation. Users can upload an image and provide text instructions for modifications. The system interprets these instructions to update the image while maintaining high visual quality.

## Table of Contents

- [Setup](#Setup)
- [Features](#Features)
- [Tools](#Tools)
- [Screenshots](#Screenshots)
- [Dataset](#Dataset)
- [TeamMembers](#TeamMembers)

## Setup

### Deployment Setup

#### Install dependencies

```bash
python -m venv env
.\env\Scripts\activate
```

#### Run

1. First, you need to create a notebook on Kaggle and use the code in `pix2pix-model.ipynb`.

2. Don't forget to modify the API keys for the Google Drive API to correctly download inputs and upload outputs so that the system works correctly.

3. You can upload the code to a hugging face space or run it locally using the following command:
```bash
python app.py
```

### Dataset Generation Setup
use the same dependencies that were used in the Deployment Setup
#### Run

```bash
python web_scrap.py
python main.py
```
#### Run
## Features

- the user can specify parameters that affect the output generation:
  - Steps: Number of steps.
  - Seed: The initial random value used to start the image generation process. Changing the seed value can result in different outputs for the same input.
  - Text CFG(Classifier free guidance): The effect of the text on the generated image, as it increases the change in the generated image increases.
  - Image CFG(Classifier free guidance): How much the generated image will be similar to the input image, as it increases the generated image will be similar to the input image.
  - Resolution: The quality and resolution of the generated image.
- The Dataset generation code is provided in `/Dataset_Generation` and you can specify the domain or the source of the generated dataset, we used the products domain and scrapped the textual dataset from [unsplash](https://unsplash.com/)

## Tools

- Python
- Pytorch
- CUDA
- Gradio Interface
- GoogleDrive API
- Kaggle API

## Screenshots

## Dataset

<p align="center">
    <img src="https://user-images.githubusercontent.com/83420413/171068520-cc285b9e-804a-4791-839f-bfcd26fac8d7.jpg" width="45%" height="100%" align="center" />
    <img src="https://user-images.githubusercontent.com/83420413/171070813-bfd8b5f9-cc6b-4d07-bcd1-dc5d3de37a63.jpg" width="45%" height="100%" align="center"/>
</p>

## TeamMembers

| Name            | Account                                                |
| --------------- | ------------------------------------------------------ |
| Amir Moris      | [@Amir-Moris](https://github.com/Amir-Moris)           |
| Verina Gad      | [@verina101](https://github.com/verina101)             |
| Maria Tawfek    | [@Maria801](https://github.com/Maria801)               |
| Mina Girgis     | [@Mina-Girgis](https://github.com/Mina-Girgis)         |
| Carolina George | [@carolina-george](https://github.com/carolina-george) |
