<h1 align="center">European Options Pricing </h1>

# Introduction

This repository represents a web app for calculating European Options prices, including the computation and the visualization of the Option Greeks.

The model has various parameters that user should adjust:

1. Type of option (Call or put)  
2. Spot price  
3. Strike  
4. Volatility  
5. Expiry date  
6. Risk-free rate  


# Files
- `Requirements.txt` : package requirements files
- `option_price.py`: python file containing the main formulas
- `dashboard_options.py`: streamlit app file
- `Dockerfile` for docker deployment

#  Running Demo
## Run Demo Locally 

### Shell
It is recommended that you create a new virtual environment (either venv or conda).  
You can directly run streamlit locally in the repo as follows:

```shell
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r Requirements.txt
$ streamlit run dashboard_options.py
```
Open http://localhost:8501 to view the demo

### Docker

Dockerfile has exposed 8501, so when you deploy it to some cloud provider, you access the recently deployed web app through browser.
Build and run the docker image named `st-demo`:

```
$ docker build -t st-option .
$ docker run -it --rm st-option
```

`-it` keeps the terminal interactive

`--rm` removes the image once the command is stopped.

Visit http://localhost:8501/ to view the app.
