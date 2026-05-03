FROM python:3.12-slim
RUN apt-get update && apt-get install -y curl git && apt-get clean
# Cursor is a desktop app; CI testing uses the cursor-rules directory convention
COPY . /agent-forge
WORKDIR /agent-forge
RUN pip install -e scripts/agent_forge
CMD ["bash"]
