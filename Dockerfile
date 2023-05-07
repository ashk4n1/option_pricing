FROM ubuntu:20.04

RUN apt-get update && apt-get -y update

RUN apt-get install -y build-essential python3.6 python3-pip python3-dev

RUN pip3 -q install pip --upgrade

RUN mkdir src

COPY . /src

WORKDIR src/

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "--server.port", "8501", "dashboard_options.py"]

