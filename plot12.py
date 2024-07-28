import matplotlib.pyplot as plt
import numpy as np
import data


if True:
    plt.rcParams.update({'font.size': 16.5})
    fig, ax = plt.subplots()

    memory_kubectl = data.memory_data['kubectl']
    memory_os = data.memory_data['os']

    memory_kubectl = {runtime: [sum(memory_kubectl[runtime][i] for i in [10, 100, 400]) / sum(1 if memory_kubectl[runtime][i] != 0 else 0 for i in [10, 100, 400])] for runtime in
                       memory_kubectl}
    memory_os = {runtime: [sum(memory_os[runtime][i] for i in [10, 100, 400]) / sum(1 if memory_os[runtime][i] != 0 else 0 for i in [10, 100, 400])] for runtime in memory_os}


    memory_os = {runtime: memory_os[runtime] for runtime in sorted(memory_os, key=lambda x: memory_os[x])}
    memory_kubectl = {runtime: memory_kubectl[runtime] for runtime in memory_os}


    memory = [memory_kubectl[runtime] for runtime in memory_kubectl]
    memory_os = [memory_os[runtime] for runtime in memory_os]

    runtimes = list(memory_kubectl.keys())
    width = 0.4

    y = np.arange(len(runtimes))

    alpha = [1 if "python" not in runtime else 0.5 for runtime in runtimes]

    for i, runtime in enumerate(runtimes):
        if 'wamr' not in runtime:
            print('kubectl: wamr uses', memory[0][0], 'MB of memory, while', runtime, 'uses', memory[i][0], 'MB of memory')
            print('kubectl: wamr uses ', round((1 - memory[0][0] / memory[i][0]) * 100, 2), '% less memory than', runtime)
            print('OS: wamr uses', memory_os[0], 'MB of memory, while', runtime, 'uses', memory_os[i], 'MB of memory')
            print('OS: wamr uses ', round((1 - memory_os[0][0] / memory_os[i][0]) * 100, 2), '% less memory than', runtime)
            print('__________________________________________________________')


    for i, runtime in enumerate(runtimes):
        alpha_value = alpha[i]
        ax.barh(y[i] + width / 2, memory_os[i], width*0.95, color='#ed755c', label='free command' if i == 0 else "", alpha=alpha_value)
        ax.barh(y[i] - width / 2, memory[i], width*0.95, color='#2d85f0', label='kubectl top' if i == 0 else "", alpha=alpha_value)

    ax.set_yticks(y)
    ytick_labels = ax.set_yticklabels(runtimes)

    for ytick_label in ytick_labels:
        if 'wamr' in ytick_label.get_text():
            ytick_label.set_color('green')

    ax.legend(title='Metrics source:')

    ax.set_xlabel('Average Memory Used per Pod (MB)')
    ax.set_ylabel('Runtime Configuration Used')
    ax.set_title('Memory Usage: crun + WAMR vs Current Sate-of-Art')

    fig.set_size_inches(13.5, 6)
    plt.tight_layout()
    plt.savefig('plot12_crun_avg.png')
