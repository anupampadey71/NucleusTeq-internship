# importing the modules
from fastapi import FastAPI
from route.employee_route import employee_router
app = FastAPI()

@app.get("/")
async def main():
    return {"msg" : "Hey Everyone"}

app.include_router(employee_router, prefix="/employees", tags=["Employees"])
