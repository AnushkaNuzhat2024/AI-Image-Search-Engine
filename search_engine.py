"""Import the required libraries"""

from nicegui import ui
from PIL import Image
import os
import torch
import io
from sentence_transformers import SentenceTransformer, util

"""Load CLIP model"""

model = SentenceTransformer('clip-ViT-L-14')

"""Load images from the database (Folder)"""

image_query = ''
folder_path = 'images'
device = 'cuda' if torch.cuda.is_available() else 'cpu'
image_embedding = []
if os.path.exists(folder_path):
    file_list = os.listdir(folder_path)
    file_list = [file_name for file_name in file_list if file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif'))]
    if len(file_list) > 0:
        image_embedding = model.encode([Image.open(os.path.join(folder_path, image_file)) for image_file in file_list], batch_size=128, convert_to_tensor=True)
    else:
        print(f"The folder '{folder_path}' does not contain any images.")

else:
    print(f"The folder '{folder_path}' does not exist.")

"""Define Searching Method"""

def search_images(query, top_k=3):
    query_embedding = model.encode([query], convert_to_tensor=True)
    picks = util.semantic_search(query_embedding, image_embedding, top_k=top_k)[0]
    return [file_list[pick['corpus_id']] for pick in picks]

"""Update the grid based on the user input."""

def update_grid(input_value, top_k=10):
    top_picks = search_images(input_value, top_k)
    images = [os.path.join(folder_path, image_file) for image_file in top_picks]
    grid.clear()
    with grid:
        for image_path in images:
            with ui.card():
                ui.image(image_path).style('width: 100%; height: auto;')

"""Handle the submit button action."""

def handle_submit():
    input_type = input_selection.value
    input_value = text_input.value if input_type == 'Text' else image_query
    top_k = 10
    if top_pick_input.value:
        top_k = int(top_pick_input.value)
    update_grid(input_value, top_k)

"""Toggle visibility of text and image input fields."""

def toggle_input_visibility():
    if input_selection.value == 'Text':
        text_input.style('display:block')
        image_input.style('display:none')
    else:
        text_input.style('display:none')
        image_input.style('display:block')

"""Handle image upload and display."""

def handle_image_upload(event):
    content = event.content.read()
    global image_query
    image_input.clear()
    image_query = Image.open(io.BytesIO(content))


"""Create the UI components."""

ui.dark_mode().enable()

with ui.row().classes('w-full flex-center items-center gap-4'):
    ui.label('AI Image Search Engine').classes('text-2xl mb-4 font-semibold')

with ui.row().classes('w-full flex-center items-center gap-4'):
    input_selection = ui.toggle(['Text', 'Image'], value='Text', on_change=lambda: toggle_input_visibility())

with ui.row().classes('w-full flex-center items-center gap-4'):
    text_input = ui.input('Enter text here...').props('clearable').classes('flex-col col-12 col-md-8')
    image_input = ui.upload(label='Upload Image', auto_upload=True, on_upload=lambda e: handle_image_upload(e)).classes('max-w-full col-12 col-md-4').style('display:none')

with ui.row().classes('w-full flex-center items-center gap-4'):
    top_pick_input = ui.input('Top picks').props('type="number"')
    ui.button('Submit', on_click=handle_submit)
    
grid = ui.grid(columns=3).classes('w-full p-8')

ui.run()

