---
Status:: #status/new
Priority:: #priority/high
Assignee:: [[Gregory Karsten]]
DueDate:: 2025-08-30
---

# WhatsApp Note-to-Self System

**Purpose**: Monitor WhatsApp self-messages for task creation and note updates  
**Method**: Send messages to yourself (27833911315) which Claude will monitor and respond to  
**Response**: Direct WhatsApp reply with confirmation of action taken  

## System Design

### Message Monitoring
- **Target**: Messages sent to your own number (27833911315)
- **Detection**: Monitor for new self-messages via messaging system
- **Processing**: Parse message content for instructions
- **Response**: Send confirmation WhatsApp reply

### Supported Commands

#### Task Creation
**Format**: "Task: [task description] #priority/[level] #due:[date]"  
**Example**: "Task: Review BEV contracts #priority/high #due:2025-09-01"  
**Action**: Add to master task list and create calendar entry if due date provided

#### Note Updates  
**Format**: "Note: [note content] #project/[name] #person/[name]"  
**Example**: "Note: Meeting with Sipho about Gloria equipment #project/gloria #person/sipho"  
**Action**: Add to appropriate project file or daily note

#### Quick Reminders
**Format**: "Remind: [reminder] in [timeframe]"  
**Example**: "Remind: Call Lizette about leaky feeder in 2 hours"  
**Action**: Create reminder task with appropriate timing

#### Daily Notes
**Format**: "Daily: [content]"  
**Example**: "Daily: HD0054 engine needs heat shield material"  
**Action**: Add to today's daily note

### Implementation Requirements

#### Messaging Integration
```python
# Monitor for new messages to self
messages = list_messages(sender_phone_number="27833911315")
# Filter for messages to self (note-to-self)
self_messages = [msg for msg in messages if msg.chat_type == "self"]
# Process new messages since last check
process_new_messages(self_messages)
```

#### Response System
```python
# Send confirmation back via WhatsApp
send_message(
    recipient="27833911315", 
    message="✅ Task added: [task description] - Due: [date]"
)
```

### Workflow

1. **Greg sends message to himself** via WhatsApp note-to-self
2. **Claude monitors** WhatsApp for new self-messages  
3. **Parse message** for command type and content
4. **Execute action** (add task, update note, etc.)
5. **Send confirmation** back via WhatsApp
6. **Update MarthaVault** files accordingly

### Message Processing Logic

#### Task Commands
- Parse priority level (#priority/high, #priority/medium, etc.)
- Extract due dates (#due:YYYY-MM-DD)
- Add to `tasks/master_task_list.md`
- Create calendar entry if due date provided
- Link to relevant projects if tags present

#### Note Commands  
- Identify target location (project, person, daily)
- Create or update appropriate file
- Maintain proper tagging and linking
- Add timestamps and context

#### Error Handling
- Invalid command format → request clarification
- Missing required fields → prompt for details  
- System errors → notify via WhatsApp with error details

### Real-Time Processing (Preferred)
- **Method**: WebSocket connection or webhook notifications
- **Response Time**: Immediate (within seconds)
- **Event-Driven**: Process messages as they arrive
- **Always Available**: 24/7 real-time processing

#### Implementation Options:

**Option 1: WebSocket Connection**
```javascript
// Establish persistent WebSocket connection to WhatsApp bridge
const ws = new WebSocket('ws://messaging-bridge/messages');
ws.onmessage = (event) => {
    const message = JSON.parse(event.data);
    if (message.sender === '27833911315' && message.to === '27833911315') {
        processNoteToSelf(message);
    }
};
```

**Option 2: Webhook Notifications**
```javascript
// Messaging bridge sends POST requests when new messages arrive
app.post('/webhook/whatsapp', (req, res) => {
    const message = req.body;
    if (message.type === 'note_to_self' && message.sender === '27833911315') {
        processMessage(message);
        sendConfirmation(message.sender, `✅ Processed: ${message.content}`);
    }
});
```


### Security & Privacy
- **Access Control**: Only process messages from your number to yourself
- **Data Validation**: Sanitize all input before processing
- **Error Logging**: Track processing issues for debugging
- **Backup**: Maintain message processing log

### Examples

#### Task Creation Example
**Your Message**: "Task: Finalize TMM COP presentation #priority/high #due:2025-09-03"  
**Claude Response**: "✅ Task added to master list: 'Finalize TMM COP presentation' - Priority: High - Due: Sep 3, 2025 📅"  
**Actions**: Added to master_task_list.md + calendar entry created

#### Note Update Example  
**Your Message**: "Note: Spoke with Xavier about lamp room contract progress #person/xavier #contract"  
**Claude Response**: "✅ Note added to Xavier Peterson's file: Contract discussion logged"  
**Actions**: Updated `people/Xavier Peterson.md` with timestamp and content

#### Daily Note Example
**Your Message**: "Daily: DMRE presentation went well, good feedback on safety protocols"  
**Claude Response**: "✅ Added to today's daily note (Aug 27): DMRE presentation feedback"  
**Actions**: Updated `00_Inbox/2025-08-27.md`

## Next Steps

1. **Implement monitoring script** - Check WhatsApp messages regularly
2. **Set up message parsing** - Command recognition and validation  
3. **Create response system** - Confirmation messages via WhatsApp
4. **Test workflow** - Send test messages and verify processing
5. **Deploy automation** - Schedule regular monitoring

#automation #note-taking #task-management #self-messaging #year/2025

See: ProductionReports/CLAUDE.md and ProductionReports/reference/*.