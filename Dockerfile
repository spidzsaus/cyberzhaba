FROM python:latest

WORKDIR /bot_dir

COPY . /bot_dir

RUN pip install --no-cache-dir --upgrade -r /bot_dir/requirements.txt
CMD ["python3", "main.py"]