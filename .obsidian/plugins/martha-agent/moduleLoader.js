// Module loader fix for Obsidian plugins
// Obsidian doesn't add plugin node_modules to require paths
// So we load modules with absolute paths

const path = require('path');
const Module = require('module');

// Get the plugin directory
const pluginDir = __dirname;

// Create a require function that looks in plugin's node_modules
function pluginRequire(moduleName) {
  const modulePath = path.join(pluginDir, 'node_modules', moduleName);

  // Try to load from plugin's node_modules
  try {
    return require(modulePath);
  } catch (e) {
    // Fallback to normal require
    return require(moduleName);
  }
}

// Export the custom require
module.exports = { pluginRequire };
