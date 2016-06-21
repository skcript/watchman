# Watchman
Ping file system events to any API

* [Dependencies](#dependencies)
* [Installing](#installing)
* [Running Watchman](#running-watchman)
* [Functions](#functions)
* [YAML Configuration](#yaml-configuration)
* [Extending](#extending)
* [Running Watchman as a Service](#running-watchman-as-a-service)
* [Logs](#logs)
* [License](#license)

## Dependencies
* Python 2.7 (Developed and Tested)
* [Redis](http://redis.io/)
* [RQ](http://python-rq.org)

## Installing
1. Download this Repo
2. Run `python setup.py install`
3. Configure the app by running `watchman configure`. Or copy the [default YAML file](#yaml-config) to `~`.

## Running Watchman
1. From Terminal, run `watchman sync`
2. From another Terminal, run `watchman worker`

## Functions
* `watchman sync`: Watches over all paths added to `source` in [YAML configuration file](#yaml-config)
* `watchman worker`: Starts the RQ worker to ping all endpoints added to `endpoints` in [YAML configuration file](#yaml-config)

## YAML Configuration
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

## Extending
Watchman can ratelimit and selectively prevent your API calls for each file
system event. These are managed in `watchman/extension.py`. Each function defined
in `extension.py` takes path (where the file system event occurred) as input.

### Ratelimiting
Watchman can ratelimit your API calls based on a unique string at 100 calls
per second.

The unique string is used to group your API calls. Modify the `ratelimit()`
function in `watchman/extension.py` to enable this. By default it returns the
root directory of the path Watchman is watching.

For example, if you are monitoring `/uploads` folder which has directories for
each user, like,
- `/uploads/user1`
- `/uploads/user2`
- `/uploads/user3`

Modify `ratelimit()` to return the username from the path. This way you can
ratelimit API calls based on each user.

### Preventing
Watchman can selectively prevent API calls from being triggered by simply
returning a boolean for each path. Modify the `prevent()` function in
`watchman/extension.py` to enable this.

By default `prevent()` returns `False` and does not prevent any API calls.

## Running Watchman as a Service
Watchman can be run as a service in your production environments. Currently,
only Linux environments are supported.

1. Download `watchman_sync` and `watchman_worker` to your in `/etc/init.d` folder
2. Create folder `/var/run/watchman` to store pids file
3. Create a `/tmp` if it is not present already
4. Give appropriate permissions to `/var/run/watchman` and `/tmp` (to whichever user Watchman is running from)

**To start the service**
```
  service watchman_sync start
  service watchman_worker start
```

**To stop the service**
```
  service watchman_sync stop
  service watchman_worker stop
```

**To restart the service**
```
  service watchman_sync restart
  service watchman_worker restart
```

## Logs
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
