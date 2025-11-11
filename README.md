# boids

Boids is a set of parametrized behaviors in swarm robotics, simulating and producing behavior comparable to what is seen in flocks of birds.

The rule for boids are as follows:

* Separation - turn away from the location of local neighbors
* Alignment - turn towards the average heading of local neighbors
* Cohesion - turn towards the average location of local neighbors

As you can see, the rules for boids are fairly straightforward, but can produce incredible emergent behavior:

![](/readme/example.gif)

## To Do
* Show update rate
    * time swarm update loop iteration
    * time websocket delay
    * time canvas delay
* vertical/horizonal toolbar based on window size
* attractors
* olfaction 
* leadership/control
