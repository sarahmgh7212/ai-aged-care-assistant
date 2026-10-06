'use client';

import { useState } from 'react';

type Source = {
  id: string;
  text: string;
  source: string;
  page: number;
};

type Message = {
  role: 'user' | 'assistant';
  content: string;
  sources?: Source[];
};

export default function Home() {
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!question.trim() || loading) {
      return;
    }

    const currentQuestion = question.trim();

    setLoading(true);
    setError('');

    try {
      const response = await fetch('http://127.0.0.1:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: currentQuestion,
          messages: messages,
        }),
      });

      if (!response.ok) {
        throw new Error('Request failed');
      }

      const data = await response.json();

      if (!data || typeof data.answer !== 'string') {
        throw new Error(
          data?.detail || 'The assistant returned an empty response.',
        );
      }

      setMessages((previousMessages) => [
        ...previousMessages,
        {
          role: 'user',
          content: currentQuestion,
        },
        {
          role: 'assistant',
          content: data.answer,
          sources: Array.isArray(data.sources) ? data.sources : [],
        },
      ]);

      setQuestion('');
    } catch (err) {
      setError(
        'Something went wrong while contacting the assistant. Please try again.',
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-50 px-4 py-10">
      <div className="mx-auto max-w-3xl">
        {/* Header */}
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-900">
            AI Aged Care Information Assistant
          </h1>

          <p className="mt-3 text-gray-600">
            Ask questions about aged care and receive answers based on the
            information available in the knowledge base.
          </p>

          <div className="mt-4 rounded-lg border border-gray-200 bg-white p-4 text-left text-sm text-gray-600">
            <strong>Important:</strong> This is an AI-powered information
            assistant and is not an official Aged Care Quality and Safety
            Commission service. It provides general information from its
            knowledge base and should not be treated as medical, legal or
            professional advice.
          </div>
        </div>

        {/* Conversation */}
        {messages.length > 0 && (
          <div className="mt-8 space-y-6">
            {messages.map((message, index) => (
              <div
                key={index}
                className={
                  message.role === 'user'
                    ? 'rounded-lg bg-gray-100 p-4'
                    : 'rounded-lg border border-gray-200 bg-white p-6 shadow-sm'
                }
              >
                <p className="text-sm font-semibold text-gray-900">
                  {message.role === 'user' ? 'You' : 'Assistant'}
                </p>
                <div className="mt-2 whitespace-pre-wrap leading-7 text-gray-700">
                  {message.content}
                </div>
                {/* Sources */}

                {/* Knowledge-base sources */}
                {message.role === 'assistant' &&
                  message.sources &&
                  message.sources.length > 0 && (
                    <div className="mt-6 border-t border-gray-200 pt-5">
                      <div>
                        <p className="text-sm font-semibold text-gray-900">
                          Knowledge-base sources
                        </p>

                        <p className="mt-1 text-sm text-gray-500">
                          These are the evidence passages retrieved from the
                          knowledge base and used to generate the answer.
                        </p>
                      </div>

                      <div className="mt-3 space-y-2">
                        {message.sources.map((source) => (
                          <details
                            key={source.id}
                            className="overflow-hidden rounded-md border border-gray-200 bg-white"
                          >
                            <summary className="cursor-pointer list-none p-3 hover:bg-gray-50">
                              <div className="flex items-center justify-between gap-4">
                                <div>
                                  <span className="text-sm font-semibold text-gray-900">
                                    {source.id}
                                  </span>

                                  <span className="ml-2 text-sm text-gray-700">
                                    {source.source}
                                  </span>
                                </div>

                                <span className="shrink-0 text-xs text-gray-500">
                                  Page {source.page}
                                </span>
                              </div>
                            </summary>

                            <div className="border-t border-gray-200 bg-gray-50 p-4">
                              <p className="text-xs font-medium uppercase tracking-wide text-gray-500">
                                Retrieved evidence
                              </p>

                              <p className="mt-2 whitespace-pre-wrap text-sm leading-6 text-gray-700">
                                {source.text}
                              </p>
                            </div>
                          </details>
                        ))}
                      </div>
                    </div>
                  )}
              </div>
            ))}
          </div>
        )}

        {/* Loading indicator */}
        {loading && (
          <div className="mt-6 rounded-lg border border-gray-200 bg-white p-4">
            <p className="text-sm text-gray-600">Thinking...</p>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="mt-6 rounded-lg border border-red-200 bg-red-50 p-4">
            <p className="text-sm text-red-700">{error}</p>
          </div>
        )}

        {/* Question form */}
        <form onSubmit={handleSubmit} className="mt-8">
          <label
            htmlFor="question"
            className="block text-sm font-medium text-gray-900"
          >
            Your question
          </label>

          <textarea
            id="question"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="For example: What can I do if I am unhappy with the care I receive?"
            rows={4}
            disabled={loading}
            className="mt-2 w-full rounded-lg border border-gray-300 bg-white p-4 text-gray-900 shadow-sm outline-none focus:border-gray-500 focus:ring-1 focus:ring-gray-500 disabled:bg-gray-100"
          />

          <button
            type="submit"
            disabled={loading || !question.trim()}
            className="mt-3 rounded-lg bg-gray-900 px-5 py-3 text-sm font-medium text-white hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading ? 'Thinking...' : 'Ask assistant'}
          </button>
        </form>
      </div>
    </main>
  );
}
