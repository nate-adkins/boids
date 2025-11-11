# boids

Boids (bird-oids) are a swarm of agents that follow a set of parametrized rules, simulating behavior observed in groups of organisms, including birds.

The fundamental rules for boids are as follows:

- **Separation** - turn away from surrounding local neighbors
- **Alignment** - turn towards the average heading of local neighbors
- **Cohesion** - turn towards the average location of local neighbors

These fundamental rules are applied amongst local neighbors in the swarm, defined either by a distance threshold or by an agent's k-nearest neighbors. Weights are applied to each rule's effect, allowing for modulation of the strength of each individual rule. Each agent in the swarm follows the net effect of the rules.

In this particular simulation, rules are applied using an agent's k-nearest neighbors and each rule produces a heading delta, weighted by the rule's parameter. The weighted heading deltas are then summed to produce the net heading delta. Each agent maintains constant linear speed in the simulation, changing only their heading.

The rules for boids are simple, but produce incredible emergent behavior:

<p align="center">
  <img src="/readme/example.gif" />
</p>

## To Do
* Show update rate
    * time swarm update loop iteration
    * time websocket delay
    * time canvas delay
* vertical/horizonal toolbar based on window size
* attractors
* olfaction 
* leadership/control
