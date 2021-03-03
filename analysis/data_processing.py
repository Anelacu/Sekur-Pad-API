import requests


def fetch():
    url = "https://sekurpad-api.herokuapp.com/api/logs"
    res = requests.get(url)
    return res.json()['data']


def group_by_user(d):
    data = {}
    for el in d:
        uuid = el['userUuid']
        element_body = [el['activity'], el['timestamp']]
        if uuid in data.keys():
            data[uuid].append(element_body)
        else:
            data[uuid] = [element_body]

    return data


def filter_out_uncompleted(data):
    filtered = {}
    required = []
    for i in range(1, 13):
        required.append(f"Start stage: {i}")
        required.append(f"Correct pin entered at stage: {i}")
    for uuid, logs in data.items():
        activities = [el[0] for el in logs]
        ok = True
        for r in required:
            if r not in activities:
                ok = False

        if ok:
            filtered[uuid] = logs

    return filtered


def get_completion_times(data):
    times = {}
    for i in range(1, 13):
        times[i] = []
        start = f"Start stage: {i}"
        correct = f"Correct pin entered at stage: {i}"
        for uuid, logs in data.items():
            s = None
            c = None
            for el in logs:
                if el[0] == start:
                    s = int(el[1])
                elif el[0] == correct:
                    c = int(el[1])
            if s is None or c is None:
                print(
                    f"User {uuid} does not have start or correct pin on stage {i}")
            else:
                times[i].append(c - s)

    return times


def get_errors_per_stage(data):
    errors = {}
    for i in range(1, 13):
        errors[i] = []
        msg = f"Wrong pin entered at stage: {i}"
        for uuid, logs in data.items():
            n = 0
            for el in logs:
                if el[0].startswith(msg):
                    n += 1
            errors[i].append(n)

    return errors


d = filter_out_uncompleted(group_by_user(fetch()))
print(get_completion_times(d))
print(get_errors_per_stage(d))
