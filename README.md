# Text-Driven Image-to-Image Generation

### [Deployment](https://huggingface.co/spaces/Graduation-Proect-Team/Text_Driven_Image_to_Image_Generation) | [Dataset](https://huggingface.co/datasets/Graduation-Proect-Team/Text-Driven-I2I-Generation-Dataset)

This work aims to apply a deep learning model to update images based on text input, essential for social media, advertising, and content creation. Users can upload an image and provide text instructions for modifications. The system interprets these instructions to update the image while maintaining high visual quality.

## Table of Contents

- [Features](#Features)
- [Tools](#Tools)
- [Screenshots](#Screenshots)
- [Dataset](#Dataset)
- [TeamMembers](#TeamMembers)

## Features

- the user can specify paramters that affects the output generation:
  - Steps: Number of steps.
  - Seed: The initial random value used to start the image generation process. Changing the seed value can result in different outputs for the same input.
  - Text CFG(Classifier free guidance): The effect of the text on the generated image, as it increases the change in the generated image increases.
  - Image CFG(Classifier free guidance): How much the generated image will be similar to the input image, as it increases the generated image will be similar to the input image.
  - Resolution: The quality and resolution of the generated image.
- The Dataset generation code is provided in location /Dataset_Generation and it is splitted into 2 parts:
  - Textual Dataset Generation: This part is responsible for the textual dataset generation process to obtain high-quality prompts that will be used to generate the images for the training dataset.
  - Image Dataset Generation: A notebook that is responsible for generating the images in the dataset. The code provides the final shape of the dataset.

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
