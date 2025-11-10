# Module 5: Language Features

**Duration**: Week 5 | **Difficulty**: Advanced

Implement advanced language support including Language Server Protocol, semantic highlighting, and navigation features.

## 📖 Learning Objectives

- Configure language basics
- Understand and implement Language Server Protocol
- Add semantic highlighting
- Implement go-to-definition and find-references
- Create rename providers
- Add document symbols and outline
- Implement workspace symbols

## 📚 Lessons

### [5.1 Language Configuration](./5.1-language-config.md)
- Language contribution
- Syntax highlighting with TextMate grammars
- Bracket matching
- Auto-closing pairs
- Comment toggling
- Indentation rules
- Folding markers
- Word patterns

### [5.2 Language Server Protocol (LSP)](./5.2-language-server.md)
- Introduction to LSP
- LSP architecture
- Setting up language client
- Setting up language server
- Server initialization
- Text document synchronization
- Implementing language features
- Debugging language servers
- Multi-root workspace support

### [5.3 Semantic Highlighting](./5.3-semantic-highlighting.md)
- Semantic tokens provider
- Token types and modifiers
- Legend configuration
- Dynamic semantic highlighting
- Performance optimization
- Incremental updates

### [5.4 Advanced Language Features](./5.4-advanced-features.md)
- Go to definition
- Find all references
- Document symbols
- Workspace symbols
- Rename provider
- Document link provider
- Call hierarchy
- Type hierarchy

## 💻 Examples

1. **language-basics** - Language configuration
2. **simple-lsp** - Minimal language server
3. **semantic-tokens** - Semantic highlighting
4. **definition-provider** - Go-to-definition
5. **references-provider** - Find references
6. **rename-provider** - Symbol renaming
7. **symbols-provider** - Document outline
8. **workspace-symbols** - Project-wide symbols

## ✏️ Exercises

1. **Simple Language** - Create basic language support
2. **DSL Parser** - Domain-specific language with LSP
3. **Enhanced Navigation** - Implement all navigation features
4. **Refactoring Support** - Add rename and refactoring
5. **Symbol Index** - Build workspace symbol index

## 🎯 Mini Project: Custom Language Support

**Features**:
- Complete syntax highlighting
- Language server with validation
- Semantic highlighting
- Go-to-definition and references
- Symbol outline
- Rename refactoring

**Time**: 8-10 hours

## ⏭️ Next Steps

[Module 6: Workspace Management](../module-06-workspace-management/README.md)
