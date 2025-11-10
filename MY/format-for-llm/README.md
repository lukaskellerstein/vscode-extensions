# Prerequisite

Install VSCE packaging tool

```bash
npm install -g vsce
```

# Build

Increase version in package.json

```bash
vsce package
```

# Install in VSCode

Open VSCode, then:

1. Press Ctrl+Shift+P (or Cmd+Shift+P on macOS)

2. Type: Extensions: Install from VSIX...

3. Select your .vsix file
