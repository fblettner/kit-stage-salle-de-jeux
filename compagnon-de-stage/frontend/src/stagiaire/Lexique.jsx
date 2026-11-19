import { useState } from 'react'
import { useApi } from '../api.js'
import Markdown from '../Markdown.jsx'

export default function Lexique() {
  const { donnees } = useApi('/lexique')
  const [filtre, setFiltre] = useState('')
  if (!donnees) return <p className="chargement">Chargement…</p>
  const f = filtre.toLowerCase()
  const mots = donnees.filter((m) => !f || (m.mot + m.definition).toLowerCase().includes(f))
  return (
    <div className="lexique">
      <input className="recherche" placeholder="Chercher un mot (API, branche, simulation…)" value={filtre} onChange={(e) => setFiltre(e.target.value)} />
      <dl>
        {mots.map((m) => (
          <div key={m.mot} className="mot carte">
            <dt>{m.mot}</dt>
            <dd>
              <Markdown texte={m.definition} className="en-ligne" />
              {m.souvenir && <span className="souvenir">💡 {m.souvenir}</span>}
            </dd>
          </div>
        ))}
      </dl>
      {!mots.length && <p className="discret">Aucun mot trouvé. Demande à Claude de te l'expliquer !</p>}
    </div>
  )
}
