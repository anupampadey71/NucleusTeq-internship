# importing the modules
from fastapi import FastAPI
from route.employee_route import employee_router
from route.department_route import department_router
from route.skillset_route import skillset_router
from route.manager_route import manager_router
app = FastAPI()

@app.get("/")
async def main():
    return {"msg" : "Hey Everyone"}

app.include_router(employee_router, prefix="/employees", tags=["Employees"])
app.include_router(department_router, prefix="/departments", tags=["Departments"])
app.include_router(skillset_router, prefix="/skillsets", tags=["Skillsets"])
app.include_router(manager_router, prefix="/manager", tags=["manager"])