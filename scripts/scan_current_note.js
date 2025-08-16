/**
 * Scans the currently open note for dates and creates calendar events
 * @returns {string} Results of the scan
 */
module.exports = function() {
    // Get the current active file
    const activeFile = app.workspace.getActiveFile();
    if (!activeFile) {
        return "❌ No note is currently open. Please open a note first.";
    }
    
    // Read the file content
    const content = app.vault.cachedRead(activeFile);
    const createdEvents = [];
    const noteTitle = activeFile.basename;
    
    // Date detection patterns
    const patterns = [
        {
            regex: /meeting.*?(\d{4}-\d{2}-\d{2})/gi,
            type: "Meeting",
            titlePrefix: "Meeting"
        },
        {
            regex: /due.*?(\d{4}-\d{2}-\d{2})/gi,
            type: "Deadline",
            titlePrefix: "Task Due"
        },
        {
            regex: /deadline.*?(\d{4}-\d{2}-\d{2})/gi,
            type: "Deadline", 
            titlePrefix: "Deadline"
        },
        {
            regex: /review.*?(\d{4}-\d{2}-\d{2})/gi,
            type: "Review",
            titlePrefix: "Review"
        },
        {
            regex: /call.*?(\d{4}-\d{2}-\d{2})/gi,
            type: "Call",
            titlePrefix: "Call"
        }
    ];
    
    // Scan content for date patterns
    patterns.forEach(pattern => {
        let match;
        while ((match = pattern.regex.exec(content)) !== null) {
            const date = match[1];
            const eventTitle = `${pattern.titlePrefix} - ${noteTitle}`;
            const fileName = `Schedule/${date} - ${eventTitle}.md`;
            
            // Check if event already exists
            if (app.vault.getAbstractFileByPath(fileName)) {
                continue; // Skip if already exists
            }
            
            try {
                // Create calendar event
                const eventContent = `---
title: ${eventTitle}
allDay: true
date: ${date}
completed: null
---

# ${eventTitle}

**Date**: ${date}  
**Type**: ${pattern.type}  
**Source**: [[${noteTitle}]]

Auto-generated from note content.`;

                // Create the event file
                app.vault.create(fileName, eventContent);
                createdEvents.push(`${eventTitle} (${date})`);
                
            } catch (error) {
                // Skip on error
            }
        }
    });
    
    if (createdEvents.length > 0) {
        return `📅 Auto-created ${createdEvents.length} calendar events:\n${createdEvents.join('\n')}`;
    } else {
        return "🔍 No new dates detected in current note.";
    }
};