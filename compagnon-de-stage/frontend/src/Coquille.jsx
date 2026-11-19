import { useEffect, useState } from 'react'
import Icone from './Icone.jsx'

// La « coquille » commune aux deux espaces : la navigation à gauche, le bandeau de la page, puis son contenu.
// - sections : [{ titre, liens: [{ cle, nom, icone, description, badge }] }]
// - page / allerA : la page affichée et la fonction pour en changer
// - qui : le bloc sous le logo (prénom, jeu…) ; pied : ce qui s'affiche au-dessus des boutons du bas (l'avancement)
// - actions : les boutons à droite du bandeau

const CLE_THEME = 'compagnon-theme'

function lireTheme() {
  try {
    return localStorage.getItem(CLE_THEME) === 'clair' ? 'clair' : 'sombre'
  } catch {
    return 'sombre'
  }
}

export function useTheme() {
  const [theme, setTheme] = useState(lireTheme)
  useEffect(() => {
    document.documentElement.classList.toggle('theme-clair', theme === 'clair')
    // La salle de jeux est affichée dans un cadre : on lui donne le même thème
    document.querySelectorAll('iframe.salle').forEach((cadre) => {
      cadre.contentDocument?.documentElement.classList.toggle('theme-clair', theme === 'clair')
    })
    try {
      localStorage.setItem(CLE_THEME, theme)
    } catch {
      // navigation privée : le choix ne sera pas gardé, tant pis
    }
  }, [theme])
  return [theme, () => setTheme(theme === 'clair' ? 'sombre' : 'clair')]
}

export function Marque() {
  return (
    <span className="nav-nom">
      compagnon<span>.stage</span>
    </span>
  )
}

export default function Coquille({ sections, page, allerA, qui, pied, actions, description, onDeconnexion, children }) {
  const [theme, changerTheme] = useTheme()
  const [tiroir, setTiroir] = useState(false) // sur téléphone, la navigation s'ouvre comme un tiroir
  const lien = sections.flatMap((s) => s.liens).find((l) => l.cle === page)

  function choisir(cle) {
    setTiroir(false)
    allerA(cle)
  }

  return (
    <div className={`appli ${tiroir ? 'nav-ouverte' : ''}`}>
      <div className="voile-nav" onClick={() => setTiroir(false)} />
      <nav className="nav" aria-label="Navigation">
        <div className="nav-marque">
          <span className="nav-logo"><Icone nom="boussole" /></span>
          <Marque />
        </div>
        {qui && <div className="nav-qui">{qui}</div>}
        <div className="nav-liens">
          {sections.map((s) => (
            <div key={s.titre}>
              <div className="nav-titre">{s.titre}</div>
              {s.liens.map((l) => (
                <button key={l.cle} className={`nav-lien ${page === l.cle ? 'actif' : ''}`} onClick={() => choisir(l.cle)}
                  aria-current={page === l.cle ? 'page' : undefined}>
                  <Icone nom={l.icone} />
                  {l.nom}
                  {l.badge > 0 && <span className="badge">{l.badge}</span>}
                </button>
              ))}
            </div>
          ))}
        </div>
        <div className="nav-pied">
          {pied}
          <button className="nav-lien" onClick={changerTheme}>
            <Icone nom={theme === 'clair' ? 'lune' : 'soleil'} />
            {theme === 'clair' ? 'Thème sombre' : 'Thème clair'}
          </button>
          <button className="nav-lien" onClick={onDeconnexion}>
            <Icone nom="sortie" />
            Quitter
          </button>
        </div>
      </nav>
      <div className="page">
        <header className="page-entete">
          <button className="bouton-menu carre" onClick={() => setTiroir(true)} aria-label="Ouvrir le menu">
            <Icone nom="menu" />
          </button>
          <span className="page-icone"><Icone nom={lien?.icone} taille={19} /></span>
          <div className="page-titres">
            <div className="page-titre">{lien?.titre || lien?.nom}</div>
            <div className="page-description">{description || lien?.description}</div>
          </div>
          <div className="page-actions">{actions}</div>
        </header>
        <main className={`page-contenu ${lien?.pleine ? 'pleine' : ''}`}>{children}</main>
      </div>
    </div>
  )
}
