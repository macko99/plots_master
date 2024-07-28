import matplotlib.pyplot as plt
import numpy as np
import data


for iter in [400, 10]:
    plt.rcParams.update({'font.size': 16.5})
    fig, ax = plt.subplots()

    time_data = {runtime: data.time_data[runtime] for runtime in data.time_data}

    time_data = {runtime: time_data[runtime] for runtime in sorted(time_data, key=lambda x: time_data[x][iter])}


    times = [time_data[runtime][iter] for runtime in time_data]

    runtimes = list(time_data.keys())
    width = 0.4

    colors = ['#2d85f0' if runtime != "crun+wamr" else "#ed755c" for runtime in runtimes]
    alpha = [1 if "python" not in runtime else 0.5 for runtime in runtimes]

    for i, runtime in enumerate(runtimes):
        if 'wamr' not in runtime:
            if time_data[runtime][iter] != 0:
                print(iter, ': wamr uses', time_data["crun+wamr"][iter], 's, while', runtime, 'uses', time_data[runtime][iter], 's')
                print(iter, ': wamr uses', round((1 - time_data["crun+wamr"][iter] / time_data[runtime][iter]) * 100, 2), '% less time than', runtime)
            print('__________________________________________________________')

    for i, runtime in enumerate(runtimes):
        if 'containerd-shim-wasmedge' not in runtime:
            if time_data[runtime][iter] != 0:
                print(iter, ': containerd-shim-wasmedge uses', time_data["containerd-shim-wasmedge"][iter], 's, while', runtime, 'uses', time_data[runtime][iter], 's')
                print(iter, ': containerd-shim-wasmedge uses', round((1 - time_data["containerd-shim-wasmedge"][iter] / time_data[runtime][iter]) * 100, 2), '% less time than', runtime)
            print('__________________________________________________________')

    for i, runtime in enumerate(runtimes):
        if 'crun+wasmtime' not in runtime:
            if time_data[runtime][iter] != 0:
                print(iter, ': wasmtime uses', time_data["crun+wasmtime"][iter], 's, while', runtime, 'uses', time_data[runtime][iter], 's')
                print(iter, ': wasmtime uses', round((1 - time_data["crun+wasmtime"][iter] / time_data[runtime][iter]) * 100, 2), '% less time than', runtime)
            print('__________________________________________________________')

    avg = sum(times) / len(times)
    print('avg time for', iter, 'pods:', avg, 's')

    y = np.arange(len(runtimes))
    for i, runtime in enumerate(runtimes):
        ax.barh(runtime, times[i], color=colors[i], label='kubectl top', alpha=alpha[i])


    ax.set_xlabel('Time to Start All Containers (s)')
    ax.set_title('Startup Time: crun + WAMR vs Current Sate-of-Art (' + str(iter) + ' pods)')

    fig.set_size_inches(13.5, 6)
    plt.tight_layout()
    plt.savefig('plot11_crun_' + str(iter) + '.png')
