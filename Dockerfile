
FROM python:3.8

COPY . /var/app

WORKDIR /var/app

RUN pip3 install -r requirements.txt

CMD streamlit run fipe/streamlit_main_page.py