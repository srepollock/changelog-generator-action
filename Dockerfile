FROM python:3
COPY changelog_generator.py /changelog_generator.py
CMD ["python", "/changelog_generator.py"]
