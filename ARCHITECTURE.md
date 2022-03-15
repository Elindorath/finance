ARCHITECTURE
------------

Simulation
  Classes:
    - World feeder
      - Takes an url or a file to get a market timeserie
      - Enhances the timeserie with indicators (RSI, MACD, ...)
    - World
      - Class that represents the market as a timeserie
      - Its main goal is to iterate over the timeserie and the population
      - For each actor, it feeds the current data to it
    - Population
      - Class that represents the collection of all living actors
    - Actor
      - Class that represents a trading actor
      - It contains a genome that is a 16 bits representation of its neural network
      - Its main goal is to determine a potential action by feeding the received data to its neural network
    - Genome
      - Class that represents a genome as a 16 bits string
    - Gene
      - Class that represents a unique gene
      - A gene describe a weighted connection between a transmitter neuron and a receptor neuron
    - Neural network
      - Class that derive a neural network from a given genome
    - Sensor neurone
      - Should produce an output between 0.0 and 1.0
    - Internal neurone
      - Should sum all of its inputs and output the hyperbolic tangent ot the sum
    - Action neurone
      - Should sum all of its inputs and output the hyperbolic tangent ot the sum
      - The resulting output (range between -1.0 and 1.0) should be interpreted as a probability of action during simulation
    - Connection
      - Should multiply the input by a range between -4.0 and 4.0

Visualizer
  - Neural network
  - Candle chart with orders

Multi processing
As the program is basically 3 imbricated loops, we can speed it up by spreading loops across multiple processes:
  - First loop : Generations are dependant of the previous one, so they only can be processed in linear order
  - Second loop: World is immutable during the whole process, making it a good candidate to be shared between processes
  - Third loop : Actors are immutable during a generation

We see that second and third loops order is interchangeable

We then could distribute calculation either:
  - Actors living in the entire world. This means that:
    - Each process is responsible for one actor
    - Each process needs to receive the world data
    - Each process needs to receive the given actor data (its genome essentialy)
    - Each process needs to return back the given actor trading history
  - World slice fed to all actors
    - Each process is responsible for one time slice
    - Each process needs to receive the time slice data (one row of the world's dataframe)
    - Each process needs to receive all of the actors data
    - Each process needs to return back the trading probability of each actors

To circumvent the overhead of process management, we need to ensure "enough work" is provided to each processes
  - For actors, it's the world size that matter. For a world of 2329 entries, it takes around 300ms
  - For world slices, it's the actor count that matter

There are two ways to pass data between processes:
  - Shared ctypes objects (Value, Array, ...)
  - Shared_memory module

===============

If not holding
  When buy signal
    Buy

If holding
  When sell signal
    Sell

Sensors:
  Bought price
  RSI
  MA
  MACD
  StochasticRSI
  Bandes de Bollinger



Actions:
  Spot:
    Buy
    Sell
    Responsiveness



Buy at 50
Drop to 25
