FROM python:3.6

ENV TZ GMT-7:00
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ADD . / denton/
ENV PYTHONPATH /denton/

RUN pip install -r denton/requirements.txt
ENTRYPOINT ["python", "denton/run_reports.py"]
CMD []
#to run just docker run DOCKER_IMAGE --monthly, --weekly, --daily, --test
