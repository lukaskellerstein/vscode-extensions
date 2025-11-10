# lukas-extension-3

VSCode extension with React-based UI in a side panel.

## Features

- Custom side panel with React UI
- Interactive components (buttons, inputs, text areas, color picker)
- Uses VSCode theme variables for consistent styling
- Webpack bundled for optimal performance

## Development

### Setup

```bash
npm install
```

### Build

```bash
npm run compile
```

### Watch Mode

```bash
npm run watch
```

### Run Extension

Press F5 in VSCode to launch the Extension Development Host.

## Structure

- `src/extension.ts` - Extension activation and registration
- `src/SidePanelProvider.ts` - Webview provider for the side panel
- `src/webview/` - React application for the webview
  - `index.tsx` - React app entry point
  - `App.tsx` - Main React component
  - `App.css` - Styles using VSCode theme variables
- `webpack.config.js` - Webpack configuration for bundling extension and React app
