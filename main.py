from priority import priority_non_preemptive, priority_preemptive
from round_robin import round_robin
from sjn import shortest_job_next

def display_gantt_chart(gantt_chart):
    if not gantt_chart:
        return

    # Get unique time points
    time_points = []
    for _, start, end in gantt_chart:
        if start not in time_points:
            time_points.append(start)
        if end not in time_points and end is not None:
            time_points.append(end)
    time_points.sort()
    
    # Fixed width for each segment
    segment_width = 7
    
    # Draw top border
    print("\nGantt Chart:")
    print("+" + ("-" * segment_width + "+") * len(gantt_chart))
    
    # Draw process names
    print("|", end=' ')
    for pid, _, _ in gantt_chart:
        label = " Idle" if isinstance(pid, str) and pid == 'Idle' else f" P{pid}"
        print(f"{label.center(segment_width)}|", end=' ')
    print()
    
    # Draw bottom border
    print("+" + ("-" * segment_width + "+") * len(gantt_chart))
    
    # Print time points
    if len(time_points) > 0:
        total_width = (segment_width + 1) * len(gantt_chart) + 1
        if len(time_points) == 1:
            print(time_points[0])
            return
            
        spacing = (total_width - 1) // (len(time_points) - 1)
        timeline = [" "] * total_width
        
        # Place first number
        first_num = str(time_points[0])
        for i, digit in enumerate(first_num):
            timeline[i] = digit
            
        # Place middle numbers
        for i in range(1, len(time_points) - 1):
            pos = i * spacing
            num = str(time_points[i])
            for j, digit in enumerate(num):
                if pos + j < total_width:
                    timeline[pos + j] = digit
        
        # Place last number
        last_num = str(time_points[-1])
        last_pos = total_width - len(last_num)
        for i, digit in enumerate(last_num):
            timeline[last_pos + i] = digit
        
        print("".join(timeline))


class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        # Only used by round_robin
        self.remaining_time = burst_time

def get_valid_input(prompt, min_val=None, max_val=None):
    while True:
        try:
            value = int(input(prompt))
            if min_val is not None and value < min_val:
                print(f"Please enter a number greater than or equal to {min_val}.")
                continue
            if max_val is not None and value > max_val:
                print(f"Please enter a number less than or equal to {max_val}.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")

def main():
    # Available scheduling algorithms
    algorithms = {
        1: (priority_non_preemptive, "Priority Non-Preemptive"),
        2: (priority_preemptive, "Priority Preemptive"),
        3: (lambda p: round_robin(p, 3), "Round Robin Scheduling (Time Quantum = 3)"),
        4: (shortest_job_next, "Shortest Job Next (SJN)")
    }

    # Get process details
    num_processes = get_valid_input("Enter the number of processes (3 to 10): ", 3, 10)
    processes = []
    
    for i in range(num_processes):
        print(f"\nEnter details for Process {i + 1}:")
        arrival_time = get_valid_input("  Arrival Time (>= 0): ", 0)
        burst_time = get_valid_input("  Burst Time (> 0): ", 1)
        priority = get_valid_input("  Priority (>= 0, lower number = higher priority): ", 0)
        processes.append(Process(i + 1, arrival_time, burst_time, priority))

    # Select and execute algorithm
    print("\nSelect Scheduling Algorithm:")
    for i, (_, name) in enumerate(algorithms.values(), 1):
        print(f"{i}. {name.split('(')[0].strip()}")
    
    choice = get_valid_input("Enter your choice (1-4): ", 1, 4)
    algorithm_func, algorithm_name = algorithms[choice]
    gantt_chart, turnaround_times, waiting_times = algorithm_func(processes)

    # Display results
    print(f"\nResults for {algorithm_name}:")
    print(f"{'Process':<10}{'Turnaround Time':<20}{'Waiting Time':<15}")
    for i, p in enumerate(processes):
        print(f"P{p.pid:<9}{turnaround_times[i]:<20}{waiting_times[i]:<15}")

    # Calculate and display averages
    avg_turnaround = sum(turnaround_times) / len(turnaround_times)
    avg_waiting = sum(waiting_times) / len(waiting_times)
    print(f"\nAverage Turnaround Time: {avg_turnaround:.2f}")
    print(f"Average Waiting Time: {avg_waiting:.2f}")

    display_gantt_chart(gantt_chart)

if __name__ == "__main__":
    main()
