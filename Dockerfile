FROM python:3
COPY changelog_generator.py /changelog_generator.py
RUN pip install -y PyGithub['integrations']
CMD ["python", "/changelog_generator.py"]
