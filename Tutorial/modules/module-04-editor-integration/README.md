# Module 4: Editor Integration

**Duration**: Week 4 | **Difficulty**: Intermediate

Work directly with the editor to add decorations, code lenses, and intelligent code assistance.

## 📖 Learning Objectives

- Manipulate text documents and editors
- Add decorations and highlights
- Implement code lenses
- Provide code actions and quick fixes
- Create hover providers
- Build completion providers
- Add signature help

## 📚 Lessons

### [4.1 Text Document and Editor APIs](./4.1-text-document.md)
- TextDocument vs TextEditor
- Reading document content
- Making text edits
- Workspace edits
- Document selections and ranges
- Cursor position and movement
- Document formatting

### [4.2 Decorations and Highlights](./4.2-decorations.md)
- Text decoration types
- Creating decoration types
- Applying decorations
- Gutter decorations
- Overview ruler markers
- Performance considerations
- Dynamic decoration updates

### [4.3 Code Lens and Code Actions](./4.3-codelens-actions.md)
- CodeLensProvider implementation
- Resolving code lenses
- Refreshing code lenses
- Code action providers
- Quick fixes
- Refactorings
- Source actions
- Code action kinds

### [4.4 Hover and Completion Providers](./4.4-hover-completion.md)
- Hover provider
- Markdown in hovers
- Completion item provider
- Completion item kinds
- Snippet completions
- Resolve completion items
- Signature help provider
- Parameter hints

## 💻 Examples

1. **text-manipulation** - Edit operations
2. **decorations-demo** - Various decoration types
3. **codelens-sample** - Code lens implementation
4. **quick-fix** - Code actions provider
5. **hover-docs** - Documentation hovers
6. **completion-basic** - Simple completions
7. **completion-advanced** - Context-aware completions
8. **signature-help** - Function signatures

## ✏️ Exercises

1. **TODO Highlighter** - Highlight TODO comments
2. **Error Lens** - Show errors inline
3. **Reference Counter** - Code lens showing usage
4. **Smart Imports** - Auto-import quick fixes
5. **Context Completion** - Intelligent suggestions

## 🎯 Mini Project: Code Annotator

**Features**:
- Highlight important code patterns
- Code lens for statistics
- Quick fixes for common issues
- Hover documentation
- Smart completions

**Time**: 4-5 hours

## ⏭️ Next Steps

[Module 5: Language Features](../module-05-language-features/README.md)
