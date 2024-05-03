from fastapi import APIRouter, HTTPException
from config.databases import sql, cursor
from model.request_models import Register
from schema.request_schema import list_serial

request_router = APIRouter()

@request_router.post("/")
async def create_request(request: Register):
    """Create a new request."""
    sql_query = "INSERT INTO request VALUES (%s, %s, %s, %s);"
    try:
        cursor.execute(sql_query, (request.requestId, request.projectId, request.skillId, request.status))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Request added successfully"}

@request_router.get("/all_requests")
async def get_all_requests():
    """Retrieve all requests."""
    sql_query = "SELECT * FROM request;"
    try:
        cursor.execute(sql_query)
        values = cursor.fetchall()
        result = list_serial(values)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return result

@request_router.put("/{requestId}")
async def update_request(requestId: str, status: str):
    """Update the status of a request."""
    sql_query = "UPDATE request SET status = %s WHERE requestId = %s;"
    try:
        cursor.execute(sql_query, (status, requestId))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Request status updated successfully"}

@request_router.delete("/{requestId}")
async def delete_request(requestId: str):
    """Delete a request."""
    sql_query = "DELETE FROM request WHERE requestId = %s;"
    try:
        cursor.execute(sql_query, (requestId,))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Request deleted successfully"}
