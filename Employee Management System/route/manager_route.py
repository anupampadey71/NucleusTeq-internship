from fastapi import APIRouter, HTTPException
from config.databases import sql, cursor
from model.manager_models import Register  
from schema.manager_schema import list_serial  

manager_router = APIRouter()

@manager_router.post("/")
async def add_manager(info: Register):
    """Add a new manager"""
    sql_query = "INSERT INTO manager VALUES (%s, %s);"
    try:
        cursor.execute(sql_query, (info.managerId, info.employeeId))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Manager added successfully"}

@manager_router.get("/")
async def get_managers():
    """Get all managers"""
    sql_query = "SELECT * FROM manager;"
    try:
        cursor.execute(sql_query)
        managers = cursor.fetchall()
        result = list_serial(managers)  # Assuming you have a function to serialize manager data
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@manager_router.put("/{managerId}")
async def update_manager(managerId: str, employeeId: str):
    """Update manager"""
    sql_query = "UPDATE manager SET employeeId = %s WHERE managerId = %s;"
    try:
        cursor.execute(sql_query, (employeeId, managerId))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Manager updated successfully"}

@manager_router.delete("/{managerId}")
async def delete_manager(managerId: str):
    """Delete manager"""
    sql_query = "DELETE FROM manager WHERE managerId = %s;"
    try:
        cursor.execute(sql_query, (managerId,))
        sql.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Manager deleted successfully"}
