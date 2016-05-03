# Watchman
A Watchdog that pings file changes to endpoints of your choice.

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
