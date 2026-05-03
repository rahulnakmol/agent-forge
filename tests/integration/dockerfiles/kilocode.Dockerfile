FROM python:3.12-slim
RUN apt-get update && apt-get install -y curl git && apt-get clean
# Kilocode uses ~/.claude/skills/ convention (same as Claude Code)
COPY . /agent-forge
WORKDIR /agent-forge
RUN pip install -e scripts/agent_forge
CMD ["bash"]
