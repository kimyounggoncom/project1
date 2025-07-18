import React from 'react';

interface Message {
  id: number;
  type: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

interface ChatWindowProps {
  messages: Message[];
  currentMessage: string;
  setCurrentMessage: (message: string) => void;
  onSendMessage: (e: React.FormEvent) => void;
  isTyping: boolean;
}

export default function ChatWindow({
  messages,
  currentMessage,
  setCurrentMessage,
  onSendMessage,
  isTyping
}: ChatWindowProps) {
  return (
    <div style={{ 
      padding: '20px',
      height: '100%',
      display: 'flex',
      flexDirection: 'column'
    }}>
      {/* 채팅 메시지 영역 */}
      <div style={{ 
        flex: 1, 
        overflowY: 'auto',
        display: 'flex',
        flexDirection: 'column',
        gap: '16px',
        marginBottom: '20px'
      }}>
        {messages.length === 0 ? (
          <div style={{ 
            textAlign: 'center',
            color: '#6b7280',
            marginTop: '100px'
          }}>
            <h2 style={{ fontSize: '24px', marginBottom: '8px' }}>
              안녕하세요! 👋
            </h2>
            <p>무엇을 도와드릴까요?</p>
          </div>
        ) : (
          messages.map((msg) => (
            <div
              key={msg.id}
              style={{
                display: 'flex',
                justifyContent: msg.type === 'user' ? 'flex-end' : 'flex-start',
                marginBottom: '12px'
              }}
            >
              <div
                style={{
                  maxWidth: '70%',
                  padding: '12px 16px',
                  borderRadius: '18px',
                  backgroundColor: msg.type === 'user' ? '#007bff' : '#f1f3f4',
                  color: msg.type === 'user' ? 'white' : '#2d2d30',
                  fontSize: '14px',
                  lineHeight: '1.4'
                }}
              >
                <div>{msg.content}</div>
                <div style={{ 
                  fontSize: '11px',
                  opacity: 0.7,
                  marginTop: '4px'
                }}>
                  {msg.timestamp}
                </div>
              </div>
            </div>
          ))
        )}

        {isTyping && (
          <div style={{ 
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            color: '#6b7280'
          }}>
            <div>💭</div>
            <div>입력 중...</div>
          </div>
        )}
      </div>

      {/* 메시지 입력 영역 */}
      <div style={{ 
        borderTop: '1px solid #e5e5e5',
        paddingTop: '20px'
      }}>
        <form onSubmit={onSendMessage}>
          <div style={{ 
            display: 'flex',
            gap: '12px',
            alignItems: 'flex-end'
          }}>
            <textarea
              value={currentMessage}
              onChange={(e) => setCurrentMessage(e.target.value)}
              placeholder="메시지를 입력하세요..."
              style={{
                flex: 1,
                padding: '12px 16px',
                border: '1px solid #d1d5db',
                borderRadius: '12px',
                fontSize: '14px',
                resize: 'none',
                minHeight: '44px',
                maxHeight: '120px',
                outline: 'none'
              }}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  onSendMessage(e);
                }
              }}
            />
            <button
              type="submit"
              disabled={!currentMessage.trim()}
              style={{
                backgroundColor: currentMessage.trim() ? '#007bff' : '#e5e5e5',
                color: currentMessage.trim() ? 'white' : '#9ca3af',
                border: 'none',
                borderRadius: '12px',
                padding: '12px 20px',
                cursor: currentMessage.trim() ? 'pointer' : 'not-allowed',
                fontSize: '14px',
                fontWeight: '500'
              }}
            >
              전송
            </button>
          </div>
        </form>
      </div>
    </div>
  );
} 