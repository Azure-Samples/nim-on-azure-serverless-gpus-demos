# NIM on Azure Serverless GPU Demos

[![Open in GitHub Codespaces](https://img.shields.io/static/v1?style=for-the-badge&label=GitHub+Codespaces&message=Open&color=brightgreen&logo=github)](https://codespaces.new/Azure-Samples/python-ai-agent-frameworks-demos)
[![Open in Dev Containers](https://img.shields.io/static/v1?style=for-the-badge&label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/Azure-Samples/python-ai-agent-frameworks-demos)


## Purpose

This repository demonstrates how to use the **OpenAI and OpenAI Agents Python frameworks** with NIM models running on Azure Serverless GPUs. The examples show how to integrate these frameworks with NIM endpoints, enabling scalable, cost-effective, and high-performance AI workloads on Azure.

Currently, only the OpenAI and OpenAI Agents examples are fully working and maintained in this repository.

## Getting Started

You can run these examples in GitHub Codespaces, VS Code Dev Containers, or locally. The fastest way to get started is with GitHub Codespaces, which sets up everything for you.

See the sections below for setup instructions.


## Running the Python Examples

Each script in the `examples` directory demonstrates a different agent pattern using OpenAI or OpenAI Agents, all designed to work with NIM models on Azure Serverless GPUs.

### Working Examples

| Example Script | Description |
|---------------|------------|
| `openai_agents_basic.py` | Basic usage of OpenAI Agents with a NIM endpoint. |
| `openai_agents_handoffs.py` | Demonstrates agent handoff between multiple OpenAI Agents using NIM. |
| `openai_agents_mcp_github.py` | Shows how to use OpenAI Agents with MCP GitHub integration and NIM. |
| `openai_agents_mcp_http.py` | Uses OpenAI Agents with MCP HTTP tools and NIM endpoint. |
| `openai_agents_tools.py` | Builds a weekend planner agent with tools using OpenAI Agents and NIM. |
| `openai_functioncalling.py` | Demonstrates OpenAI function calling with NIM endpoint. |
| `openai_reasoning.py` | Example of reasoning and tool use with OpenAI Agents and NIM. |
| `openai_responses.py` | Shows response handling with OpenAI Agents and NIM. |

## Using NIM Models on Azure Serverless GPUs

All examples are designed to connect to NIM model endpoints provisioned on Azure Serverless GPUs. This enables you to leverage powerful, scalable AI models with minimal infrastructure management.

To provision NIM models on Azure and obtain endpoint details, see the [Provisioning Azure AI resources](#provisioning-azure-ai-resources) section.

## Configuring Your Environment

You can run the scripts using GitHub Models for free, or connect to your own NIM endpoints on Azure. For Azure, set the appropriate environment variables with your endpoint and credentials.

See the setup instructions in the sections below for details.

## Provisioning Azure AI Resources

This project includes infrastructure as code (IaC) to provision NIM model deployments on Azure Serverless GPUs. Use the Azure Developer CLI to deploy resources and obtain endpoint details for your agents.

See the [Provisioning Azure AI resources](#provisioning-azure-ai-resources) section for step-by-step instructions.


## Resources

* [NIM on Azure Documentation](https://learn.microsoft.com/en-us/azure/ai-services/nim/)
* [OpenAI Agents Documentation](https://openai.github.io/openai-agents-python/)
* [OpenAI Python API Documentation](https://platform.openai.com/docs/guides/python)
* [Provisioning NIM on Azure Serverless GPUs](https://learn.microsoft.com/azure/container-apps/serverless-gpu-nim?tabs=bash)

---

For full setup, usage, and example details, see the sections below in this README.
