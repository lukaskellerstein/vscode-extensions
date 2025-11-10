# Luke Editor VSCode Extension

Custom editor for `.luke` files with drawing capabilities.

## Features

- Custom editor for `.luke` files
- Draw circles, rectangles, and text on a canvas
- Interactive webview-based canvas
- Save/load drawings as JSON
- Integrates with MCP server for AI agent control

## Setup

```bash
cd extension
npm install
npm run compile
```

## Development

```bash
npm run watch
```

Then press F5 in VSCode to launch the extension development host.

## Usage

1. Create a new file with `.luke` extension
2. The custom editor will open automatically
3. Use the toolbar to select tools (circle, rectangle, text)
4. Click on the canvas to draw
5. The file will be saved as JSON with all element data

## Architecture

The extension provides:
- **Custom Editor Provider** for `.luke` files
- **Drawing API** that interfaces with the MCP server
- **Webview-based Canvas** for interactive drawing
- **JSON-based file format** for storing drawings

The MCP server can control the editor programmatically through the Drawing API.

## File Format

`.luke` files are JSON documents with this structure:

```json
{
  "elements": [
    {
      "id": "elem_1",
      "x": 100,
      "y": 100,
      "radius": 50,
      "color": "#FF0000"
    },
    {
      "id": "elem_2",
      "x": 200,
      "y": 200,
      "width": 100,
      "height": 60,
      "color": "#0000FF"
    }
  ]
}
```
