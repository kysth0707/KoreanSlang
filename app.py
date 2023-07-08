from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import module
import uvicorn

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
async def convert(originalText : str):
	restoredText = module.restoreSplitedWord(originalText, circumventDict)
	joinedJamo = module.join_jamos(restoredText)
	module.toHappyWord(joinedJamo, badToHappyDict)

	convertedWord = ""
	canSend = True
	return {
		'canSend' : canSend,
		'originalWord' : originalText,
		'restoredText' : restoredText,
		'joinedJamo' : joinedJamo,
		'convertedWord' : convertedWord,
	}

if __name__ == "__main__":
	uvicorn.run("app:app", host="0.0.0.0", port=999, reload=True)