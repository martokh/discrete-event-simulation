import simpy
import random
import matplotlib.pyplot as plt

def student(env, name, cafeteria, arrival_time, wait_times):
    # Student kommt an
    with cafeteria.request() as req:
        yield req  # warten, bis Kasse frei
        start_service = env.now
        waiting_time = start_service - arrival_time
        wait_times.append(waiting_time)
        
        # Bedienzeit 1..3 min
        service_time = random.uniform(1.0, 3.0)
        yield env.timeout(service_time)

def arrival_generator(env, cafeteria, wait_times):
    # 11:00 - 12:00 (t=0..60) => Rate 0.5
    while env.now < 60:
        inter_arrival = random.expovariate(0.5)
        yield env.timeout(inter_arrival)
        if env.now < 60:
            env.process(student(env, f"Student_Early_{env.now:.1f}",
                                cafeteria, env.now, wait_times))
    
    # 12:00 - 13:00 (t=60..120) => Rate 1.4
    while env.now < 120:
        inter_arrival = random.expovariate(1.4)
        yield env.timeout(inter_arrival)
        if env.now < 120:
            env.process(student(env, f"Student_Peak_{env.now:.1f}",
                                cafeteria, env.now, wait_times))
    
    # 13:00 - 14:00 (t=120..180) => Rate 0.333
    while env.now < 180:
        inter_arrival = random.expovariate(0.333)
        yield env.timeout(inter_arrival)
        if env.now < 180:
            env.process(student(env, f"Student_Late_{env.now:.1f}",
                                cafeteria, env.now, wait_times))

def run_sim(capacity, seed=42):
    random.seed(seed)
    env = simpy.Environment()
    wait_times = []
    cafeteria = simpy.Resource(env, capacity=capacity)
    env.process(arrival_generator(env, cafeteria, wait_times))
    env.run(until=180)
    return wait_times


# Szenario A (2 Kassen)
wait_times_2 = run_sim(capacity=2, seed=42)    
# Szenario B (3 Kassen)
wait_times_3 = run_sim(capacity=3, seed=42)    
# Statistische Auswertung
if wait_times_2:
    avg_wait_2 = sum(wait_times_2) / len(wait_times_2)
    max_wait_2 = max(wait_times_2)
else:
    avg_wait_2, max_wait_2 = 0, 0
    
if wait_times_3:
    avg_wait_3 = sum(wait_times_3) / len(wait_times_3)
    max_wait_3 = max(wait_times_3)
else:
    avg_wait_3, max_wait_3 = 0, 0
    
print("=== Szenario mit 2 Kassen ===")
print(f"Durchschnittliche Wartezeit: {avg_wait_2:.2f} min")
print(f"Maximale Wartezeit:         {max_wait_2:.2f} min")  
print("\n=== Szenario mit 3 Kassen ===")
print(f"Durchschnittliche Wartezeit: {avg_wait_3:.2f} min")
print(f"Maximale Wartezeit:         {max_wait_3:.2f} min")
    
# Beide Histogramme nebeneinander
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,4))
# Linkes Histogramm: 2 Kassen
ax1.hist(wait_times_2, bins=20, edgecolor='black')
ax1.set_title("Wartezeiten mit 2 Kassen")
ax1.set_xlabel("Wartezeit [min]")
ax1.set_ylabel("Häufigkeit")
ax1.grid(True, alpha=0.3)
# Rechtes Histogramm: 3 Kassen
ax2.hist(wait_times_3, bins=20, edgecolor='black', color='orange')
ax2.set_title("Wartezeiten mit 3 Kassen")
ax2.set_xlabel("Wartezeit [min]")
ax2.set_ylabel("Häufigkeit")
ax2.grid(True, alpha=0.3)   
plt.tight_layout()
plt.show()