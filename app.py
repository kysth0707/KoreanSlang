from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import module
import uvicorn
import time

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)

circumventDict = module.getCircumventDict()
badToHappyDict = module.getBadToHappyDict()

@app.get('/')
def home():
	return "goto /docs"

@app.get('/convert/{txt}')
async def convert(txt : str):
	lastTime = time.time()

	convertedWord, joinedJamo, canSend, changedWordCount, = module.convertToGoodWriting(txt, circumventDict, badToHappyDict)
	return {
		'canSend' : canSend,
		'originalWord' : txt,
		'joinedJamo' : joinedJamo,
		'changedWordCount' : changedWordCount,
		'convertedWord' : convertedWord,
		'time' : time.time() - lastTime
	}

if __name__ == "__main__":
	uvicorn.run("app:app", host="0.0.0.0", port=7979, reload=True)