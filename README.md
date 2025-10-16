# NIM on Azure Serverless GPU Demos

[![Open in GitHub Codespaces](https://img.shields.io/static/v1?style=for-the-badge&label=GitHub+Codespaces&message=Open&color=brightgreen&logo=github)](https://codespaces.new/Azure-Samples/nim-on-azure-serverless-gpus-demos)
[![Open in Dev Containers](https://img.shields.io/static/v1?style=for-the-badge&label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/Azure-Samples/nim-on-azure-serverless-gpus-demos)

This repository demonstrates how to work with NIM models running on Azure Serverless GPUs. The examples show how to integrate popular Python AI agent frameworks with NIM endpoints, enabling scalable, cost-effective, and high-performance AI workloads on Azure.

* [Getting started](#getting-started)
  * [GitHub Codespaces](#github-codespaces)
  * [VS Code Dev Containers](#vs-code-dev-containers)
  * [Local environment](#local-environment)
* [Provisioning NIM Models on Azure Serverless GPUs](#provisioning-nim-models-on-azure-serverless-gpus)
* [Running the Python examples](#running-the-python-examples)

## Getting started

You have a few options for getting started with this repository.
The quickest way to get started is GitHub Codespaces, since it will setup everything for you, but you can also [set it up locally](#local-environment).

### GitHub Codespaces

You can run this repository virtually by using GitHub Codespaces. The button will open a web-based VS Code instance in your browser:

1. Open the repository (this may take several minutes):

    [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Azure-Samples/nim-on-azure-serverless-gpus-demos)

2. Open a terminal window
3. Continue with the steps to run the examples

### VS Code Dev Containers

A related option is VS Code Dev Containers, which will open the project in your local VS Code using the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers):

1. Start Docker Desktop (install it if not already installed)
2. Open the project:

    [![Open in Dev Containers](https://img.shields.io/static/v1?style=for-the-badge&label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/Azure-Samples/nim-on-azure-serverless-gpus-demos)

3. In the VS Code window that opens, once the project files show up (this may take several minutes), open a terminal window.
4. Continue with the steps to run the examples

### Local environment

1. Make sure the following tools are installed:

    * [Python 3.10+](https://www.python.org/downloads/)
    * Git

2. Clone the repository:

    ```shell
    git clone https://github.com/Azure-Samples/nim-on-azure-serverless-gpus-demos.git
    cd nim-on-azure-serverless-gpus-demos
    ```

3. Set up a virtual environment:

    ```shell
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

4. Install the requirements:

    ```shell
    pip install -r requirements.txt
    ```

## Provisioning NIM Models on Azure Serverless GPUs

All examples are designed to connect to NIM model endpoints provisioned on Azure Serverless GPUs. This enables you to leverage powerful, scalable AI models with minimal infrastructure management.

To provision NIM models on Azure and obtain endpoint details, follow this tutorial, but replace the model name with `gpt-oss-20b`, since that is the model verified to work with these examples:

[Provisioning NIM on Azure Serverless GPUs](https://learn.microsoft.com/azure/container-apps/serverless-gpu-nim?tabs=bash)

## Configuring Your Environment

Create a `.env` file by copying the provided `.env.sample`, then fill in the required variables:

```
NIM_ENDPOINT=https://ENDPOINT.azurecontainerapps.io/v1/
NIM_MODEL=
```

## Running the Python Examples

Each script in the `examples` directory demonstrates a different agent pattern, all designed to work with NIM models on Azure Serverless GPUs.

### OpenAI

These examples use NIM with the [openai package](https://pypi.org/project/openai/).

| Example Script | Description |
|----------------|-------------|
| `openai_responses.py` | Calls model using the Responses API. |
| `openai_reasoning.py` | Calls model with reasoning effort and displays reasoning tokens. |
| `openai_functioncalling.py` | Calls model with function calling and single function definition. |
| `openai_functioncalling_loop.py` | Calls model with multiple function calling definitions, and executes calls in a loop until complete. |

### Agent Framework

These examples use NIM with the [Agent Framework Python package](https://learn.microsoft.com/agent-framework/).

| Example Script | Description |
|-----------------------------|---------------------------------------------------------------|
| `agentframework_tool.py`     | Demonstrates a single-tool agent using Agent Framework and NIM. |
| `agentframework_tools.py`    | Weekend planner agent with multiple tools using Agent Framework and NIM. |
| `agentframework_supervisor.py` | Supervisor agent orchestrating sub-agents with Agent Framework and NIM. |
| `agentframework_mcp_http.py` | Demonstrates using agent with a local MCP HTTP server. Requires running the MCP server (`mcp_server_basic.py`) locally. |

### OpenAI Agents

These examples use NIM with the [OpenAI Agents package](https://openai.github.io/openai-agents-python/).

| Example Script | Description |
|---------------|------------|
| `openai_agents_basic.py` | Calls agent with no tools. |
| `openai_agents_tools.py` | Builds a weekend planner agent with tools. |
| `openai_agents_mcp_http.py` | Builds a hotel booking agent using a local HTTP MCP server. |
| `openai_agents_mcp_github.py` | Builds an issue triaging agent using the GitHub MCP server. |
