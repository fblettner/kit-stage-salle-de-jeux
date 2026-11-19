import { useEffect, useRef, useState } from 'react'

// Une zone de texte qui s'enregistre toute seule (un peu après qu'on a fini de taper).
export default function ZoneTexte({ cle, valeur = '', onRepondre, lignes = 3, placeholder = '', uneLigne = false, prefixe = '' }) {
  const [texte, setTexte] = useState(valeur)
  const [etat, setEtat] = useState('') // '', 'attente', 'ok', 'erreur'
  const minuteur = useRef(null)
  const dernierEnvoye = useRef(valeur)

  // Si la valeur change ailleurs (rechargement) et qu'on n'est pas en train de taper
  useEffect(() => {
    if (etat !== 'attente' && valeur !== dernierEnvoye.current) {
      setTexte(valeur)
      dernierEnvoye.current = valeur
    }
  }, [valeur, etat])

  useEffect(() => () => clearTimeout(minuteur.current), [])

  function changer(v) {
    setTexte(v)
    setEtat('attente')
    clearTimeout(minuteur.current)
    minuteur.current = setTimeout(() => envoyer(v), 800)
  }

  async function envoyer(v) {
    try {
      await onRepondre(cle, v)
      dernierEnvoye.current = v
      setEtat('ok')
    } catch {
      setEtat('erreur')
    }
  }

  const statut = { attente: '…', ok: '✓ Enregistré', erreur: '⚠️ Pas enregistré, réessaie' }[etat] || ''
  return (
    <div className="zone-texte">
      {uneLigne ? (
        <div className="avec-prefixe">
          {prefixe && <span>{prefixe}</span>}
          <input value={texte} onChange={(e) => changer(e.target.value)} placeholder={placeholder} maxLength={5000} />
        </div>
      ) : (
        <textarea
          rows={lignes}
          value={texte}
          onChange={(e) => changer(e.target.value)}
          placeholder={placeholder}
          maxLength={5000}
        />
      )}
      <span className={`statut statut-${etat}`}>{statut}</span>
    </div>
  )
}
