'use client';

import { FormEvent, useState } from 'react';

type Source = {
  id: string;
  source: string;
  page: number;
};

type ChatResponse = {
  answer: string;
  sources: Source[];
};

export default function Home() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [sources, setSources] = useState<Source[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();

    if (!question.trim()) {
      return;
    }

    setLoading(true);
    setError('');
    setAnswer('');
    setSources([]);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get a response from the server.');
      }

      const data: ChatResponse = await response.json();

      setAnswer(data.answer);
      setSources(data.sources);
    } catch (err) {
      console.error(err);
      setError(
        'Sorry, something went wrong while getting an answer. Please try again.',
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-gray-50 px-6 py-12">
      <div className="mx-auto max-w-3xl">
        <h1 className="text-3xl font-bold text-gray-900">
          Aged Care Information Assistant
        </h1>

        <p className="mt-3 text-gray-600">
          Ask questions about aged care and receive answers based on the
          available official information.
        </p>

        <form onSubmit={handleSubmit} className="mt-8">
          <textarea
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="Ask a question about aged care..."
            rows={4}
            className="w-full rounded-lg border border-gray-300 bg-white p-4 text-gray-900 shadow-sm focus:border-blue-500 focus:outline-none"
          />

          <button
            type="submit"
            disabled={loading || !question.trim()}
            className="mt-4 rounded-lg bg-blue-600 px-6 py-3 font-medium text-white disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading ? 'Finding an answer...' : 'Ask question'}
          </button>
        </form>

        {error && (
          <div className="mt-6 rounded-lg border border-red-200 bg-red-50 p-4 text-red-700">
            {error}
          </div>
        )}

        {answer && (
          <section className="mt-10">
            <h2 className="text-xl font-semibold text-gray-900">Answer</h2>

            <div className="mt-4 rounded-lg bg-white p-6 shadow-sm">
              <p className="whitespace-pre-wrap leading-7 text-gray-800">
                {answer}
              </p>
            </div>
          </section>
        )}

        {sources.length > 0 && (
          <section className="mt-8">
            <h2 className="text-xl font-semibold text-gray-900">Sources</h2>

            <div className="mt-4 space-y-3">
              {sources.map((source) => (
                <div
                  key={source.id}
                  className="rounded-lg border border-gray-200 bg-white p-4"
                >
                  <p className="font-medium text-gray-900">
                    [{source.id}] {source.source}
                  </p>

                  <p className="mt-1 text-sm text-gray-600">
                    Page {source.page}
                  </p>
                </div>
              ))}
            </div>
          </section>
        )}
      </div>
    </main>
  );
}
