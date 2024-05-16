#!/usr/bin/env python
# coding: utf-8

# In[2]:


class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.start_time = 0
        self.finish_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0


def fcfs(processes):
    current_time = 0
    for process in processes:
        if process.arrival_time >= current_time:
            current_time = process.arrival_time
        process.start_time = current_time
        process.finish_time = current_time + process.burst_time
        process.waiting_time = process.start_time - process.arrival_time
        process.turnaround_time = process.finish_time - process.arrival_time
        current_time = process.finish_time



def srt(processes):
    n = len(processes)
    rt = [0] * n

    # Copy the burst time into rt[]
    for i in range(n):
        rt[i] = processes[i].burst_time
    complete = 0
    t = 0
    minm = 999999999
    short = 0
    check = False

    # Process until all processes get
    # completed
    while complete != n:

        # Find process with minimum remaining
        # time among the processes that
        # arrive till the current time
        for j in range(n):
            if processes[j].arrival_time <= t and rt[j] < minm and rt[j] > 0:
                minm = rt[j]
                short = j
                check = True
        if not check:
            t += 1
            continue

        # Reduce remaining time by one
        rt[short] -= 1

        # Update minimum
        minm = rt[short]
        if minm == 0:
            minm = 999999999

        # If a process gets completely
        # executed
        if rt[short] == 0:

            # Increment complete
            complete += 1
            check = False

            # Find finish time of the current
            # process
            fint = t + 1

            # Calculate waiting time
            processes[short].waiting_time = (fint - processes[short].burst_time -
                                             processes[short].arrival_time)

            if processes[short].waiting_time < 0:
                processes[short].waiting_time = 0

            # Calculating turnaround time
            processes[short].turnaround_time = processes[short].burst_time + processes[short].waiting_time
            processes[short].finish_time = fint

        # Increment time
        t += 1



def rr(processes, quantum):
    n = len(processes)
    rem_bt = [0] * n

    # Copy the burst time into rem_bt[]
    for i in range(n):
        rem_bt[i] = processes[i].burst_time
    t = 0  # Current time

    # Keep traversing processes in round
    # robin manner until all of them are
    # not done.
    while True:
        done = True

        # Traverse all processes one by
        # one repeatedly
        for i in range(n):

            # If burst time of a process is greater
            # than 0 then only need to process further
            if rem_bt[i] > 0:
                done = False  # There is a pending process

                if rem_bt[i] > quantum:

                    # Increase the value of t i.e. shows
                    # how much time a process has been processed
                    t += quantum

                    # Decrease the burst_time of current
                    # process by quantum
                    rem_bt[i] -= quantum

                # If burst time is smaller than or equal
                # to quantum. Last cycle for this process
                else:

                    # Increase the value of t i.e. shows
                    # how much time a process has been processed
                    t += rem_bt[i]

                    # Waiting time is current time minus
                    # time used by this process
                    processes[i].waiting_time = t - processes[i].burst_time

                    # As the process gets fully executed
                    # make its remaining burst time = 0
                    rem_bt[i] = 0

        # If all processes are done
        if done == True:
            break

    # Calculating turnaround time
    for i in range(n):
        processes[i].turnaround_time = processes[i].burst_time + processes[i].waiting_time
        processes[i].finish_time = processes[i].arrival_time + processes[i].turnaround_time              
            


def calculate_metrics(processes):
    
    if not processes:  # Check if the list is empty
        return 0, 0, 0
    total_turnaround_time = 0
    total_waiting_time = 0
    total_cpu_burst = 0
    current_time = processes[0].finish_time  # Initialize current_time
    for process in processes:
        total_turnaround_time += process.turnaround_time
        total_waiting_time += process.waiting_time
        total_cpu_burst += process.burst_time
        current_time = max(current_time, process.finish_time)  # Update current_time
    cpu_utilization = (total_cpu_burst / current_time) * 100
    return total_turnaround_time / len(processes), total_waiting_time / len(processes), cpu_utilization




def display_results(processes):
    processes.sort(key=lambda x: x.start_time)
    print("Gantt Chart:")
    for process in processes:
        print("P" + str(process.pid), end=" ")
    print()
    print("Process\t\tFinish Time\tWaiting Time\tTurnaround Time")
    for process in processes:
        print(f"P{process.pid}\t\t{process.finish_time}\t\t{process.waiting_time}\t\t{process.turnaround_time}")
    avg_turnaround_time, avg_waiting_time, cpu_utilization = calculate_metrics(processes)
    print(f"\nAverage Turnaround Time: {avg_turnaround_time}")
    print(f"Average Waiting Time: {avg_waiting_time}")
    print(f"CPU Utilization: {cpu_utilization}%")


def main():
    
    filename = r"C:\Users\S.C.P\Desktop\الجامعة\Third year\Second semester\OS\CPU Scheduler Simulation\proceess.txt"

    processes = []
    with open(filename, "r") as file:
        cs, quantum = map(int, file.readline().split())
        for line in file:
            data = line.strip().split()
            pid, arrival_time, burst_time = map(int, data)
            processes.append(Process(pid, arrival_time, burst_time))

    fcfs_processes = processes.copy()
    srt_processes = processes.copy()
    rr_processes = processes.copy()

    print("\nFCFS Scheduling:")
    fcfs(fcfs_processes)
    display_results(fcfs_processes)

    print("\nSRT Scheduling:")
    srt(srt_processes)
    print("\nGantt Chart:")
    if srt_processes:  # Check if srt_processes is not empty
        display_results(srt_processes)


    print("\nRound-Robin Scheduling:")
    rr(rr_processes, quantum)
    display_results(rr_processes)


if __name__ == "__main__":
    main()




# In[ ]:




