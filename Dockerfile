FROM python

WORKDIR ocp-addons-operators-cli
COPY . .
RUN python3 -m pip install pip --upgrade \
    && python3 -m pip install poetry \
    && poetry config cache-dir /cnv-tests \
    && poetry config virtualenvs.in-project true \
    && poetry config --list \
    && poetry env remove --all \
    && poetry install \
    && poetry export --without-hashes -n

ENTRYPOINT ["poetry", "run", "python", "app/cli.py"]
