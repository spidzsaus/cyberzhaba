FROM python:3.12.7

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg

WORKDIR /bot_dir

COPY . /bot_dir

RUN pip install --no-cache-dir --upgrade -r /bot_dir/requirements.txt
CMD ["python3", "main.py"]