FROM python:3.12-slim
RUN apt-get update && apt-get install -y curl git && apt-get clean
RUN curl -fsSL https://opencode.ai/install.sh | sh || true
COPY . /agent-forge
WORKDIR /agent-forge
RUN pip install -e scripts/agent_forge
CMD ["bash"]
