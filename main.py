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
    stepBoards = generate_step_boards(board, shapes, turn)
    # Store the result and update status.

    return stepBoards


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/upload/")
async def create_upload_file(file: UploadFile, background_tasks: BackgroundTasks):
    # if not file.content_type.startswith('image/'):
    #     raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail='Invalid format, file must be an image.')
    # try:
    #     image = await file.read()
    #     task_id = str(uuid.uuid4())
    #     processing_status[task_id] = {'status': 'processing'}
    #     background_tasks.add_task(process_image, image, task_id)
    # except Exception as e:
    #     print(f"Error processing image: {str(e)}")
    #     return HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail=str(e)
    #     )
    image = await file.read()
    stepBoards = process_image(image)
    stepBoards_serialized = [step.tolist() for step in stepBoards]
    return stepBoards_serialized



