def round_robin(processes, time_quantum):
    gantt_chart = []  # Stores the Gantt chart with process IDs and their times
    remaining_processes = [p for p in processes]  # Copy of processes to manage them during the scheduling
    current_time = 0  # Start time of scheduling

    # Initialize turnaround and waiting times
    turnaround_times = [0] * len(processes)
    waiting_times = [0] * len(processes)
    
    # Track finish time for each process
    finish_times = [-1] * len(processes)
    
    # While there are processes left to execute
    while remaining_processes:
        for process in remaining_processes[:]:
            if process.remaining_time > 0:
                # If a process needs to run, execute it
                run_time = min(process.remaining_time, time_quantum)
                start_time = current_time
                end_time = current_time + run_time
                
                # Add process to Gantt chart
                gantt_chart.append((process.pid, start_time, end_time))
                
                # Update the current time
                current_time = end_time
                
                # Subtract the run time from the remaining time
                process.remaining_time -= run_time
                
                # If process has finished, record finish time
                if process.remaining_time == 0:
                    finish_times[process.pid - 1] = end_time
                    remaining_processes.remove(process)
                
    # Calculate turnaround and waiting times
    for i, process in enumerate(processes):
        turnaround_times[i] = finish_times[i] - process.arrival_time
        waiting_times[i] = turnaround_times[i] - process.burst_time

    # Debugging print statements
    print("\nRound Robin Scheduling Results (Time Quantum = {})".format(time_quantum))
    print("Gantt Chart:", gantt_chart)
    print("Turnaround Times:", turnaround_times)
    print("Waiting Times:", waiting_times)
    
    return gantt_chart, turnaround_times, waiting_times
