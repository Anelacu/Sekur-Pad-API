import requests
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


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
                times[i].append((c - s)/1000)

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


def plot_errors_per_stage_all(errors_per_stage_data: dict) -> None:
    colors = ['lime', 'gold', 'orangered'] * 4
    means = []
    stages = []
    for stage, errors in errors_per_stage_data.items():
        stages.append(stage)
        means.append(np.mean(errors))

    x = np.array(stages)
    width = 0.35
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, means, width, color=colors, alpha=0.5)

    plt.legend()
    plt.xlabel("Stage")
    plt.xticks(np.array(stages))
    plt.ylabel("Number of errors")
    plt.title("Mean number of errors at each stage")
    plt.savefig('plots/errors_per_stage_all.png')
    plt.clf()


def plot_completion_times_all(completion_times: dict) -> None:
    means = []
    medians = []
    stages = []
    for stage, times in completion_times.items():
        stages.append(stage)
        means.append(np.mean(times))
        medians.append(np.median(times))

    x = np.array(stages)
    width = 0.35
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, means, width, label='Mean', color='coral')
    rects2 = ax.bar(x + width/2, medians, width,
                    label='Median', color='royalblue')

    plt.legend()
    plt.xlabel("Stage")
    plt.xticks(np.array(stages))
    plt.ylabel("Completion time (s)")
    plt.title("Mean vs Median completion time for each stage")
    plt.savefig('plots/completion_time_all.png')
    plt.clf()


def plot_completion_times_scatter(completion_times: dict) -> None:
    y = []
    x = []
    stages = []
    for stage, times in completion_times.items():
        stages.append(stage)
        for t in times:
            x.append(stage)
            y.append(t)

    plt.scatter(x, y, marker='x', alpha=0.5, s=30, c='coral')
    plt.xlabel("Stage")
    plt.xticks(np.array(stages))
    plt.ylabel("Completion time (s)")
    plt.title("Completion time for each stage")
    plt.savefig('plots/completion_time_scatter.png')
    plt.clf()


def plot_completion_box(completion_times: dict) -> None:
    colors = ['lime', 'gold', 'orangered'] * 4

    df = pd.DataFrame.from_dict(completion_times)
    data_df = df.melt(var_name='stage', value_name='time')
    sns.boxplot(x="stage", y="time", data=data_df, linewidth=0.9,
                palette=colors, showfliers=False, boxprops=dict(alpha=0.5))
    sns.stripplot(x="stage", y="time", data=data_df, color='royalblue',
                  size=6, jitter=False, alpha=0.5, marker='X')
    plt.xlabel("Stage")
    plt.xticks(range(0, 12))
    plt.ylabel("Completion time (s)")
    plt.title("Completion time for each stage")
    plt.savefig('plots/completion_time_box_scatter.png')
    plt.clf()


def plot_completion_sorted_box(completion_times):
    cols = []
    for i in range(3):
        stages = [i+1+j*3 for j in range(4)]
        cols.extend(stages)

    df = pd.DataFrame.from_dict(completion_times)
    data_df = df.melt(var_name='stage', value_name='time')

    colors = ['lime'] * 4 + ['gold'] * 4 + ['orangered'] * 4

    sns.boxplot(x="stage", y="time", data=data_df, linewidth=0.9, order=cols,
                palette=colors, showfliers=False, boxprops=dict(alpha=0.5))
    sns.stripplot(x="stage", y="time", data=data_df, color='royalblue', order=cols,
                  size=6, jitter=False, alpha=0.5, marker='X')
    plt.xlabel("Stage")
    plt.xticks(range(0, 12))
    plt.ylabel("Completion time (s)")
    plt.title("Completion time for each stage (sorted)")
    plt.savefig('plots/completion_time_sorted_box_scatter.png')
    plt.clf()


d = filter_out_uncompleted(group_by_user(fetch()))
errors_per_stage = get_errors_per_stage(d)
completion_times = get_completion_times(d)
print("No. of participants:", len(d.keys()))

# Temp data
#errors_per_stage = {i: np.random.normal(3, 1, 40) * ((i-1)%3 + 0.2) for i in range(1, 13)}
#completion_times = {i: np.random.normal(10000, 3000, 40) * ((i-1)%3 * 0.1 + 0.2) for i in range(1, 13)}

plot_errors_per_stage_all(errors_per_stage)
plot_completion_times_all(completion_times)
plot_completion_times_scatter(completion_times)
plot_completion_box(completion_times)
plot_completion_sorted_box(completion_times)
