from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Any, Dict
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import database
import time
import llm_service

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Request Models ---

class ChatRequest(BaseModel):
    message: str

class DDLRequest(BaseModel):
    action: str
    table_name: str
    column_name: Optional[str] = None
    new_column_name: Optional[str] = None
    column_type: Optional[str] = None
    new_table_name: Optional[str] = None
    # For Foreign Keys
    fk_table: Optional[str] = None
    fk_column: Optional[str] = None
    constraint_name: Optional[str] = None

# --- API Endpoints ---

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize DB with sample data on startup"""
    # --- STARTUP PHASE ---
    try:
        database.init_db()
        print("Database initialized.")
    except Exception as e:
        print(f"Error connecting to DB: {e}")
@app.get("/schema")
def read_schema():
    try:
        return database.get_current_schema()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
def chat_with_data(request: ChatRequest):
    print(f"User Query: {request.message}")
    
    MAX_RETRIES = 5
    attempt = 0
    current_sql = ""
    last_error = ""
    
    try:
        # Step 1: Get Schema
        current_schema = database.get_current_schema()
        
        # Step 2: Initial Generation
        current_sql = llm_service.generate_sql_from_query(request.message, current_schema)
        
        # SELF-CORRECTION LOOP
        while attempt < MAX_RETRIES:
            
            if current_sql.startswith("-- Error"):
                return { "response": "LLM Connectivity Error", "sql": current_sql, "data": [] }

            print(f"Executing SQL (Attempt {attempt+1}): {current_sql}")
            
            # Try executing
            query_result = database.execute_query(current_sql)
            
            # Check for DB Errors
            if isinstance(query_result, dict) and "error" in query_result:
                last_error = query_result["error"]
                print(f"Database Rejected SQL: {last_error}")
                
                if attempt < MAX_RETRIES - 1:
                    print("Asking LLM to fix the query...")
                    current_sql = llm_service.fix_generated_sql(
                        request.message, 
                        current_sql, 
                        last_error, 
                        current_schema
                    )
                    attempt += 1
                    continue
                else:
                    return {
                        "response": f"I tried {MAX_RETRIES} times but couldn't fix the error. Last error: {last_error}",
                        "sql": current_sql,
                        "data": []
                    }
            
            return {
                "response": f"Success! (Executed after {attempt+1} attempts)",
                "sql": current_sql,
                "data": query_result
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ddl")
def execute_no_code_update(request: DDLRequest):
    sql = ""
    try:
        if request.action == "create_table":
            sql = f"CREATE TABLE {request.table_name} (id SERIAL PRIMARY KEY);"
        elif request.action == "add_column":
            if not request.column_name or not request.column_type:
                raise HTTPException(status_code=400, detail="Column name and type required")
            sql = f"ALTER TABLE {request.table_name} ADD COLUMN {request.column_name} {request.column_type};"
        elif request.action == "drop_column":
            if not request.column_name:
                raise HTTPException(status_code=400, detail="Column name required")
            sql = f"ALTER TABLE {request.table_name} DROP COLUMN {request.column_name};"
        elif request.action == "drop_table":
             sql = f"DROP TABLE {request.table_name} CASCADE;"
        elif request.action == "rename_table":
            if not request.new_table_name:
                raise HTTPException(status_code=400, detail="New table name required")
            sql = f"ALTER TABLE {request.table_name} RENAME TO {request.new_table_name};"
        elif request.action == "rename_column":
            if not request.column_name or not request.new_column_name:
                raise HTTPException(status_code=400, detail="Column names required")
            sql = f"ALTER TABLE {request.table_name} RENAME COLUMN {request.column_name} TO {request.new_column_name};"
        elif request.action == "alter_column_type":
            if not request.column_name or not request.column_type:
                raise HTTPException(status_code=400, detail="Column name and type required")
            sql = f"ALTER TABLE {request.table_name} ALTER COLUMN {request.column_name} TYPE {request.column_type} USING {request.column_name}::{request.column_type};"
        
        # --- NEW CONNECTION ACTIONS ---
        elif request.action == "add_foreign_key":
            # ALTER TABLE orders ADD CONSTRAINT fk_orders_users FOREIGN KEY (user_id) REFERENCES users(id)
            if not request.column_name or not request.fk_table or not request.fk_column:
                raise HTTPException(status_code=400, detail="FK details required")
            
            constraint_name = f"fk_{request.table_name}_{request.column_name}_{int(time.time())}"
            sql = f"ALTER TABLE {request.table_name} ADD CONSTRAINT {constraint_name} FOREIGN KEY ({request.column_name}) REFERENCES {request.fk_table}({request.fk_column});"

        elif request.action == "drop_foreign_key":
            if not request.constraint_name:
                raise HTTPException(status_code=400, detail="Constraint name required")
            sql = f"ALTER TABLE {request.table_name} DROP CONSTRAINT {request.constraint_name};"

        else:
            raise HTTPException(status_code=400, detail=f"Unknown action: {request.action}")

        print(f"Executing DDL: {sql}")
        result = database.execute_query(sql)
        if isinstance(result, dict) and "error" in result:
             raise HTTPException(status_code=400, detail=result["error"])

        return {"status": "success", "sql_executed": sql}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)