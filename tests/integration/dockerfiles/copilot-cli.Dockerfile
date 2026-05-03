FROM python:3.12-slim
RUN apt-get update && apt-get install -y curl git && apt-get clean
# GitHub Copilot CLI: gh extension install github/gh-copilot
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null && \
    apt-get update && apt-get install -y gh && apt-get clean && \
    gh extension install github/gh-copilot || true
COPY . /agent-forge
WORKDIR /agent-forge
RUN pip install -e scripts/agent_forge
CMD ["bash"]
