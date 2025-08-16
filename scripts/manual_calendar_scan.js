// Manual calendar scanning script
// Run this in developer console when a note is open

function scanNoteForDates() {
    const activeFile = app.workspace.getActiveFile();
    if (!activeFile) {
        console.log("❌ No note is currently open");
        return;
    }
    
    app.vault.cachedRead(activeFile).then(content => {
        const noteTitle = activeFile.basename;
        const createdEvents = [];
        
        // Date detection patterns
        const patterns = [
            { regex: /meeting.*?(\d{4}-\d{2}-\d{2})/gi, type: "Meeting", prefix: "Meeting" },
            { regex: /due.*?(\d{4}-\d{2}-\d{2})/gi, type: "Deadline", prefix: "Task Due" },
            { regex: /deadline.*?(\d{4}-\d{2}-\d{2})/gi, type: "Deadline", prefix: "Deadline" },
            { regex: /review.*?(\d{4}-\d{2}-\d{2})/gi, type: "Review", prefix: "Review" },
            { regex: /call.*?(\d{4}-\d{2}-\d{2})/gi, type: "Call", prefix: "Call" }
        ];
        
        patterns.forEach(pattern => {
            let match;
            while ((match = pattern.regex.exec(content)) !== null) {
                const date = match[1];
                const eventTitle = `${pattern.prefix} - ${noteTitle}`;
                const fileName = `Schedule/${date} - ${eventTitle}.md`;
                
                // Check if event already exists
                if (app.vault.getAbstractFileByPath(fileName)) {
                    continue;
                }
                
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

                app.vault.create(fileName, eventContent)
                    .then(() => {
                        console.log(`✅ Created: ${eventTitle} (${date})`);
                        createdEvents.push(eventTitle);
                    })
                    .catch(err => console.log(`⚠️ Skipped: ${eventTitle} (may already exist)`));
            }
        });
        
        setTimeout(() => {
            if (createdEvents.length === 0) {
                console.log("🔍 No dates detected in current note");
            }
        }, 1000);
    });
}

// Run the function
scanNoteForDates();