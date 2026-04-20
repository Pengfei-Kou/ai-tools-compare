import { useEffect, useMemo, useState } from 'react';

import { fetchModels } from '../lib/api';
import type { AIModel } from '../types/api';

type SortKey = 'name' | 'provider' | 'input_price' | 'output_price' | 'context_window';
type SortDir = 'asc' | 'desc';

const PROVIDERS = ['All', 'OpenAI', 'Anthropic', 'Google', 'DeepSeek'];

export default function ModelsTable() {
  const [models, setModels] = useState<AIModel[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [sortKey, setSortKey] = useState<SortKey>('input_price');
  const [sortDir, setSortDir] = useState<SortDir>('asc');
  const [provider, setProvider] = useState<string>('All');

  useEffect(() => {
    fetchModels()
      .then((data) => setModels(data.models))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const filteredSorted = useMemo(() => {
    const filtered = provider === 'All' ? models : models.filter((m) => m.provider === provider);
    return [...filtered].sort((a, b) => {
      const av = a[sortKey];
      const bv = b[sortKey];
      if (typeof av === 'string' && typeof bv === 'string') {
        return sortDir === 'asc' ? av.localeCompare(bv) : bv.localeCompare(av);
      }
      return sortDir === 'asc' ? Number(av) - Number(bv) : Number(bv) - Number(av);
    });
  }, [models, sortKey, sortDir, provider]);

  const toggleSort = (key: SortKey) => {
    if (key === sortKey) {
      setSortDir(sortDir === 'asc' ? 'desc' : 'asc');
    } else {
      setSortKey(key);
      setSortDir('asc');
    }
  };

  const sortIndicator = (key: SortKey) => (sortKey === key ? (sortDir === 'asc' ? ' ↑' : ' ↓') : '');

  if (loading) return <div className="status">Loading models...</div>;
  if (error) return <div className="status error">Failed to load: {error}</div>;

  return (
    <div className="models-table-wrapper">
      <div className="filters">
        <span className="filter-label">Provider:</span>
        {PROVIDERS.map((p) => (
          <button
            key={p}
            className={`filter-btn ${provider === p ? 'active' : ''}`}
            onClick={() => setProvider(p)}
          >
            {p}
          </button>
        ))}
      </div>

      <div className="table-scroll">
        <table className="models-table">
          <thead>
            <tr>
              <th onClick={() => toggleSort('name')}>Model{sortIndicator('name')}</th>
              <th onClick={() => toggleSort('provider')}>Provider{sortIndicator('provider')}</th>
              <th onClick={() => toggleSort('input_price')}>Input $/M{sortIndicator('input_price')}</th>
              <th onClick={() => toggleSort('output_price')}>Output $/M{sortIndicator('output_price')}</th>
              <th onClick={() => toggleSort('context_window')}>Context{sortIndicator('context_window')}</th>
            </tr>
          </thead>
          <tbody>
            {filteredSorted.map((m) => (
              <tr key={m.id}>
                <td className="model-name">{m.name}</td>
                <td>
                  <span className={`provider-badge provider-${m.provider.toLowerCase()}`}>{m.provider}</span>
                </td>
                <td className="price">${m.input_price.toFixed(2)}</td>
                <td className="price">${m.output_price.toFixed(2)}</td>
                <td className="context">{(m.context_window / 1000).toLocaleString()}K</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <style>{`
        .models-table-wrapper {
          margin: 2rem 0;
        }

        .filters {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
          align-items: center;
          margin-bottom: 1rem;
        }

        .filter-label {
          color: var(--color-text-muted);
          margin-right: 0.5rem;
        }

        .filter-btn {
          background: var(--color-bg-secondary);
          color: var(--color-text-muted);
          border: 1px solid var(--color-border);
          padding: 0.4rem 0.9rem;
          border-radius: 6px;
          cursor: pointer;
          font-size: 0.9rem;
          transition: all 0.2s;
        }

        .filter-btn:hover {
          color: var(--color-text);
          border-color: var(--color-primary);
        }

        .filter-btn.active {
          background: var(--color-primary);
          color: var(--color-bg);
          border-color: var(--color-primary);
        }

        .table-scroll {
          overflow-x: auto;
          border: 1px solid var(--color-border);
          border-radius: 12px;
        }

        .models-table {
          width: 100%;
          border-collapse: collapse;
          background: var(--color-bg-secondary);
        }

        .models-table th {
          text-align: left;
          padding: 1rem;
          font-weight: 600;
          color: var(--color-text-muted);
          background: var(--color-bg);
          border-bottom: 1px solid var(--color-border);
          cursor: pointer;
          user-select: none;
        }

        .models-table th:hover {
          color: var(--color-primary);
        }

        .models-table td {
          padding: 0.9rem 1rem;
          border-bottom: 1px solid var(--color-border);
        }

        .models-table tr:last-child td {
          border-bottom: none;
        }

        .model-name {
          font-weight: 600;
          color: var(--color-text);
        }

        .provider-badge {
          display: inline-block;
          padding: 0.2rem 0.6rem;
          border-radius: 4px;
          font-size: 0.8rem;
          font-weight: 500;
        }

        .provider-openai { background: rgba(16, 163, 127, 0.15); color: #10a37f; }
        .provider-anthropic { background: rgba(217, 119, 87, 0.15); color: #d97757; }
        .provider-google { background: rgba(66, 133, 244, 0.15); color: #4285f4; }
        .provider-deepseek { background: rgba(139, 92, 246, 0.15); color: #8b5cf6; }

        .price {
          font-family: 'SF Mono', Monaco, monospace;
          color: var(--color-accent);
        }

        .context {
          color: var(--color-text-muted);
          font-size: 0.9rem;
        }

        .status {
          padding: 2rem;
          text-align: center;
          color: var(--color-text-muted);
        }

        .status.error {
          color: #ef4444;
        }
      `}</style>
    </div>
  );
}
