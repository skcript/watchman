# Watchman
A Watchdog that pings file changes to an API of your choice.

* [Dependencies](#dependencies)
* [Compiling & Configuring](#compiling-configuring)
* [Default YAML config](#default-yaml-config)
* [Running RQ](#running-rq)
* [Logs](#logs)
* [License](#license)

### Dependencies
* Python 2.7 (Developed and Tested)
* Redis
* [RQ](http://python-rq.org)

### Compiling & Configuring
1. Clone this Repo
2. python setup.py install
3. Configure the app by running `watchman configure`. Use the [Default YAML](#default-yaml-config).

### Running Watchman
1. From Terminal, run `watchman sync`
2. From another Terminal, run `watchman worker` (Starts the RQ worker for Watchman)

### Functions
* `watchman sync`: Watches over all paths added to `source` in watchman.yml

### Default YAML config
This YAML is automatically created in the `~` directory. 
```
  source:
    - /home/users/skcript
  regexes:
    - "([a-zA-Z0-9_ -/]*)/home/(\\w+)/uploads/"
  endpoints:
    file_create: "http://localhost/api/v2/files/create"
    folder_create: "http://localhost/api/v2/folders/create"
    file_move: "http://localhost/api/v2/files/move"
    folder_move: "http://localhost/api/v2/folders/move"
    file_destroy: "http://localhost/api/v2/files/destroy"
    folder_destroy: "http://localhost/api/v2/folders/destroy"
```

### Logs
All Watchman logs are maintained at `/tmp/watchman.log`

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
