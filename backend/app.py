from dotenv import load_dotenv
import os
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional, List
import motor.motor_asyncio
import uuid
import uvicorn
load_dotenv()

MONGODB_URL = os.getenv('MONGODB_URL')

app = FastAPI()
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5173)

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

#college is the database name
db = client.college

def generate_uuid():
    return uuid.uuid4().hex

# create a base model / primary model for the student
class StudentModel(BaseModel):
    #default_factory is used to generate a new id automatically
    #3 dots (...) means required field
    id: str = Field(default_factory=generate_uuid)
    name: str = Field(...)
    email: EmailStr = Field(...)
    course: str = Field(...)
    gpa: float = Field(..., le=4.0)

    class Config:
        allow_population_by_field_name = True # allows populating model instances using dictionaries with field names as keys
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str} 
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "course": "Experiments, Science, and Fashion in Nanophotonics",
                "gpa": "3.0",
            }
        }


# updateStudentModel
# no id and no required fields
class UpdateStudentModel(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    course: Optional[str]
    gpa: Optional[float]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "course": "Experiments, Science, and Fashion in Nanophotonics",
                "gpa": "3.0",
            }
        }



# response model
class StudentResponseModel(BaseModel):
    success:bool
    message:str
    content: List[StudentModel]

#Create Student Route
# 5 routes: POST, GET, GET by ID, PUT by ID, DELETE by ID


# POST request
# receive in JSON decode into Python dict
@app.post("/", response_description= "Add new student", response_model=StudentModel)
async def create_student(student: StudentModel = Body(...)):
    student = jsonable_encoder(student)
    new_student = await db["students"].insert_one(student)
    #_id is the object(_id) which is auto created by MongoDB
    created_student = await db["students"].find_one({"_id": new_student.inserted_id})
    response_content = StudentResponseModel(
        success= True,
        message = "New student added successfully",
        content = [created_student]
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=response_content.dict())


# GET request for all students
@app.get("/", response_description="List all students", response_model=StudentResponseModel)
async def list_students():
    #to_list() method returns a list of all the documents in the collection
    #1000 is hardcoded, you should use pagination
    students = await db["students"].find().to_list(1000)
    response_content = StudentResponseModel(
        success= True,
        message = "Students retrieved successfully",
        content = students
    )
    return JSONResponse(status_code=status.HTTP_200_OK, content=response_content.dict())

# GET request for a single student
@app.get("/{id}", response_description="Get a single student",response_model=StudentResponseModel)
async def show_student(id: str):
    if (student := await db["students"].find_one({"id": id})) is not None:
        response_content = StudentResponseModel(
            success=True,
            message=f"Student with ID {id} retrieved successfully",
            content=[student]
        )
        return JSONResponse(status_code=status.HTTP_200_OK, content=response_content.dict())
    else:
        response_content = StudentResponseModel(
            success=False,
            message=f"Student with id {id} not found",
            content=[]
        )
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=response_content.dict())
    
# PUT request for a single student 
@app.put("/{id}", response_description="Update a student", response_model=StudentResponseModel)
async def update_student(id:str, student: UpdateStudentModel = Body(...)):
    # go through the student input model and remove any fields that are not provided
    student = {k:v for k,v in student.dict().items() if v is not None}

    # if there is at least one field in the student input model, update the student
    if len(student) >= 1:
        update_result = await db["students"].update_one({"id":id}, {"$set":student})
        
        # if update is successful, return the updated student
        if update_result.modified_count == 1:
            if(
                update_student := await db["students"].find_one({"id":id})
            ) is not None:
                response_content = StudentResponseModel(
                    success= True,
                    message = f"Student with id {id} update successfully",
                    content = [update_student]
                )
                return JSONResponse(status_code=status.HTTP_200_OK, content=response_content.dict())

    #it is possible that the student is not updated, so we return the existing student   
    if (existing_student := await db["students"].find_one({"_id":id})) is not None:

        response_content = StudentResponseModel(
            success= True,
            message = f"Student with id {id} update successfully",
            content = [existing_student]
        )       
        return JSONResponse(status_code=status.HTTP_200_OK, content=response_content.dict())
    
    # if student is not found, return 404
    else:
        response_content = StudentResponseModel(
            success= False,
            message = f"Student with id {id} not found",
            content = []
        )       
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=response_content.dict())
    

#DELETE request for a single student
@app.delete("/{id}", response_description="Delete a student", response_model=StudentResponseModel)
async def delete_student(id: str):
    delete_result = await db["students"].delete_one({"id":id})

    # the student is deleted successfully
    if delete_result.deleted_count == 1:
        response_content = StudentResponseModel(
            success= True,
            message = f"Student with id {id} deleted successfully",
            content = []
        )       
        return JSONResponse(status_code=status.HTTP_200_OK, content=response_content.dict())
    
    # the student is not found. 
    else:
        response_content = StudentResponseModel(
            success= False,
            message = f"Student with id {id} not found",
            content = []
        )       
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=response_content.dict())
