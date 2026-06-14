const { app, BrowserWindow, ipcMain, Tray, Menu, nativeImage, globalShortcut } = require('electron');
const path = require('path');

let mainWindow;
let tray;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 420,
    height: 720,
    minWidth: 380,
    minHeight: 600,
    frame: false,
    transparent: true,
    resizable: true,
    alwaysOnTop: false,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
    icon: path.join(__dirname, 'assets', 'icon.png'),
    titleBarStyle: 'hidden',
    backgroundColor: '#00000000',
  });

  mainWindow.loadFile(path.join(__dirname, 'renderer', 'index.html'));

  // Oynani o'ng pastga joylashtirish
  const { screen } = require('electron');
  const display = screen.getPrimaryDisplay();
  const { width, height } = display.workAreaSize;
  mainWindow.setPosition(width - 440, height - 740);

  mainWindow.on('closed', () => { mainWindow = null; });
}

function createTray() {
  // System tray icon
  const icon = nativeImage.createEmpty();
  tray = new Tray(icon);

  const contextMenu = Menu.buildFromTemplate([
    { label: '🎤 PC Yordamchi', enabled: false },
    { type: 'separator' },
    { label: '📂 Ochish', click: () => { if (mainWindow) mainWindow.show(); else createWindow(); } },
    { label: '🔽 Yashirish', click: () => { if (mainWindow) mainWindow.hide(); } },
    { type: 'separator' },
    { label: '❌ Chiqish', click: () => app.quit() },
  ]);

  tray.setToolTip('PC Yordamchi - O\'zbek tilida ovozli boshqaruv');
  tray.setContextMenu(contextMenu);
  tray.on('click', () => {
    if (mainWindow) {
      mainWindow.isVisible() ? mainWindow.hide() : mainWindow.show();
    }
  });
}

app.whenReady().then(() => {
  createWindow();
  createTray();

  // Global hotkey: Ctrl+Shift+V - ovozni yoqish/o'chirish
  globalShortcut.register('CommandOrControl+Shift+V', () => {
    if (mainWindow) {
      mainWindow.show();
      mainWindow.focus();
      mainWindow.webContents.send('toggle-voice');
    }
  });

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', (e) => {
  e.preventDefault(); // Tray da qolsin
});

app.on('will-quit', () => {
  globalShortcut.unregisterAll();
});

// IPC handlers
ipcMain.on('minimize-window', () => {
  if (mainWindow) mainWindow.minimize();
});

ipcMain.on('close-window', () => {
  if (mainWindow) mainWindow.hide();
});

ipcMain.on('drag-window', (event, { x, y }) => {
  if (mainWindow) {
    const [wx, wy] = mainWindow.getPosition();
    mainWindow.setPosition(wx + x, wy + y);
  }
});
