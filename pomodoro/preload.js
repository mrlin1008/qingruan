const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  closeWindow: () => ipcRenderer.send('close-window'),
  minimizeWindow: () => ipcRenderer.send('minimize-window'),
  toggleAlwaysOnTop: () => ipcRenderer.send('toggle-always-on-top'),
  showNotification: (title, body) => ipcRenderer.send('show-notification', title, body),
});
