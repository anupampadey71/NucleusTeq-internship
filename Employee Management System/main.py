from fastapi import FastAPI
from route.employee_route import employee_router
from route.department_route import department_router
from route.skillset_route import skillset_router
from route.manager_route import manager_router
from route.employeeskill_route import employeeskill_router
from route.project_route import project_router
from route.request_route import request_router
from route.assignment_route import assignment_router
from route.auth_route import auth_router  # Import the auth router
from config.databases import sql, cursor

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get("/")
async def main():
    return {"msg" : "Hey Everyone"}



# Configure CORS
origins = [
    "http://localhost:3000",  # Adjust this to your frontend's origin
    # Add other allowed origins here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)




# Define endpoints for other routes
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])  # Include the auth router
app.include_router(employee_router, prefix="/employees", tags=["Employees"])
app.include_router(department_router, prefix="/departments", tags=["Departments"])
app.include_router(skillset_router, prefix="/skillsets", tags=["Skillsets"])
app.include_router(manager_router, prefix="/manager", tags=["manager"])
app.include_router(employeeskill_router, prefix="/employeeskill", tags=["employeeskill"])
app.include_router(project_router, prefix="/project", tags=["project"])
app.include_router(request_router, prefix="/request", tags=["request"])
app.include_router(assignment_router, prefix="/assignment", tags=["assignment"])

