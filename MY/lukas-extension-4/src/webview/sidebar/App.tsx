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

  const handleAddCircle = () => {
    vscode.postMessage({
      type: 'addCircleToEditor'
    });
  };

  return (
    <div className="container">
      <div className="section">
        <h2>Luke Editor Controls</h2>
        <p>Open a .luke file and use the button below to add circles to the editor.</p>
        <div className="info">Circles will be added at random positions.</div>
      </div>

      <div className="section">
        <h2>Editor Actions</h2>
        <button className="action-button" onClick={handleAddCircle}>
          Add Circle to Editor
        </button>
      </div>

      <div className="section">
        <h2>Quick Actions</h2>
        <button className="action-button" onClick={handleButtonClick}>
          Show Message
        </button>
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
