[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md)

<div style="display: flex; align-items: center;">
   <div style="flex: 1;">
    <!-- Image -->
    <img src="https://github.com/MetaphoraStudios/mochi-code/assets/178898/441777f2-1670-4f7b-81a4-690f6056a1b3"
       alt="Mochi Coder" width="200" align="left">
  </div>
  <div style="flex: 1;">
    <!-- Text content -->
    <h1>Mochi-Code 👋</h1>

    > An assistant for coding tasks.

   The project is in the early stages of development and is intended for
    educational purposes only.
  </div>
</div>

<br/>

## Current State

![CleanShot 2023-07-11 at 21 37 33](https://github.com/MetaphoraStudios/mochi-code/assets/178898/b613cf9d-4ff8-44a6-abc2-1492e3664f15)

## Wishlist 🧞‍♂️

- Learn the details of a new project faster 📚
- Stay up-to-date with changes to your repo 🔔
- Jump to the right place in the codebase 🔦
- Chat with your codebase (including dependencies) 💬

## Getting Started 🚀

### Prerequisites 📋

- Python 3.8 or higher
- macOS _(happy to support other platforms, but haven't tested yet)_

## Installation 🔧

For now you have to run Mochi from source.
Mochi uses OpenAI's APIs (for now) and before you start you need to set up your
OpenAI API key. Create a file called `.keys` in the root of the project:

```bash
OPENAI_API_KEY="sk-your-key-here"
```

Mochi-Code should be published to PyPI soon, but for now you can install it from
source.

### Install whl file

From `mochi-code` root directory:

```bash
poetry build
```

The command above creates a whl file in the dist directory which you can install
with pip in a project you'd like to use Mochi in:

```bash
pip install dist/mochi_code-0.1.0-py3-none-any.whl # version my diverge!
```

### Install as an editable package

Alternatively, you can install as an editable package:

```bash
pip install -e path/to/mochi-code
```

## Usage 💻

For now I'm going to use Mochi directly from this repo's `poetry` setup, but you
can use it from anywhere once it's installed.

You can ask Mochi any coding questions straight away:

```bash
poetry run mochi ask "How do I install retry?"

# real output, although each run will be different
> "Answer: You can install Retry using your package manager. For example, if
   you're using npm, you can run this command in your terminal: `npm install
   retry`%"
```

But you will notice this likely doesn't match quite what you're looking for.
That's because Mochi needs to learn about your project first.  
You can do this by initializing Mochi in your project root:

```bash
poetry run mochi init
```

Running the same command again should give you a better result:

```bash
poetry run mochi ask "How do I install retry?"

# real output, although each run will be different
> "Answer: You can install retry easily with poetry. Use the command \"poetry
   add retry2\" in your project directory and it will be installed in your
   virtual environment.%"
```

Spot on! 🎯

**Note: Soon, just running `mochi` will start the interactive chat interface.**

## Roadmap 🗺

_Semi-prioritised order_

- Chat mode (similar to `ask` command but goes on forever)
- Access to the actual code
- Access to git history
- Access to the documentation for all dependencies
- Support for other models (e.g. Claude2)
- (Researchy) Local fine-tuned (open-sourced) models

## Contributing 🤝

We welcome contributions from anyone.
Whether you're a seasoned developer or a beginner, your help is always welcome.

Here's how you can contribute:

### Reporting Bugs 🐛

If you find a bug, open an issue in the
[issue tracker](https://github.com/MetaphoraStudios/mochi-code/issues).

### Proposing Features 💡

Have an idea for a new feature? Feel free to open an issue describing your
feature, how it would be used, and why you think it would be a great addition to
Mochi.

### Code Contributions 🖥

If you'd like to contribute code, please follow these steps:

1. Fork the repository.
2. Create a new branch for your features / fixes (e.g.
   `git checkout -b feature/YourFeatureName`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push the changes to the branch (`git push origin feature/YourFeatureName`).
5. Create a new Pull Request.

Before contributing, please read our
[Contributing Guide](https://github.com/MetaphoraStudios/mochi-code/blob/main/CONTRIBUTING.md)
and
[Code of Conduct](https://github.com/MetaphoraStudios/mochi-code/blob/main/CODE_OF_CONDUCT.md).

## License 📝

This project is licensed under the MIT License - see the
[LICENSE.md](https://github.com/MetaphoraStudios/mochi-code/blob/main/LICENSE.md)
file for details.

## Contact 📧

Join the discussion at [Discord](https://discord.gg/kyy5ncWsMa).

## Acknowledgements 🙏

Coming soon...
ChatGPT, Bard and Mochi for helping generate sections of this README.
