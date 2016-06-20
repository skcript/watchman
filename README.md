# Watchman
A Watchdog that pings file changes to an API of your choice.

* [Dependencies](#dependencies)
* [Compiling & Configuring](#compiling--configuring)
* [Running Watchman](#running-watchman)
* [Functions](#functions)
* [YAML Configuration](#yaml-config)
* [Logs](#logs)
* [License](#license)

### Dependencies
* Python 2.7 (Developed and Tested)
* [Redis](http://redis.io/)
* [RQ](http://python-rq.org)

### Compiling & Configuring
1. Clone this Repo
2. Run `python setup.py install`
3. Configure the app by running `watchman configure`. Or copy the [default YAML file](#yaml-config) to `~`.

### Running Watchman
1. From Terminal, run `watchman sync`
2. From another Terminal, run `watchman worker`

### Functions
* `watchman sync`: Watches over all paths added to `source` in [YAML configuration file](#yaml-config)
* `watchman worker`: Starts the RQ worker to ping all endpoints added to `endpoints` in [YAML configuration file](#yaml-config)

### YAML configuration
This YAML is automatically created in the `~` directory. It holds all the configuration attributes for Watchman.

#### Attributes
* `source`: Array of all paths Watchman should monitor
* `regexes`: Array of all regexes Watchman should abide by (These regexes are matched with the filepath)
* `endpoints`: Hash of each file/folder action which should ping to an API endpoint

#### Default File
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

About
-----

![Skcript](http://www.skcript.com/static/skcript_norm.png)

Watchman is maintained and funded by Skcript. The names and logos for
Skcript are properties of Skcript.

We love open source, and we have been doing quite a bit of contributions to the community. Take a look at them [here][skcriptoss]. Also, encourage people around us to get involved in community [operations][community]. [Join us][hiring], if you'd like to see the world change from our HQ.

[skcriptoss]: http://skcript.github.io/
[community]: http://www.skcript.com/community?utm_source=github
[hiring]: http://www.skcript.com/careers?utm_source=github
