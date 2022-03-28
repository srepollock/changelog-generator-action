FROM python:3

COPY changelog_generator.py /changelog_generator.py
RUN pip install PyGithub['integrations']

ENTRYPOINT [ "python", "/changelog_generator.py" ]
