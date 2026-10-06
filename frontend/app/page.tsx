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

const exampleQuestions = [
  'What rights do older people have when receiving aged care?',
  'What can I do if I am unhappy with the care I receive?',
  'What choices should older people have about their care?',
];

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
      const response = await fetch(
        process.env.NEXT_PUBLIC_API_URL + '/api/chat',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            question: currentQuestion,
            messages: messages,
          }),
        },
      );

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

  const handleExampleQuestion = (example: string) => {
    if (loading) {
      return;
    }

    setQuestion(example);

    setTimeout(() => {
      document.getElementById('question')?.focus();
    }, 0);
  };

  const handleNewConversation = () => {
    if (loading) {
      return;
    }

    setMessages([]);
    setQuestion('');
    setError('');

    setTimeout(() => {
      document.getElementById('question')?.focus();
    }, 0);
  };

  return (
    <main className="min-h-screen bg-gray-50 px-4 py-6 sm:px-6 sm:py-10">
      <div className="mx-auto max-w-4xl">
        {/* Navigation */}
        <nav className="flex items-center justify-between border-b border-gray-200 pb-4">
          <div className="text-sm font-semibold text-gray-900">
            AI Aged Care Assistant
          </div>

          <a
            href="/evaluation"
            className="rounded-md px-3 py-2 text-sm font-medium text-gray-600 transition hover:bg-gray-100 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-400"
          >
            Evaluation Dashboard
          </a>
        </nav>

        {/* Header */}
        <header className="mx-auto mt-10 max-w-3xl text-center">
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-gray-900 text-lg font-semibold text-white">
            AI
          </div>

          <h1 className="mt-5 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            AI Aged Care Information Assistant
          </h1>

          <p className="mx-auto mt-4 max-w-2xl text-base leading-7 text-gray-600">
            Ask questions about aged care and receive information grounded in
            the assistant&apos;s knowledge base.
          </p>

          {/* Important notice */}
          <div
            role="note"
            className="mt-6 rounded-lg border border-gray-200 bg-white p-4 text-left text-sm leading-6 text-gray-600 shadow-sm"
          >
            <span className="font-semibold text-gray-900">Important:</span> This
            is an AI-powered information assistant and is not an official Aged
            Care Quality and Safety Commission service. It provides general
            information from its knowledge base and should not be treated as
            medical, legal or professional advice.
          </div>
        </header>

        {/* Empty state / example questions */}
        {messages.length === 0 && !loading && (
          <section className="mt-10">
            <div className="text-center">
              <h2 className="text-sm font-semibold text-gray-900">
                Try an example question
              </h2>

              <p className="mt-1 text-sm text-gray-500">
                Select a question to get started.
              </p>
            </div>

            <div className="mt-4 grid gap-3 sm:grid-cols-3">
              {exampleQuestions.map((example) => (
                <button
                  key={example}
                  type="button"
                  onClick={() => handleExampleQuestion(example)}
                  className="rounded-lg border border-gray-200 bg-white p-4 text-left text-sm leading-6 text-gray-700 shadow-sm transition hover:border-gray-300 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-400"
                >
                  {example}
                </button>
              ))}
            </div>
          </section>
        )}

        {/* Conversation */}
        {messages.length > 0 && (
          <section aria-label="Conversation" className="mt-10 space-y-5">
            {messages.map((message, index) => (
              <div
                key={index}
                className={
                  message.role === 'user'
                    ? 'ml-auto max-w-3xl rounded-2xl bg-gray-900 px-5 py-4 text-white shadow-sm'
                    : 'max-w-3xl rounded-2xl border border-gray-200 bg-white px-5 py-5 shadow-sm'
                }
              >
                <p
                  className={
                    message.role === 'user'
                      ? 'text-xs font-semibold uppercase tracking-wide text-gray-300'
                      : 'text-xs font-semibold uppercase tracking-wide text-gray-500'
                  }
                >
                  {message.role === 'user' ? 'You' : 'Assistant'}
                </p>

                <div
                  className={
                    message.role === 'user'
                      ? 'mt-2 whitespace-pre-wrap leading-7 text-white'
                      : 'mt-2 whitespace-pre-wrap leading-7 text-gray-700'
                  }
                >
                  {message.content}
                </div>

                {/* Knowledge-base sources */}
                {message.role === 'assistant' &&
                  message.sources &&
                  message.sources.length > 0 && (
                    <div className="mt-6 border-t border-gray-200 pt-5">
                      <div>
                        <p className="text-sm font-semibold text-gray-900">
                          Knowledge-base sources
                        </p>

                        <p className="mt-1 text-sm leading-6 text-gray-500">
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
                            <summary className="cursor-pointer list-none p-3 transition hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-gray-400">
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
          </section>
        )}

        {/* Loading indicator */}
        {loading && (
          <div
            className="mt-6 flex max-w-3xl items-center gap-3 rounded-2xl border border-gray-200 bg-white px-5 py-4 shadow-sm"
            role="status"
            aria-live="polite"
          >
            <div className="flex gap-1">
              <span className="h-2 w-2 animate-pulse rounded-full bg-gray-400" />
              <span className="h-2 w-2 animate-pulse rounded-full bg-gray-400 [animation-delay:150ms]" />
              <span className="h-2 w-2 animate-pulse rounded-full bg-gray-400 [animation-delay:300ms]" />
            </div>

            <p className="text-sm text-gray-600">
              Searching the knowledge base and generating an answer...
            </p>
          </div>
        )}

        {/* Error */}
        {error && (
          <div
            className="mt-6 rounded-lg border border-red-200 bg-red-50 p-4"
            role="alert"
          >
            <p className="text-sm font-medium text-red-800">
              Unable to contact the assistant
            </p>

            <p className="mt-1 text-sm leading-6 text-red-700">{error}</p>
          </div>
        )}

        {/* Question form */}
        <form
          onSubmit={handleSubmit}
          className="mt-8 rounded-xl border border-gray-200 bg-white p-4 shadow-sm sm:p-5"
        >
          <div className="flex items-center justify-between gap-4">
            <label
              htmlFor="question"
              className="block text-sm font-semibold text-gray-900"
            >
              Your question
            </label>

            {messages.length > 0 && (
              <button
                type="button"
                onClick={handleNewConversation}
                disabled={loading}
                className="text-sm font-medium text-gray-500 transition hover:text-gray-900 disabled:cursor-not-allowed disabled:opacity-50"
              >
                New conversation
              </button>
            )}
          </div>

          <textarea
            id="question"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="For example: What can I do if I am unhappy with the care I receive?"
            rows={4}
            disabled={loading}
            aria-describedby="question-help"
            className="mt-3 w-full resize-y rounded-lg border border-gray-300 bg-white p-4 text-gray-900 shadow-sm outline-none transition placeholder:text-gray-400 focus:border-gray-500 focus:ring-2 focus:ring-gray-200 disabled:cursor-not-allowed disabled:bg-gray-100"
          />

          <div className="mt-3 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <p id="question-help" className="text-xs leading-5 text-gray-500">
              Information is generated using the available aged care knowledge
              base.
            </p>

            <button
              type="submit"
              disabled={loading || !question.trim()}
              className="rounded-lg bg-gray-900 px-5 py-3 text-sm font-medium text-white transition hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-400 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? 'Generating...' : 'Ask assistant'}
            </button>
          </div>
        </form>

        {/* Footer */}
        <footer className="mt-8 pb-4 text-center text-xs leading-5 text-gray-500">
          AI Aged Care Information Assistant · Portfolio project
        </footer>
      </div>
    </main>
  );
}
