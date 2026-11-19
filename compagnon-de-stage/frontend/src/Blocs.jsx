import { useState } from 'react'
import Markdown, { copier } from './Markdown.jsx'

// Affiche le contenu d'une activité : texte, prompts à copier, code, cases « Ce qu'on vérifie »,
// fichier à télécharger, partie repliée.
// - coches : { cle: true/false } ; onCocher(cle, fait) : si absent, les cases sont en lecture seule
export default function Blocs({ blocs, coches = {}, onCocher }) {
  let numeroPrompt = 0
  return (
    <div className="blocs">
      {blocs.map((b, i) => {
        if (b.type === 'md') return <Markdown key={i} texte={b.texte} />
        if (b.type === 'prompt') {
          numeroPrompt += 1
          return <Prompt key={i} texte={b.texte} numero={numeroPrompt} secret={b.secret} />
        }
        if (b.type === 'code')
          return (
            <Markdown key={i} texte={'```' + b.langage + '\n' + b.texte + '\n```'} />
          )
        if (b.type === 'verif') return <Verif key={i} bloc={b} coches={coches} onCocher={onCocher} />
        if (b.type === 'fichier') return <Fichier key={i} nom={b.nom} texte={b.texte} />
        if (b.type === 'repli')
          return (
            <details key={i} className="repli">
              <summary>{b.titre}</summary>
              <Blocs blocs={b.blocs} coches={coches} onCocher={onCocher} />
            </details>
          )
        return null
      })}
    </div>
  )
}

function BoutonCopier({ texte }) {
  const [copie, setCopie] = useState(false)
  return (
    <button
      className={copie ? 'copie' : ''}
      onClick={() => {
        copier(texte)
        setCopie(true)
        setTimeout(() => setCopie(false), 1800)
      }}
    >
      {copie ? '✓ Copié !' : 'Copier'}
    </button>
  )
}

function Prompt({ texte, numero, secret }) {
  // Un prompt « secret » (le rôle du client, avec ses réponses) se copie sans se lire
  const [visible, setVisible] = useState(!secret)
  const aCompleter = /\[[^\]]*[A-ZÉ]{3,}[^\]]*\]/.test(texte)
  return (
    <div className={`prompt ${secret ? 'secret' : ''}`}>
      <div className="prompt-entete">
        <span>{secret ? '🤫 Prompt secret — copie-le sans le lire' : `💬 Prompt ${numero} — à coller dans Claude`}</span>
        <BoutonCopier texte={texte} />
      </div>
      {visible ? (
        <pre>{texte}</pre>
      ) : (
        <p className="prompt-cache">
          Ce prompt contient les réponses : le lire, c'est regarder la fin du film avant le début.{' '}
          <button className="lien" onClick={() => setVisible(true)}>Le montrer quand même (après l'activité)</button>
        </p>
      )}
      {aCompleter && visible && <p className="prompt-note">✏️ Remplace ce qui est entre [CROCHETS] avant d'envoyer.</p>}
    </div>
  )
}

function Fichier({ nom, texte }) {
  function telecharger() {
    const url = URL.createObjectURL(new Blob([texte], { type: 'text/markdown' }))
    const a = document.createElement('a')
    a.href = url
    a.download = nom
    a.click()
    URL.revokeObjectURL(url)
  }
  return (
    <div className="fichier">
      <span className="fichier-nom">📄 {nom}</span>
      <button className="principal" onClick={telecharger}>⬇️ Télécharger</button>
      <details>
        <summary>Voir le contenu</summary>
        <pre className="fichier-brut">{texte}</pre>
      </details>
    </div>
  )
}

function Verif({ bloc, coches, onCocher }) {
  const faits = bloc.items.filter((it) => coches[it.cle]).length
  return (
    <div className="verif">
      <div className="verif-entete">
        <span>✅ {bloc.titre}</span>
        <span className="pastille">
          {faits}/{bloc.items.length}
        </span>
      </div>
      <ul>
        {bloc.items.map((it) => (
          <li key={it.cle}>
            <label className={coches[it.cle] ? 'coche' : ''}>
              <input
                type="checkbox"
                checked={!!coches[it.cle]}
                disabled={!onCocher}
                onChange={(e) => onCocher?.(it.cle, e.target.checked)}
              />
              <Markdown texte={it.texte} className="en-ligne" />
            </label>
          </li>
        ))}
      </ul>
    </div>
  )
}
