# sjn.py

def shortest_job_next(processes):
    n = len(processes)
    is_completed = [False] * n
    current_time = 0
    completed = 0
    gantt_chart = []
    waiting_times = [0] * n
    turnaround_times = [0] * n

    while completed != n:
        idx = -1
        min_burst = float('inf')
        for i in range(n):
            if (processes[i].arrival_time <= current_time) and not is_completed[i]:
                if processes[i].burst_time < min_burst:
                    min_burst = processes[i].burst_time
                    idx = i
                elif processes[i].burst_time == min_burst:
                    # Assumption: If burst time same, choose FCFS
                    if processes[i].arrival_time < processes[idx].arrival_time:
                        idx = i

        if idx != -1:
            start_time = current_time
            current_time += processes[idx].burst_time
            completion_time = current_time

            # Update waiting and turnaround times
            turnaround_times[idx] = completion_time - processes[idx].arrival_time
            waiting_times[idx] = turnaround_times[idx] - processes[idx].burst_time

            # Mark as completed
            is_completed[idx] = True
            completed += 1

            # Add to Gantt chart
            gantt_chart.append((processes[idx].pid, start_time, completion_time))
        else:
            current_time += 1  # CPU is idle

    return gantt_chart, turnaround_times, waiting_times
