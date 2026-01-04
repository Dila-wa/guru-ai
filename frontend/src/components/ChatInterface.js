import React, { useState } from 'react';
import { askQuestion } from '../services/api';
import '../styles/ChatInterface.css';

const ChatInterface = () => {
  const [grade, setGrade] = useState('Grade 9');
  const [subject, setSubject] = useState('Mathematics');
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [chatHistory, setChatHistory] = useState([]);

  const grades = ['Grade 9', 'Grade 10', 'Grade 11', 'Grade 12'];
  const subjects = ['Mathematics', 'Science', 'English', 'History', 'Chemistry'];

  const handleAsk = async (e) => {
    e.preventDefault();
    
    if (!question.trim()) {
      setError('Please enter a question');
      return;
    }

    setLoading(true);
    setError('');
    setAnswer('');

    try {
      const response = await askQuestion(grade, subject, question);
      setAnswer(response.answer || 'No answer received');
      
      // Add to chat history
      setChatHistory([...chatHistory, {
        question,
        answer: response.answer,
        grade,
        subject,
      }]);
      
      setQuestion('');
    } catch (err) {
      setError('Failed to get answer. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-interface">
      <div className="chat-container">
        <div className="chat-header">
          <h1>🎓 Guru.ai - Your AI Tutor</h1>
          <p>Ask questions and get instant answers from your syllabus</p>
        </div>

        <div className="chat-content">
          <form onSubmit={handleAsk} className="question-form">
            <div className="form-group">
              <label htmlFor="grade">Grade:</label>
              <select 
                id="grade"
                value={grade} 
                onChange={(e) => setGrade(e.target.value)}
              >
                {grades.map(g => <option key={g} value={g}>{g}</option>)}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="subject">Subject:</label>
              <select 
                id="subject"
                value={subject} 
                onChange={(e) => setSubject(e.target.value)}
              >
                {subjects.map(s => <option key={s} value={s}>{s}</option>)}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="question">Your Question:</label>
              <textarea 
                id="question"
                value={question} 
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Ask a question about your studies..."
                rows="4"
                disabled={loading}
              />
            </div>

            <button 
              type="submit" 
              disabled={loading}
              className="submit-btn"
            >
              {loading ? '⏳ Thinking...' : '🚀 Ask Question'}
            </button>
          </form>

          {error && (
            <div className="error-message">
              ❌ {error}
            </div>
          )}

          {answer && (
            <div className="answer-box">
              <h3>📖 Answer:</h3>
              <p>{answer}</p>
            </div>
          )}

          {chatHistory.length > 0 && (
            <div className="history">
              <h3>📚 Chat History</h3>
              <div className="history-items">
                {chatHistory.map((item, idx) => (
                  <div key={idx} className="history-item">
                    <p><strong>Q:</strong> {item.question}</p>
                    <p><strong>A:</strong> {item.answer.substring(0, 100)}...</p>
                    <small>{item.grade} - {item.subject}</small>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
