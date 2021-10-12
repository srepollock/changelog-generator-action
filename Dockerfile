FROM python:3
RUN apt get update \
  && apt get install
RUN apt install -y git
COPY changelog_generator.py /changelog_generator.py
RUN pip install PyGithub['integrations']
CMD ["python", "/changelog_generator.py"]
