import React, { useState } from 'react';

declare const acquireVsCodeApi: any;
const vscode = acquireVsCodeApi();

const App: React.FC = () => {
  const [textInput, setTextInput] = useState('');
  const [textArea, setTextArea] = useState('');

  const handleButtonClick = () => {
    vscode.postMessage({
      type: 'buttonClicked'
    });
  };

  const handleColorClick = (color: string) => {
    vscode.postMessage({
      type: 'colorSelected',
      value: color
    });
  };

  const colors = [
    '#e74c3c',
    '#3498db',
    '#2ecc71',
    '#f39c12',
    '#9b59b6',
    '#1abc9c'
  ];

  return (
    <div className="container">
      <div className="section">
        <h2>Welcome</h2>
        <p>This is a custom side panel with React for lukas-extension-3.</p>
        <div className="info">You can add any React components here.</div>
      </div>

      <div className="section">
        <h2>Quick Actions</h2>
        <button className="action-button" onClick={handleButtonClick}>
          Click Me
        </button>
      </div>

      <div className="section">
        <h2>Input Example</h2>
        <label className="label">Enter some text:</label>
        <input
          type="text"
          className="text-input"
          placeholder="Type something..."
          value={textInput}
          onChange={(e) => setTextInput(e.target.value)}
        />
      </div>

      <div className="section">
        <h2>Text Area Example</h2>
        <label className="label">Enter multiple lines:</label>
        <textarea
          className="text-area"
          placeholder="Enter multiple lines here..."
          value={textArea}
          onChange={(e) => setTextArea(e.target.value)}
        />
      </div>

      <div className="section">
        <h2>Color Picker</h2>
        <label className="label">Select a color:</label>
        <div className="color-picker">
          {colors.map((color) => (
            <div
              key={color}
              className="color-box"
              style={{ backgroundColor: color }}
              onClick={() => handleColorClick(color)}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default App;
