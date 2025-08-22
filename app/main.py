from manager import Manager
from fastapi import FastAPI


app = FastAPI()

manager = Manager()
manager.run()


@app.get('/')
def homepage():
    return 'visit /data'

@app.get('/data')
def get_data():
    return manager.get_data()