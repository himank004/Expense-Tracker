from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel

class Expense(BaseModel):
    activity:str
    cost:float
    

app=FastAPI()
expenses=[]
current_id=1
@app.post("/expense")
def add_expense(expense:Expense):
    global current_id
    item={
        "id": current_id,
        "activity":expense.activity,
        "cost":expense.cost
    }

    expenses.append(item)
    current_id+=1
    return {"message":"Item added successfully","Expense":item}

@app.get("/expenses")
def list_expenses():
    return {"List of Expenses":expenses}

@app.put("/expenses/{expense_id}")
def update_expense(expense_id:int, expense:Expense):
    for item in expenses:
        if item["id"]==expense_id:
            item["activity"]=expense.activity
            item["cost"]=expense.cost
            return {"message": "Expense updated successfully", "updated_item": item}
    raise HTTPException(status_code=404, detail="Expense not found")

@app.delete("/expense/{expense_id}")
def delete_expense(expense_id:int):
    for i,item in enumerate(expenses):
        if item["id"]==expense_id:
            deleted=expenses.pop(i)
            return{"message":"Deleted Successfully","deleted":deleted}
    raise HTTPException(status_code=404, detail="Expense not found")