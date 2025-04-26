# priority.py

def priority_non_preemptive(processes):
    n = len(processes)
    # Only sort by arrival time initially
    processes.sort(key=lambda x: x.arrival_time)

    completed = 0
    current_time = 0
    is_completed = [False] * n
    waiting_times = [0] * n
    turnaround_times = [0] * n
    gantt_chart = []
    last_completion_time = 0

    while completed != n:
        idx = -1
        highest_priority = float('inf')
        earliest_arrival = float('inf')
        
        # Find process with highest priority among arrived processes
        for i in range(n):
            if processes[i].arrival_time <= current_time and not is_completed[i]:
                if processes[i].priority < highest_priority:
                    highest_priority = processes[i].priority
                    earliest_arrival = processes[i].arrival_time
                    idx = i
                elif processes[i].priority == highest_priority:
                    # If same priority, choose the one that arrived first
                    if processes[i].arrival_time < earliest_arrival:
                        earliest_arrival = processes[i].arrival_time
                        idx = i
        
        if idx != -1:
            # Add idle time to Gantt chart if there's a gap
            if current_time > last_completion_time:
                gantt_chart.append(('Idle', last_completion_time, current_time))

            start_time = current_time
            current_time += processes[idx].burst_time
            completion_time = current_time
            last_completion_time = completion_time

            # Update waiting and turnaround times
            turnaround_times[idx] = completion_time - processes[idx].arrival_time
            waiting_times[idx] = turnaround_times[idx] - processes[idx].burst_time

            # Mark as completed
            is_completed[idx] = True
            completed += 1

            # Add to Gantt chart
            gantt_chart.append((processes[idx].pid, start_time, completion_time))
        else:
            # If no process is available, move to the next arrival time
            next_arrival = float('inf')
            for i in range(n):
                if not is_completed[i] and processes[i].arrival_time > current_time:
                    next_arrival = min(next_arrival, processes[i].arrival_time)
            
            if next_arrival != float('inf'):
                # Add idle time to Gantt chart
                if current_time > last_completion_time:
                    gantt_chart.append(('Idle', last_completion_time, next_arrival))
                current_time = next_arrival
            else:
                current_time += 1

    return gantt_chart, turnaround_times, waiting_times

def priority_preemptive(processes):
    n = len(processes)
    processes.sort(key=lambda x: x.arrival_time)

    remaining_times = [p.burst_time for p in processes]
    completion_times = [-1] * n
    is_completed = [False] * n
    current_time = 0
    completed = 0
    gantt_chart = []
    waiting_times = [0] * n
    turnaround_times = [0] * n
    last_process = -1
    execution_start = [-1] * n

    while completed != n:
        idx = -1
        highest_priority = float('inf')
        
        # Find process with highest priority among arrived processes
        for i in range(n):
            if processes[i].arrival_time <= current_time and not is_completed[i] and remaining_times[i] > 0:
                if processes[i].priority < highest_priority:
                    highest_priority = processes[i].priority
                    idx = i
                elif processes[i].priority == highest_priority and processes[i].arrival_time < processes[idx].arrival_time:
                    idx = i

        if idx != -1:
            # Track execution start for waiting time calculation
            if execution_start[idx] == -1:
                execution_start[idx] = current_time

            # Update Gantt chart only when switching processes
            if last_process != idx:
                if len(gantt_chart) > 0:
                    gantt_chart[-1] = (gantt_chart[-1][0], gantt_chart[-1][1], current_time)
                gantt_chart.append((processes[idx].pid, current_time, None))
                last_process = idx

            remaining_times[idx] -= 1
            current_time += 1

            if remaining_times[idx] == 0:
                is_completed[idx] = True
                completed += 1
                completion_times[idx] = current_time
                
                # Calculate turnaround and waiting times
                turnaround_times[idx] = current_time - processes[idx].arrival_time
                total_execution_time = processes[idx].burst_time
                waiting_times[idx] = turnaround_times[idx] - total_execution_time
                
                # Update last Gantt chart entry
                gantt_chart[-1] = (gantt_chart[-1][0], gantt_chart[-1][1], current_time)
                last_process = -1  # Reset last process as current one is completed
        else:
            # Add idle time to Gantt chart
            if len(gantt_chart) == 0 or gantt_chart[-1][0] != 'Idle':
                gantt_chart.append(('Idle', current_time, None))
            current_time += 1
            if len(gantt_chart) > 0 and gantt_chart[-1][0] == 'Idle':
                gantt_chart[-1] = ('Idle', gantt_chart[-1][1], current_time)
            last_process = -1

    return gantt_chart, turnaround_times, waiting_times
