FROM python:3.12-slim
RUN apt-get update && apt-get install -y curl git nodejs npm && apt-get clean
RUN npm install -g @anthropic-ai/claude-code || true
COPY . /agent-forge
WORKDIR /agent-forge
RUN pip install -e scripts/agent_forge
CMD ["bash"]
