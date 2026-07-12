from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import sessionLocal, DBExpense

class Expense(BaseModel):
    activity:str
    cost:float

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()  

app=FastAPI()
expenses=[]

@app.get("/")
def read_root():
    return {"message": "Welcome to the Expense Tracker API! Head over to /docs to test the endpoints."}

@app.post("/expenses/")
def add_expense(expense:Expense, db: Session = Depends(get_db)):
    global current_id
    item = DBExpense(activity=expense.activity, cost=expense.cost)

    db.add(item)
   
    db.commit()
    db.refresh(item)
    return {"message":"Item added successfully","Expense":item}

@app.get("/expenses/")
def list_expenses(db: Session = Depends(get_db)):
    expenses = db.query(DBExpense).all()
    return {"List of Expenses":expenses}

@app.put("/expenses/{expense_id}")
def update_expense(expense_id:int, expense:Expense, db: Session = Depends(get_db)):
    item = db.query(DBExpense).filter(DBExpense.id == expense_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    item.activity = expense.activity
    item.cost = expense.cost
    
    db.commit()
    db.refresh(item)
    return {"message": "Expense updated successfully", "updated_item": item}
    

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id:int):
    for i,item in enumerate(expenses):
        if item["id"]==expense_id:
            deleted=expenses.pop(i)
            return{"message":"Deleted Successfully","deleted":deleted}
    raise HTTPException(status_code=404, detail="Expense not found")