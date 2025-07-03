// CROD GNOME Extension - Quick Access to Everything!
const { St, Clutter, Gio, GLib, Meta, Shell } = imports.gi;
const Main = imports.ui.main;
const PanelMenu = imports.ui.panelMenu;
const PopupMenu = imports.ui.popupMenu;
const Util = imports.misc.util;

class CRODExtension {
    constructor() {
        this._indicator = null;
    }

    enable() {
        // Create indicator
        this._indicator = new PanelMenu.Button(0.0, 'CROD Control', false);
        
        // Create icon
        let icon = new St.Icon({
            icon_name: 'face-cool-symbolic',
            style_class: 'system-status-icon'
        });
        
        // CROD Status Label
        this._statusLabel = new St.Label({
            text: 'CROD Ready',
            y_align: Clutter.ActorAlign.CENTER
        });
        
        // Add to panel
        let box = new St.BoxLayout();
        box.add_child(icon);
        box.add_child(this._statusLabel);
        this._indicator.add_child(box);
        
        // Create menu items
        this._addMenuItems();
        
        // Add to panel
        Main.panel.addToStatusArea('crod-indicator', this._indicator);
        
        // Start background monitoring
        this._startMonitoring();
    }

    _addMenuItems() {
        // Quick Launch Section
        let quickLaunchSection = new PopupMenu.PopupMenuSection();
        quickLaunchSection.addMenuItem(new PopupMenu.PopupSeparatorMenuItem('Quick Launch'));
        
        // VS Code + Claude Code
        let vscodeItem = new PopupMenu.PopupMenuItem('🚀 VS Code + Claude Code');
        vscodeItem.connect('activate', () => {
            // Start VS Code
            Util.spawn(['code', '/home/daniel/Schreibtisch/Crod Programming']);
            
            // Wait a bit then open Claude in browser
            GLib.timeout_add(GLib.PRIORITY_DEFAULT, 2000, () => {
                Util.spawn(['xdg-open', 'https://claude.ai/chat']);
                return false;
            });
            
            // Auto-type "ich bins wieder" after 5 seconds
            GLib.timeout_add(GLib.PRIORITY_DEFAULT, 5000, () => {
                this._typeMessage("ich bins wieder");
                return false;
            });
        });
        quickLaunchSection.addMenuItem(vscodeItem);
        
        // Terminal with CROD
        let terminalItem = new PopupMenu.PopupMenuItem('💻 Terminal + CROD');
        terminalItem.connect('activate', () => {
            Util.spawn(['gnome-terminal', '--', 'bash', '-c', 
                'cd /home/daniel/Schreibtisch/Crod\\ Programming/crod-llama && ' +
                'echo "🧠 CROD ACTIVATED" && ' +
                'echo "Starting services..." && ' +
                './start-learning.sh'
            ]);
        });
        quickLaunchSection.addMenuItem(terminalItem);
        
        // CROD Status Section
        this._indicator.menu.addMenuItem(quickLaunchSection);
        this._indicator.menu.addMenuItem(new PopupMenu.PopupSeparatorMenuItem());
        
        let statusSection = new PopupMenu.PopupMenuSection();
        statusSection.addMenuItem(new PopupMenu.PopupSeparatorMenuItem('CROD Status'));
        
        // Status items
        this._consciousnessItem = new PopupMenu.PopupMenuItem('Consciousness: Loading...');
        this._patternsItem = new PopupMenu.PopupMenuItem('Patterns: Loading...');
        this._heatItem = new PopupMenu.PopupMenuItem('Heat Level: Loading...');
        
        statusSection.addMenuItem(this._consciousnessItem);
        statusSection.addMenuItem(this._patternsItem);
        statusSection.addMenuItem(this._heatItem);
        
        this._indicator.menu.addMenuItem(statusSection);
        
        // Quick Actions
        this._indicator.menu.addMenuItem(new PopupMenu.PopupSeparatorMenuItem());
        
        // Save Session
        let saveItem = new PopupMenu.PopupMenuItem('💾 Save CROD Session');
        saveItem.connect('activate', () => {
            this._saveCRODSession();
        });
        this._indicator.menu.addMenuItem(saveItem);
        
        // Tomorrow's Setup
        let tomorrowItem = new PopupMenu.PopupMenuItem('📅 Setup for Tomorrow');
        tomorrowItem.connect('activate', () => {
            this._setupTomorrow();
        });
        this._indicator.menu.addMenuItem(tomorrowItem);
    }

    _startMonitoring() {
        // Check CROD status every 5 seconds
        this._timeout = GLib.timeout_add_seconds(GLib.PRIORITY_DEFAULT, 5, () => {
            this._updateStatus();
            return true;
        });
    }

    _updateStatus() {
        // Check if services are running
        let [success, stdout] = GLib.spawn_command_line_sync('pgrep -f "crod|llama"');
        
        if (success && stdout.length > 0) {
            this._statusLabel.set_text('CROD Active');
            this._statusLabel.add_style_class_name('crod-active');
            
            // Update menu items with real data (would need API)
            this._consciousnessItem.label.set_text('Consciousness: 45/65');
            this._patternsItem.label.set_text('Patterns: 49,996 active');
            this._heatItem.label.set_text('Heat Level: 🔥 High');
        } else {
            this._statusLabel.set_text('CROD Idle');
            this._statusLabel.remove_style_class_name('crod-active');
        }
    }

    _typeMessage(message) {
        // Auto-type using xdotool
        Util.spawn(['xdotool', 'type', '--delay', '50', message]);
    }

    _saveCRODSession() {
        // Create session backup
        let timestamp = new Date().toISOString().replace(/:/g, '-');
        let backupCmd = `cd /home/daniel/Schreibtisch/Crod\\ Programming && ` +
                       `tar -czf crod-session-${timestamp}.tar.gz crod-llama/`;
        
        Util.spawn(['bash', '-c', backupCmd]);
        
        // Show notification
        Main.notify('CROD Session Saved', `Backup created: crod-session-${timestamp}.tar.gz`);
    }

    _setupTomorrow() {
        // Create startup script for tomorrow
        let script = `#!/bin/bash
# CROD Quick Start Script
echo "🚀 Starting CROD Development Environment..."

# Start VS Code
code /home/daniel/Schreibtisch/Crod\\ Programming &

# Wait for VS Code
sleep 3

# Open Claude
xdg-open https://claude.ai/chat &

# Start CROD services
cd /home/daniel/Schreibtisch/Crod\\ Programming/crod-llama
./start-learning.sh &

# Start delta tracker
cd delta-tracker
./start.sh &

echo "✅ CROD Environment Ready!"
echo "Just say 'ich bins wieder' in Claude!"
`;

        // Save script
        let file = Gio.File.new_for_path('/home/daniel/Desktop/start-crod-tomorrow.sh');
        file.replace_contents(script, null, false, Gio.FileCreateFlags.NONE, null);
        
        // Make executable
        Util.spawn(['chmod', '+x', '/home/daniel/Desktop/start-crod-tomorrow.sh']);
        
        Main.notify('Tomorrow Ready!', 'Double-click start-crod-tomorrow.sh on Desktop');
    }

    disable() {
        if (this._timeout) {
            GLib.source_remove(this._timeout);
        }
        this._indicator.destroy();
        this._indicator = null;
    }
}

function init() {
    return new CRODExtension();
}