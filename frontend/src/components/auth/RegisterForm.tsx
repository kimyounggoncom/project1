import { useState } from 'react';
import GoogleLoginButton from '../ui/GoogleLoginButton';

interface RegisterFormProps {
  onRegister: (email: string, password: string, fullName: string) => void;
  onGoogleLogin: () => void;
  onSwitchToLogin: () => void;
  message?: string;
  isLoading?: boolean;
}

export default function RegisterForm({ 
  onRegister, 
  onGoogleLogin, 
  onSwitchToLogin, 
  message,
  isLoading = false 
}: RegisterFormProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onRegister(email, password, fullName);
  };

  return (
    <div style={{ padding: '50px', maxWidth: '500px', margin: '0 auto' }}>
      <h1 style={{ textAlign: 'center', color: '#1f2937', marginBottom: '30px' }}>
        🔐 MSA 인증 시스템
      </h1>

      <div style={{ textAlign: 'center', marginBottom: '30px' }}>
        <button 
          onClick={onSwitchToLogin}
          style={{
            backgroundColor: '#e5e7eb',
            color: '#6b7280',
            padding: '10px 20px',
            border: 'none',
            borderRadius: '6px 0 0 6px',
            cursor: 'pointer'
          }}
        >
          로그인
        </button>
        <button 
          style={{
            backgroundColor: '#2563eb',
            color: 'white',
            padding: '10px 20px',
            border: 'none',
            borderRadius: '0 6px 6px 0',
            cursor: 'pointer'
          }}
        >
          회원가입
        </button>
      </div>

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '20px' }}>
          <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
            이름:
          </label>
          <input
            type="text"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            required
            disabled={isLoading}
            style={{
              width: '100%',
              padding: '12px',
              border: '1px solid #d1d5db',
              borderRadius: '6px',
              fontSize: '16px'
            }}
          />
        </div>

        <div style={{ marginBottom: '20px' }}>
          <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
            이메일:
          </label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            disabled={isLoading}
            style={{
              width: '100%',
              padding: '12px',
              border: '1px solid #d1d5db',
              borderRadius: '6px',
              fontSize: '16px'
            }}
          />
        </div>

        <div style={{ marginBottom: '20px' }}>
          <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
            비밀번호:
          </label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            disabled={isLoading}
            style={{
              width: '100%',
              padding: '12px',
              border: '1px solid #d1d5db',
              borderRadius: '6px',
              fontSize: '16px'
            }}
          />
        </div>

        <button 
          type="submit"
          disabled={isLoading}
          style={{
            width: '100%',
            backgroundColor: isLoading ? '#9ca3af' : '#2563eb',
            color: 'white',
            padding: '12px',
            border: 'none',
            borderRadius: '6px',
            fontSize: '16px',
            cursor: isLoading ? 'not-allowed' : 'pointer',
            marginBottom: '20px'
          }}
        >
          {isLoading ? '가입 중...' : '회원가입'}
        </button>
      </form>

      {/* 구분선 */}
      <div style={{ 
        display: 'flex', 
        alignItems: 'center', 
        margin: '20px 0',
        color: '#6b7280'
      }}>
        <div style={{ flex: 1, height: '1px', backgroundColor: '#e5e7eb' }}></div>
        <span style={{ padding: '0 16px', fontSize: '14px' }}>또는</span>
        <div style={{ flex: 1, height: '1px', backgroundColor: '#e5e7eb' }}></div>
      </div>

      {/* 구글 로그인 버튼 */}
      <div style={{ marginBottom: '20px' }}>
        <GoogleLoginButton 
          onLogin={onGoogleLogin}
          fullWidth={true}
        />
      </div>

      {message && (
        <div style={{ 
          padding: '15px', 
          backgroundColor: message.includes('성공') ? '#d1fae5' : '#fee2e2',
          color: message.includes('성공') ? '#065f46' : '#dc2626',
          borderRadius: '6px',
          marginBottom: '20px'
        }}>
          {message}
        </div>
      )}

      <div style={{ 
        backgroundColor: '#f9fafb', 
        padding: '15px', 
        borderRadius: '8px',
        fontSize: '14px',
        color: '#6b7280'
      }}>
        <p><strong>📡 API 연결 정보:</strong></p>
        <p>• Gateway: {process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080'}</p>
        <p>• Frontend → Gateway → Auth Service</p>
        <p>• 실시간 JWT 토큰 기반 인증</p>
      </div>
    </div>
  );
} 