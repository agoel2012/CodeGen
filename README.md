# CodeGen
C/C++ Source Code Generator based on JSON schema

## Usage
```
python3 codegen/codegen.py --help
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

## Steps to build & generate C/C++ code
1. To generate C header, `python3 codegen.py --json-file ../src/include/db_api.json --gen-c-header`
2. To generate gMOCK sources, `python3 codegen.py --json-file ../src/include/db_api.json --gen-mock-cpp`
