from manager import Manager
from fastapi import FastAPI
import uvicorn


app = FastAPI()

manager = Manager()
manager.run()


@app.get('/')
def homepage():
    return 'visit /data'

@app.get('/data')
def get_data():
    return manager.get_data()

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)