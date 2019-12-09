# animaloptics
#### Project structure outline of important things
    .
    ├── figs
    │   └── figures we made and code to generate them
    ├── data
    │   └── currently just formatted acuity data from the source below for various species and many birds.
    ├── simulator
    |   ├── Simulator.py # functional for twitter bot will make it easier if we add to this project more
    |   ├── dog.py # takes an image returns an image of dog vision simulation
    │   └── translations.py # various helper functions for acuity translations and other stuff
    ├── twitterbot                
    │   └── everything twitter bot related
    └── README.md
    
### Steps
1. Cone catch modeling
2. Acuity control
3. Brightness discrimination

# Things that would improve this
* Cameras arent consistent and since raw images are the ideal data to be working with we could create a linearization model by first taking an image of a known color pallete.[2]

## Sources
* [1] https://dog-vision.andraspeter.com/
* [2] http://www.empiricalimaging.com/  (data/code - https://github.com/troscianko/micaToolbox)
## Data

### List of common animal spatial acuities
http://www.empiricalimaging.com/knowledge-base/list-of-animal-spatial-acuities/

A poster we made overviewing the project can be found <a href="figs/455 final poster.pdf">here.</a>
