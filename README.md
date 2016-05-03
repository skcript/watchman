# Watchman
A Watchdog that pings file changes to an API of your choice.

### Default YAML config
```
  source:
    - /SHRINK/active/home
  regexes:
    - "([a-zA-Z0-9_ -/]*)/active/home/(\\w+)/uploads/(\\d+)/hot_root/"
  endpoints:
    file_create: "http://localhost/api/v2/files/create"
    folder_create: "http://localhost/api/v2/folders/create"
    file_move: "http://localhost/api/v2/files/move"
    folder_move: "http://localhost/api/v2/folders/move"
    file_destroy: "http://localhost/api/v2/files/destroy"
    folder_destroy: "http://localhost/api/v2/folders/destroy"
```

### Running RQ
To start RQ, run `python watchman/worker.py` in your Watchman folder. RQ handles
all the post requests made to the server endpoint.

License
--------

    Copyright 2016 Skcript.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
