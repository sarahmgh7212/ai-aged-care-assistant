'use client';

import { useEffect, useState } from 'react';

type EvaluationMetrics = {
  retrieval_accuracy: number;
  out_of_scope_rejection: number;
  grounded_answers: number;
  relevant_answers: number;
  complete_answers: number;
  citation_accuracy: number;
  no_hallucination: number;
};

type QuestionEvaluation = {
  grounded?: boolean;
  relevant?: boolean;
  complete?: boolean;
  citations_correct?: boolean;
  no_hallucination?: boolean;
  reason?: string;
};

type QuestionResult = {
  id: string;
  question: string;
  answerable: boolean;
  retrieved_source_count: number;
  retrieval_success: boolean;
  out_of_scope_rejection_success: boolean | null;
  answer: string;
  evaluation: QuestionEvaluation;
};

type EvaluationResults = {
  total_questions: number;
  answerable_questions: number;
  out_of_scope_questions: number;
  metrics: EvaluationMetrics;
  questions: QuestionResult[];
};

function MetricCard({ title, value }: { title: string; value: number }) {
  return (
    <div className="rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
      <p className="text-sm text-gray-500">{title}</p>

      <p className="mt-2 text-3xl font-bold text-gray-900">
        {value.toFixed(1)}%
      </p>
    </div>
  );
}

export default function EvaluationPage() {
  const [results, setResults] = useState<EvaluationResults | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const loadResults = async () => {
      try {
        const response = await fetch(
          process.env.NEXT_PUBLIC_API_URL + '/api/evaluation',
        );

        if (!response.ok) {
          throw new Error('Failed to load evaluation results.');
        }

        const data = await response.json();

        setResults(data);
      } catch (err) {
        setError(
          'Unable to load evaluation results. Make sure the backend is running.',
        );
      } finally {
        setLoading(false);
      }
    };

    loadResults();
  }, []);

  if (loading) {
    return (
      <main className="min-h-screen bg-gray-50 px-4 py-10">
        <div className="mx-auto max-w-6xl">
          <div className="rounded-lg border border-gray-200 bg-white p-6">
            <p className="text-gray-600">Loading evaluation results...</p>
          </div>
        </div>
      </main>
    );
  }

  if (error) {
    return (
      <main className="min-h-screen bg-gray-50 px-4 py-10">
        <div className="mx-auto max-w-6xl">
          <div className="rounded-lg border border-red-200 bg-red-50 p-6">
            <p className="text-red-700">{error}</p>
          </div>
        </div>
      </main>
    );
  }

  if (!results) {
    return null;
  }

  const { metrics } = results;

  return (
    <main className="min-h-screen bg-gray-50 px-4 py-10">
      <div className="mx-auto max-w-6xl">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            Evaluation Dashboard
          </h1>

          <p className="mt-2 max-w-3xl text-gray-600">
            Evaluation results for the AI Aged Care Information Assistant. These
            metrics measure retrieval performance, answer quality, grounding,
            citation accuracy, and hallucination prevention.
          </p>
        </div>

        {/* Overview */}
        <div className="mt-8 grid gap-4 sm:grid-cols-3">
          <div className="rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
            <p className="text-sm text-gray-500">Total questions</p>

            <p className="mt-2 text-3xl font-bold text-gray-900">
              {results.total_questions}
            </p>
          </div>

          <div className="rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
            <p className="text-sm text-gray-500">Answerable questions</p>

            <p className="mt-2 text-3xl font-bold text-gray-900">
              {results.answerable_questions}
            </p>
          </div>

          <div className="rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
            <p className="text-sm text-gray-500">Out-of-scope questions</p>

            <p className="mt-2 text-3xl font-bold text-gray-900">
              {results.out_of_scope_questions}
            </p>
          </div>
        </div>

        {/* Metrics */}
        <section className="mt-10">
          <h2 className="text-xl font-semibold text-gray-900">
            Performance metrics
          </h2>

          <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <MetricCard
              title="Retrieval accuracy"
              value={metrics.retrieval_accuracy}
            />

            <MetricCard
              title="Out-of-scope rejection"
              value={metrics.out_of_scope_rejection}
            />

            <MetricCard
              title="Grounded answers"
              value={metrics.grounded_answers}
            />

            <MetricCard
              title="Relevant answers"
              value={metrics.relevant_answers}
            />

            <MetricCard
              title="Complete answers"
              value={metrics.complete_answers}
            />

            <MetricCard
              title="Citation accuracy"
              value={metrics.citation_accuracy}
            />

            <MetricCard
              title="No hallucination"
              value={metrics.no_hallucination}
            />
          </div>
        </section>

        {/* Individual questions */}
        <section className="mt-10">
          <h2 className="text-xl font-semibold text-gray-900">
            Individual evaluation results
          </h2>

          <p className="mt-2 text-sm text-gray-600">
            Expand a question to inspect the generated answer and automated
            evaluation.
          </p>

          <div className="mt-4 space-y-3">
            {results.questions.map((item) => (
              <details
                key={item.id}
                className="overflow-hidden rounded-lg border border-gray-200 bg-white shadow-sm"
              >
                <summary className="cursor-pointer list-none p-5 hover:bg-gray-50">
                  <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
                    <div>
                      <span className="text-sm font-semibold text-gray-900">
                        {item.id}
                      </span>

                      <p className="mt-1 text-gray-700">{item.question}</p>
                    </div>

                    <div className="shrink-0">
                      {item.answerable ? (
                        <span className="rounded-full bg-gray-100 px-3 py-1 text-xs font-medium text-gray-700">
                          Answerable
                        </span>
                      ) : (
                        <span className="rounded-full bg-gray-100 px-3 py-1 text-xs font-medium text-gray-700">
                          Out of scope
                        </span>
                      )}
                    </div>
                  </div>
                </summary>

                <div className="border-t border-gray-200 p-5">
                  {/* Retrieval */}
                  <div>
                    <h3 className="text-sm font-semibold text-gray-900">
                      Retrieval
                    </h3>

                    <p className="mt-1 text-sm text-gray-600">
                      Sources retrieved:{' '}
                      <strong>{item.retrieved_source_count}</strong>
                    </p>

                    <p className="mt-1 text-sm text-gray-600">
                      Retrieval successful:{' '}
                      <strong>{item.retrieval_success ? 'Yes' : 'No'}</strong>
                    </p>
                  </div>

                  {/* Answer */}
                  <div className="mt-6">
                    <h3 className="text-sm font-semibold text-gray-900">
                      Generated answer
                    </h3>

                    <div className="mt-2 rounded-md bg-gray-50 p-4">
                      <p className="whitespace-pre-wrap text-sm leading-6 text-gray-700">
                        {item.answer}
                      </p>
                    </div>
                  </div>

                  {/* Evaluation */}
                  <div className="mt-6">
                    <h3 className="text-sm font-semibold text-gray-900">
                      Automated evaluation
                    </h3>

                    <div className="mt-3 grid gap-2 sm:grid-cols-2 lg:grid-cols-4">
                      {item.answerable ? (
                        <>
                          <EvaluationResult
                            label="Grounded"
                            value={item.evaluation.grounded}
                          />

                          <EvaluationResult
                            label="Relevant"
                            value={item.evaluation.relevant}
                          />

                          <EvaluationResult
                            label="Complete"
                            value={item.evaluation.complete}
                          />

                          <EvaluationResult
                            label="Citations"
                            value={item.evaluation.citations_correct}
                          />
                        </>
                      ) : (
                        <EvaluationResult
                          label="No hallucination"
                          value={item.evaluation.no_hallucination}
                        />
                      )}
                    </div>
                  </div>

                  {/* Reason */}
                  {item.evaluation.reason && (
                    <div className="mt-6">
                      <h3 className="text-sm font-semibold text-gray-900">
                        Evaluation reasoning
                      </h3>

                      <p className="mt-2 text-sm leading-6 text-gray-600">
                        {item.evaluation.reason}
                      </p>
                    </div>
                  )}
                </div>
              </details>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}

function EvaluationResult({
  label,
  value,
}: {
  label: string;
  value?: boolean;
}) {
  if (value === undefined) {
    return null;
  }

  return (
    <div className="rounded-md border border-gray-200 p-3">
      <p className="text-xs text-gray-500">{label}</p>

      <p className="mt-1 text-sm font-semibold text-gray-900">
        {value ? 'Pass' : 'Fail'}
      </p>
    </div>
  );
}
