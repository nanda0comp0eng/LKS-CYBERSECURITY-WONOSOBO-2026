FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install flask
RUN echo "LKSWNSB{4dm!n_T0_SSTI_S0_EZZZ}" > /flag.txt
EXPOSE 5000
CMD ["python", "app.py"]