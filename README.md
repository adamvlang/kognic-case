# Kognic case
Kognic Case is an annotation convertion tool that converts from Kognic format to Open Label format.

It contains three major parts

- The convertion library that performs the actual converion
- The rest api based on fastapi
- The mainfile that converts a file from kognic to open label format

## How to setup
It could be run in python >= 3.9 but I have used 3.10 and that is what is used in the setup instructions.
The instructions below are for Linux, if you are using windows or mac the instructions could vary slightly.
1) Set up an virtual environment
```
>python3.10 -m venv --prompt kognic_case .env
```
2) Activate virtual environment
```
>source .emv/bin/activate
```
3) Install required packages
```
>pip install -r requirements.txt
```
Once these steps are complete you are free to choose to use either the REST API or the library

### Running REST API
The rest api are based on fastapi and uses uvicorn to run a server.
1) Set up virtual environment as described above.
2) Start the uvicorn server
```
>uvicorn --reload annotation_convertion_api:app --port 8000
```
3) Once the server is running you can test the API using curl with the kognic file as "KOGNIC-PAYLOAD-JSON". You could copy the content in kognic_1.json and use that as the "KOGNIC-PAYLOAD-JSON".
```
>curl -X 'POST'   'http://localhost:8000/kognic_to_openlabel'   -H 'accept: application/json'   -H 'Content-Type: application/json'   -d '<KOGNIC-PAYLOAD-JSON>'
```
### Running main.py
The main.py uses the annotation convertion as a library inside a python program.
1) Set up virtual environment as described above.
2) Run main.py, to change file simply change the <path_to_kognic_annotation> variable inside the program. The current implementation prints the converted file to console.
```
>python3.10 main.py
```

