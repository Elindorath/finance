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
    - Neural network
      - Class that derive a neural network from a given genome

Visualizer
  - Neural network
  - Candle chart with orders



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



Buy at 50
Drop to 25
