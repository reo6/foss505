![](https://github.com/ramazanemreosmanoglu/foss505/blob/main/readme_assets/banner-4s-round.gif)

<div align="center">
  <b>Disclaimer:</b> This project is currently at the early development. Expect <a href="https://github.com/ramazanemreosmanoglu/foss505/blob/main/TODO.org#bugs-02">bugs</a>.
</div>

# Installation

I didn't test for operating systems other than linux for now. A running Jack server and -<i>probably</i>- a patchbay (qpwgraph, qjackctl etc.) required.

### Using pipx (Recommended)

```
pipx install foss505
```

pipx will install the program in a clean environment for you. But you can alternatively do the:

### Using pip

```
pip install foss505
```

### Development Setup

Make sure you have <a href="">poetry</a> installed on your system.

```
git clone https://github.com/ramazanemreosmanoglu/foss505
cd foss505/
poetry install
```

Building:

```
poetry build
```

Installing:

```
pip install dist/foss505-X-X-X-py3-none-any.whl
```

# Usage

Running the program:

```
# Assuming that you have $HOME/.local/bin on your PATH.
foss505
```
