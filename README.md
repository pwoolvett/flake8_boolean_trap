# Flake8 Boolean Trap

A flake8 plugin to detect boolean traps.

docs available at [readthedocs](https://flake8-boolean-trap.readthedocs.io/en/latest/)

“The Boolean Trap” is a programming anti-pattern where a boolean argument switches behaviour, leading to confusion. 

To learn more about the impact it can have on your code and how to prevent it, you can refer to the following resources:
- [What is a boolean trap? (YouTube video)](https://www.youtube.com/watch?v=CnRkXO_a5mI)
- [Python Type Hints - How to Avoid “The Boolean Trap” (article)](https://adamj.eu/tech/2021/07/10/python-type-hints-how-to-avoid-the-boolean-trap/)


## Setup

### prerequisites

* python>=3.8


### install

```console
$ pip install flake8_boolean_trap
```

## Usage

Just run `flake8` as you normally would.

## Lint Codes

| Code.  | Description                                   |
| ------ | --------------------------------------------- |
| FBT001 | Boolean positional arg in function definition |
| FBT002 | Boolean default value in function definition  |
| FBT003 | Boolean positional value in function call     |
