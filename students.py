from fastapi import APIRouter
from schemas import Student
from db import collection
from bson.objectid import ObjectId


student_router=APIRouter()


def student_helper(student):
    return {
        "id":str(student["_id"]),
        "name":student["name"],
        "age":student["age"]
    }


@student_router.get('/')
async def get_all_students():
    students=[]
   
    async for student in collection.find():
        students.append(student_helper(student))

    return students


@student_router.post('/')
async def create_student(student_data:Student):
    new_student= await collection.insert_one(
        {
            "name":student_data.name,
            "age":student_data.age,
            "email":student_data.email
        }
    )

    created_student= await collection.find_one({"_id":new_student.inserted_id})

    return {"message":"Student created","student":student_helper(created_student)}


@student_router.get('/{student_id:str}')
async def get_student_by_id(student_id:str):
    student_to_get= await collection.find_one({"_id":ObjectId(student_id)})

    return {"message":"Student","student":student_helper(student_to_get)}

@student_router.put('/{student_id:str}')
async def update_student(student_id:str,student_data:dict):
    student_to_update= await collection.find_one({"_id":ObjectId(student_id)})


    if student_to_update:
        updated_student=  await collection.update_one(
            {"_id":ObjectId(student_id)},{"$set":student_data}
        )

        if updated_student:
            return True
        return False




@student_router.delete('/{student_id:str}')
async def delete(student_id:str):
    student_to_delete=await collection.find_one({"_id":ObjectId(student_id)})

    if student_to_delete:
        await collection.delete_one({"_id":ObjectId(student_id)})

        return {"message":"Student deleted"}

    return {"error":"not deleted"}


