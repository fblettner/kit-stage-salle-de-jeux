import { useState } from 'react'
import { api, useApi } from '../api.js'
import Blocs from '../Blocs.jsx'
import { copier } from '../Markdown.jsx'

export default function Documents() {
  const { donnees } = useApi('/animateur/documents')
  const [fichier, setFichier] = useState('00-LISEZ-MOI.md')
  const [claudeMd, setClaudeMd] = useState(null)
  const doc = useApi(fichier ? `/animateur/document?fichier=${encodeURIComponent(fichier)}` : null)
  const [copie, setCopie] = useState(false)

  async function voirClaudeMd() {
    setFichier(null)
    setClaudeMd(await api('/animateur/claude-md', { texte: true }))
  }

  function telecharger() {
    const url = URL.createObjectURL(new Blob([claudeMd], { type: 'text/markdown' }))
    const a = document.createElement('a')
    a.href = url
    a.download = 'CLAUDE.md'
    a.click()
    URL.revokeObjectURL(url)
  }

  if (!donnees) return <p className="chargement">Chargement…</p>
  const groupes = [...new Set(donnees.map((d) => d.groupe))]

  return (
    <div className="documents">
      <aside className="liste-docs">
        <button className={`doc-special ${fichier === null ? 'actif' : ''}`} onClick={voirClaudeMd}>
          ✨ CLAUDE.md du projet (rempli)
        </button>
        {groupes.map((g) => (
          <div key={g}>
            <h4>{g}</h4>
            {donnees.filter((d) => d.groupe === g).map((d) => (
              <button key={d.fichier} className={fichier === d.fichier ? 'actif' : ''}
                onClick={() => { setFichier(d.fichier); setClaudeMd(null) }}>
                {d.titre}
              </button>
            ))}
          </div>
        ))}
      </aside>
      <article className="carte doc-contenu">
        {fichier === null ? (
          claudeMd === null ? <p className="chargement">Chargement…</p> : (
            <>
              <h2>CLAUDE.md</h2>
              <p className="discret petit">
                La fiche de consignes pour Claude, avec les jeux et les dossiers choisis par les stagiaires. À mettre à la racine du projet.
              </p>
              <div className="boutons">
                <button className="principal" onClick={telecharger}>⬇️ Télécharger</button>
                <button className="secondaire" onClick={() => { copier(claudeMd); setCopie(true); setTimeout(() => setCopie(false), 1500) }}>
                  {copie ? '✓ Copié' : 'Copier'}
                </button>
              </div>
              <pre className="fichier-brut">{claudeMd}</pre>
            </>
          )
        ) : !doc.donnees || doc.donnees.fichier !== fichier ? (
          <p className="chargement">Chargement…</p>
        ) : (
          <>
            <p className="discret petit"><code>{doc.donnees.fichier}</code></p>
            <h2>{doc.donnees.titre}</h2>
            <Blocs blocs={doc.donnees.blocs} />
          </>
        )}
      </article>
    </div>
  )
}
