# CodeGen
C/C++ Source Code Generator based on JSON schema

## Usage
```
python3 codegen.py --help
usage: codegen.py [-h] [--json-file JSON_FILE] [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [--gen-c-header] [--gen-mock-cpp]

Generate C/C++ sources from JSON schema

optional arguments:
  -h, --help            show this help message and exit
  --json-file JSON_FILE
                        path to JSON schema file
  --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Log level for the script
  --gen-c-header        Generate C header file from JSON schema
  --gen-mock-cpp        Generate C++ gMock header & sources from JSON schema
```
