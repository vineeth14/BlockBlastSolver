from fastapi import FastAPI
from fastapi import UploadFile, HTTPException, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from solve import solve_board, create_shapes, generate_step_boards
from image_select import image_to_grid, read_shapes_to_grid
from PIL import Image
import io
import uuid

app = FastAPI()

origins = [
    "http://localhost:4200",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins
)

processing_status ={}
def process_image(image):

    image = Image.open(io.BytesIO(image))
    board = image_to_grid(image)
    grid = read_shapes_to_grid(image)
    shapes = create_shapes(grid)
    turn =solve_board(board,shapes)
    completion_counter,stepBoards = generate_step_boards(board, shapes, turn)
    # Store the result and update status.

    return board,stepBoards,completion_counter


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/upload/")
async def create_upload_file(file: UploadFile, background_tasks: BackgroundTasks):
    image = await file.read()
    board,stepBoards,completion_counter = process_image(image)
    stepBoards_serialized = [step.tolist() for step in stepBoards]
    response_object = {
        'board': board.tolist(),
        'stepBoards': stepBoards_serialized,
        'completion_counter': completion_counter
    }
    return response_object

