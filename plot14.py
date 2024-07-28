import matplotlib.pyplot as plt
import numpy as np
import data


for iter in ['kubectl', 'os']:
    plt.rcParams.update({'font.size': 15.5})
    fig, ax = plt.subplots()

    memory = data.memory_data[iter]

    memory = {runtime: memory[runtime] for runtime in memory if 'crun' in runtime and 'python' not in runtime}



    memory = {runtime: memory[runtime] for runtime in sorted(memory, key=lambda x: memory[x][10])}

    memory_400 = [memory[runtime][400] for runtime in memory]
    memory_100 = [memory[runtime][100] for runtime in memory]
    memory_10 = [memory[runtime][10] for runtime in memory]

    print(iter)
    for i, runtime in enumerate(memory):
        if 'wamr' not in runtime:
            print('400: wamr uses', memory["crun+wamr"][400], 'MB of memory, while', runtime, 'uses', memory[runtime][400], 'MB of memory')
            print('400: wamr uses', round((1 - memory["crun+wamr"][400] / memory[runtime][400]) * 100, 2), '% less memory than', runtime)
            print('100: wamr uses', memory["crun+wamr"][100], 'MB of memory, while', runtime, 'uses', memory[runtime][100], 'MB of memory')
            print('100: wamr uses', round((1 - memory["crun+wamr"][100] / memory[runtime][100]) * 100, 2), '% less memory than', runtime)
            print('10: wamr uses', memory["crun+wamr"][10], 'MB of memory, while', runtime, 'uses', memory[runtime][10], 'MB of memory')
            print('10: wamr uses', round((1 - memory["crun+wamr"][10] / memory[runtime][10]) * 100, 2), '% less memory than', runtime)
            print('__________________________________________________________')

    runtimes = list(memory.keys())
    width = 0.2

    x = np.arange(len(runtimes))

    ax.bar(x - width, memory_10, width=width * 0.95, color='#2d85f0', label='10 pods')
    ax.bar(x, memory_100, width=width * 0.95, color='#ed755c', label='100 pods')
    ax.bar(x + width, memory_400, width=width * 0.95, color='#27a145', label='400 pods')


    ax.set_xticks(x)
    xtick_labels = ax.set_xticklabels(runtimes)

    for xtick_label in xtick_labels:
        if 'wamr' in xtick_label.get_text():
            xtick_label.set_color('red')

    ax.legend(title='Deployment Size:')

    ax.set_ylabel('Memory Used per Pod (MB)')
    ax.set_xlabel('Runtime Configuration Used')
    name = 'kubectl top' if iter == 'kubectl' else 'free command'
    ax.set_title('Memory Usage in crun: WAMR vs WasmEdge, Wasmer, Wasmtime (' + str(name) + ')')

    fig.set_size_inches(13.5, 6)
    plt.tight_layout()
    plt.savefig('plot14_crun_' + str(iter) + '.png')
