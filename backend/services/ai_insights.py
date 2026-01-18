from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import psycopg2
import os

router = APIRouter()

class UserData(BaseModel):
    user_id: int
    health_data: dict

def get_db_connection():
    try:
        connection = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        return connection
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database connection error")

def fetch_user_data(user_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT health_data FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            raise HTTPException(status_code=404, detail="User not found")
    finally:
        cursor.close()
        connection.close()

def generate_insights(health_data: dict) -> str:
    prompt_template = PromptTemplate(
        input_variables=["health_data"],
        template="Based on the following health data, provide personalized insights: {health_data}"
    )
    llm = OpenAI(temperature=0.7)
    chain = LLMChain(llm=llm, prompt=prompt_template)
    return chain.run(health_data)

@router.post("/ai/insights")
async def get_ai_insights(user_data: UserData):
    try:
        health_data = fetch_user_data(user_data.user_id)
        insights = generate_insights(health_data)
        return {"insights": insights}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error generating insights")