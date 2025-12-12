FROM ghcr.io/goauthentik/server:2025.10.2

USER root

ENV PATH="/ak-root/.venv/bin:$PATH"

RUN python3 -m ensurepip


# Patch in our app
COPY buildpatch.py /buildpatch.py
COPY overrides /overrides
RUN python3 /buildpatch.py

USER authentik