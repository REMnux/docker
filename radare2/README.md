This Docker image encapsulates the [Radare2](http://radare.org/) reverse-engineering framework.

To run this image after installing Docker, use a command like this, replacing "~/workdir" with the path to your working directory on the underlying host:

    docker run --rm -it --cap-drop=ALL --cap-add=SYS_PTRACE -v ~/workdir:/home/nonroot/workdir remnux/radare2

Then run `r2` or other Radare2 commands inside the container. Before running the application, create ~/workdir on your host.

## r2ai and decai

The image includes [r2ai](https://github.com/radareorg/r2ai), a native plugin that adds LLM-powered analysis to Radare2 (function analysis, vulnerability detection, auto variable naming), and its companion decai decompiler integration plugin. Both are pre-installed via `r2pm`.

r2ai requires an LLM backend to function, such as a cloud API (OpenAI, Anthropic, etc.) or a local model server (Ollama). Pass your API key when launching the container:

    docker run --rm -it -e OPENAI_API_KEY=your-key -v ~/workdir:/home/nonroot/workdir remnux/radare2

Inside `r2`, configure the provider and model before use. The default provider is Ollama; to use a cloud API instead:

    r2ai -p openai
    r2ai -m gpt-4

Use `r2ai -h` and `decai -h` to see available commands. Use `r2ai -p?` to list providers and `r2ai -e` to view all settings.
