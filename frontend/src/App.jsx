import { useEffect, useState } from 'react';
import DOMPurify from 'dompurify';
import { BrowserRouter, Link, NavLink, Route, Routes } from 'react-router-dom';

const loadError = 'Nie udało się pobrać danych. Spróbuj ponownie później.';
const teamColors = { instinct: 'bg-warning', mystic: 'text-bg-primary', valor: 'text-bg-danger' };

function useApi(path, isList = false) {
  const [state, setState] = useState({ data: isList ? [] : {}, loading: true, error: null });

  useEffect(() => {
    const controller = new AbortController();

    async function load() {
      try {
        const response = await fetch(path, { signal: controller.signal });
        if (!response.ok) throw new Error(loadError);
        const data = await response.json();
        if (isList && !Array.isArray(data)) throw new Error(loadError);
        if (!controller.signal.aborted) {
          setState({ data: data ?? {}, loading: false, error: null });
        }
      } catch {
        if (!controller.signal.aborted) {
          setState({ data: isList ? [] : {}, loading: false, error: loadError });
        }
      }
    }

    load();
    return () => controller.abort();
  }, [path, isList]);

  return state;
}

function LoadStatus({ loading, error }) {
  if (loading) return <p role="status">Ładowanie…</p>;
  if (error) return <p role="alert" className="alert alert-danger">{error}</p>;
  return null;
}

function Posts() {
  const { data: posts, loading, error } = useApi('/posts/', true);
  const [page, setPage] = useState(1);
  const perPage = 2;
  const pageCount = Math.ceil(posts.length / perPage);

  if (loading || error) return <LoadStatus loading={loading} error={error} />;

  return (
    <div className="container-fluid">
      {posts.length === 0 && <p>Nie ma jeszcze postów.</p>}
      {posts.slice((page - 1) * perPage, page * perPage).map((post) => (
        <article className="bg-light rounded p-3 mb-3" key={post.id}>
          <h1 className="h3 m-0">{post.title}</h1>
          <small>Autor: {post.author}</small>
          <div className="mt-2" dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(post.context) }} />
        </article>
      ))}
      {pageCount > 1 && (
        <nav aria-label="Strony postów">
          <ul className="pagination">
            {Array.from({ length: pageCount }, (_, index) => index + 1).map((number) => (
              <li className={`page-item${number === page ? ' active' : ''}`} key={number}>
                <button
                  className="page-link"
                  type="button"
                  aria-current={number === page ? 'page' : undefined}
                  onClick={() => setPage(number)}
                >
                  {number}
                </button>
              </li>
            ))}
          </ul>
        </nav>
      )}
    </div>
  );
}

function Players() {
  const { data: players, loading, error } = useApi('/players/', true);

  if (loading || error) return <LoadStatus loading={loading} error={error} />;

  return (
    <div className="container-fluid">
      <h1>Gracze</h1>
      {players.length === 0 && <p>Nie ma jeszcze graczy.</p>}
      {players.map((player) => (
        <article className="card mb-2" key={player.id}>
          <div className={`card-header ${teamColors[player.team] ?? 'bg-light'}`}>
            Drużyna: {player.team}
          </div>
          <div className="card-body">
            <h2 className="h4">{player.nickname}</h2>
            <p>Poziom: {player.level}</p>
            {player.trainer_code && <p>Kod trenera: {player.trainer_code}</p>}
          </div>
        </article>
      ))}
    </div>
  );
}

function About({ settings }) {
  const { data, loading, error } = settings;
  if (loading || error) return <LoadStatus loading={loading} error={error} />;

  return (
    <div className="container-fluid">
      <h1>O mnie</h1>
      <p>{data.owner_about || 'Właściciel nie dodał jeszcze opisu.'}</p>
      {data.discord && <p><a href={data.discord}>Discord</a></p>}
      {data.owner_screenshot && (
        <div className="text-center">
          <img src={data.owner_screenshot} className="img-fluid" alt="Screenshot właściciela" />
        </div>
      )}
    </div>
  );
}

function Website() {
  const settings = useApi('/settings/');
  const navClass = ({ isActive }) => `nav-link${isActive ? ' active' : ''}`;

  return (
    <>
      <nav className="navbar navbar-expand-lg bg-light mb-3" aria-label="Menu główne">
        <div className="container-fluid">
          <Link className="navbar-brand" to="/">{settings.data.title || 'PokeGutkowo'}</Link>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Rozwiń menu"
          >
            <span className="navbar-toggler-icon" />
          </button>
          <div className="collapse navbar-collapse" id="navbarSupportedContent">
            <ul className="navbar-nav me-auto">
              <li className="nav-item"><NavLink to="/" end className={navClass}>Strona główna</NavLink></li>
              <li className="nav-item"><NavLink to="/players" className={navClass}>Gracze</NavLink></li>
              <li className="nav-item"><NavLink to="/aboutme" className={navClass}>O mnie</NavLink></li>
            </ul>
          </div>
        </div>
      </nav>
      <main>
        <Routes>
          <Route path="/" element={<Posts />} />
          <Route path="/players" element={<Players />} />
          <Route path="/aboutme" element={<About settings={settings} />} />
          <Route path="*" element={<h1 className="container-fluid">Nie znaleziono strony.</h1>} />
        </Routes>
      </main>
    </>
  );
}

export default function App() {
  return <BrowserRouter><Website /></BrowserRouter>;
}
