# Flake8 Boolean Trap

A flake8 plugin to detect boolean traps.

## Setup

### prerequisites

* python>=3.7
* flake8 >=4

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
