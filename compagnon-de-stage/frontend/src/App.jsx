import { useEffect, useState } from 'react'
import { api, ecrireJeton, lireJeton, surDeconnexion } from './api.js'
import Connexion from './Connexion.jsx'
import Animateur from './animateur/Animateur.jsx'
import Stagiaire from './stagiaire/Stagiaire.jsx'

export default function App() {
  const [session, setSession] = useState(null) // { role, prenom }
  const [pret, setPret] = useState(false)

  useEffect(() => {
    surDeconnexion(() => setSession(null))
    if (!lireJeton()) {
      setPret(true)
      return
    }
    api('/session')
      .then(setSession)
      .catch(() => setSession(null))
      .finally(() => setPret(true))
  }, [])

  async function seDeconnecter() {
    try {
      await api('/deconnexion', { methode: 'POST' })
    } catch {
      // déjà déconnecté
    }
    ecrireJeton('')
    setSession(null)
  }

  if (!pret) return <p className="chargement">Chargement…</p>
  if (!session) return <Connexion onConnecte={setSession} />
  if (session.role === 'animateur') return <Animateur onDeconnexion={seDeconnecter} />
  return <Stagiaire prenom={session.prenom} onDeconnexion={seDeconnecter} />
}
