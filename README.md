# PID train delay notifications

This Python script checks the current position data from the Golemio API for a
chosen PID line and sends its delay to an [ntfy](https://ntfy.sh/) topic. It
performs one check each time it runs; to monitor a line regularly, schedule it
to run at the interval you want.

## Requirements

- Python 3
- A Golemio API access token
- The Golemio `routeId` for the route you want to check
- An ntfy topic (the endpoint where notifications will be published)

Install the Python dependency:

```powershell
py -m pip install requests
```

On systems where the Python launcher is not `py`, use
`python -m pip install requests` instead.

## Configure the line and notification

Open `main.py` and replace the placeholders in the final call and request:

1. Replace `"YOUR API KEY FOR GOLEMIO"` with your Golemio access token.
2. Replace `"YOUR ROUTE ID DEPENDENT ON THE LINE YOU NEED TO TRACK"` with the
   Golemio `routeId` for the route.
3. Replace `"YOUR_DESIGNED_ENDPOINT"` in the ntfy URL with your topic name.
   For example, `https://ntfy.sh/my-private-topic`.
4. Replace `"YOUR LINE"` in `check_train_delay("YOUR LINE")` with the line's
   `trip_short_name` as it appears in the Golemio response.

The route ID and line name are separate values: the route ID selects data from
the API, and the line name is matched against the returned trips. Make sure
they correspond to the same route.

Treat the Golemio token as a secret and do not commit it to a public
repository. ntfy topics are accessible to anyone who knows the topic URL unless
you configure access control; choose a topic name accordingly.

## Run a check

From the repository directory, run:

```powershell
py main.py
```

The script sends one notification containing the line and delay in minutes.
If the line is not found, or its delay is unavailable, the notification
contains `not found` for that value. Delay is converted from seconds to whole
minutes.

## Run it automatically

Schedule `main.py` with your operating system's task scheduler. For example, in
Windows Task Scheduler, create a task with:

- **Program/script:** the path to `python.exe` (find it with
  `py -c "import sys; print(sys.executable)"`)
- **Add arguments:** the full path to `main.py`
- **Start in:** the repository directory
- **Trigger:** the desired recurring interval

Save the task and use **Run** to check that it sends a notification. Keep the
computer awake and connected to the internet at the scheduled time. Each run
performs a fresh API request and sends a notification; set the interval to
avoid sending more updates than you need.

Or you can create a GitHub Actions workflow with `schedule.yaml` which sample is available in this repo too. Just keep in mind that it has to be in the folder `/.github/workflows` in order to work.
