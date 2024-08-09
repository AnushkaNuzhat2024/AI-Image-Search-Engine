
# AI Image Search Engine
The AI Image Search Engine is a powerful tool that allows users to search for images based on text or image input. It leverages the capabilities of the CLIP model developed by OpenAI and the sentence-transformers library provided by Hugging Face. The User Interface is developed using the NiceGUI Python library.

## Features

- Text-based search: Users can enter a description or keywords to search for relevant images in the database.
- Image-based search: Users can upload an image and the engine will find similar images in the database.
- Database of images: The engine considers a folder of images as the database, making it easy to manage and update.

## Dependency
1. Python >= 3.8 - https://www.python.org/downloads/
2. Anaconda/Miniconda -  https://docs.anaconda.com/miniconda/

## Getting Started

To get started with the AI Image Search Engine, follow these steps:

1. Create a new conda environment and activate it:
```bash
conda create -n clip
conda activate clip
```
2. Install packages:
```bash
conda install pytorch torchvision torchaudio cpuonly -c pytorch
pip install nicegui pillow sentence-transformers
```
3. Run the python script
```bash
python search_engine.py
```

## Usage

Once the AI Image Search Engine is set up, you can use it in the following ways:

- Text-based search: Enter a description or keywords in the provided input field and click the submit button. The engine will display the most relevant images based on your query.
- Image-based search: Upload an image using the provided file submit button. The engine will find similar images in the database and display them.
- Additionally, you can specify how many images to view by providing top picks value (default 10).

## References

1. https://github.com/openai/CLIP
2. https://huggingface.co/models?library=sentence-transformers
3. https://nicegui.io/