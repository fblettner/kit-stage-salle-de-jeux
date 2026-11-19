import { useState } from 'react'
import { api, ecrireJeton } from './api.js'
import { useTheme } from './Coquille.jsx'
import Icone from './Icone.jsx'

export default function Connexion({ onConnecte }) {
  useTheme() // applique le thème choisi la dernière fois
  const [mode, setMode] = useState('stagiaire')
  const [valeur, setValeur] = useState('')
  const [erreur, setErreur] = useState('')
  const [envoi, setEnvoi] = useState(false)

  async function valider(e) {
    e.preventDefault()
    setErreur('')
    setEnvoi(true)
    try {
      const r =
        mode === 'stagiaire'
          ? await api('/connexion/stagiaire', { methode: 'POST', corps: { code: valeur } })
          : await api('/connexion/animateur', { methode: 'POST', corps: { mot_de_passe: valeur } })
      ecrireJeton(r.jeton)
      onConnecte({ role: r.role, prenom: r.prenom })
    } catch (err) {
      setErreur(err.message)
    } finally {
      setEnvoi(false)
    }
  }

  function changerMode(m) {
    setMode(m)
    setValeur('')
    setErreur('')
  }

  return (
    <main className="connexion">
      <div className="connexion-carte">
        <div className="connexion-marque">
          <span className="connexion-logo"><Icone nom="boussole" taille={22} /></span>
          <h1>compagnon<span>.stage</span></h1>
        </div>
        <p className="discret petit">La salle de jeux · stage d'observation de 3e</p>
        <div className="onglets-mini segments">
          <button type="button" className={mode === 'stagiaire' ? 'actif' : ''} onClick={() => changerMode('stagiaire')}>
            Je suis stagiaire
          </button>
          <button type="button" className={mode === 'animateur' ? 'actif' : ''} onClick={() => changerMode('animateur')}>
            Maître de stage
          </button>
        </div>
        <form onSubmit={valider}>
          {mode === 'stagiaire' ? (
            <label>
              Mon code (6 lettres ou chiffres)
              <input
                className="code-saisie"
                value={valeur}
                onChange={(e) => setValeur(e.target.value.toUpperCase())}
                maxLength={8}
                autoComplete="off"
                autoCapitalize="characters"
                placeholder="K7PM3Q"
                autoFocus
              />
            </label>
          ) : (
            <label>
              Mot de passe
              <input type="password" value={valeur} onChange={(e) => setValeur(e.target.value)} autoFocus />
            </label>
          )}
          {erreur && <p className="erreur">{erreur}</p>}
          <button className="principal large" disabled={!valeur || envoi}>
            {envoi ? 'Connexion…' : 'Entrer'}
          </button>
        </form>
      </div>
    </main>
  )
}
