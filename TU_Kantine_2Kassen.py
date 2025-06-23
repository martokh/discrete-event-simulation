import simpy
import random
import matplotlib.pyplot as plt

wait_times = [] 

def student(env, name, cafeteria, arrival_time):
    print(f"{name} kommt an bei t={arrival_time:.1f} min")
    
    with cafeteria.request() as req:
        yield req 
        
        start_service = env.now
        waiting_time = start_service - arrival_time
        wait_times.append(waiting_time)
        
        # Bedienung: z.B. zwischen 1 und 3 Minuten
        service_time = random.uniform(1.0, 3.0)
        yield env.timeout(service_time)
        
        finish_time = env.now
        print(f"{name} beendet Bedienung bei t={finish_time:.1f} min (Wartezeit={waiting_time:.1f})")

def arrival_generator(env, cafeteria):
    # Phase 1: 11:00 - 12:00 (niedrige Rate => z.B. ~1 Student alle 2 min => rate=0.5)
    while env.now < 60:
        inter_arrival = random.expovariate(0.5)
        yield env.timeout(inter_arrival)  # Zeit schreitet voran
        if env.now < 60:  
            env.process(student(env, f"Student_Early_{env.now:.1f}", cafeteria, env.now))
    
    # Phase 2: 12:00 - 13:00 (starker Andrang => z.B. ~1 Student/0.7 min => rate=1.4)
    while env.now < 120:
        inter_arrival = random.expovariate(1.4)
        yield env.timeout(inter_arrival)
        if env.now < 120:
            env.process(student(env, f"Student_Peak_{env.now:.1f}", cafeteria, env.now))
    
    # Phase 3: 13:00 - 14:00 (abnehmende Rate => z.B. ~1 Student alle 3 min => rate=0.333)
    while env.now < 180:
        inter_arrival = random.expovariate(0.333)
        yield env.timeout(inter_arrival)
        if env.now < 180:
            env.process(student(env, f"Student_Late_{env.now:.1f}", cafeteria, env.now))


random.seed(42)
env = simpy.Environment()
    
# Zwei Kassen => Ressource mit Kapazität=2
cafeteria = simpy.Resource(env, capacity=2)
env.process(arrival_generator(env, cafeteria))
    
# Simulation für 3 Stunden (11:00 - 14:00 => 180 Minuten)
env.run(until=180)
    
# Auswertung der Wartezeiten (Histogramm)
plt.figure(figsize=(8,5))
plt.hist(wait_times, bins=20, edgecolor='black')
plt.title("Verteilung der Wartezeiten (in Minuten)")
plt.xlabel("Wartezeit [min]")
plt.ylabel("Häufigkeit (Anzahl)")
plt.grid(True, alpha=0.3)
plt.show()
    
if wait_times:
    avg_wait = sum(wait_times)/len(wait_times)
    max_wait = max(wait_times)
    print(f"Durchschnittliche Wartezeit: {avg_wait:.2f} min")
    print(f"Maximale Wartezeit:         {max_wait:.2f} min")
else:
    print("Keine Studenten bedient.")

