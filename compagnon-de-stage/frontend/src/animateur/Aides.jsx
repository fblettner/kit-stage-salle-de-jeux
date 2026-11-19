import { useState } from 'react'
import { api, useApi } from '../api.js'
import { trouverActivite } from '../Semaine.jsx'

const REPONSES_RAPIDES = [
  "J'arrive dans 5 minutes !",
  "Copie le message d'erreur complet à Claude et demande-lui d'expliquer la cause avant de corriger.",
  'As-tu enregistré le fichier et relancé le serveur (Ctrl+C puis fastapi dev) ?',
  "Regarde la console du navigateur (F12) : qu'est-ce qui est écrit en rouge ?",
]

export default function Aides({ programme, recharger }) {
  const { donnees, recharger: rechargerAides } = useApi('/animateur/aides', { toutesLes: 10 })
  if (!donnees) return <p className="chargement">Chargement…</p>

  const ouvertes = donnees.filter((a) => a.statut !== 'resolue')
  const resolues = donnees.filter((a) => a.statut === 'resolue')
  const maj = () => {
    rechargerAides()
    recharger()
  }

  return (
    <div className="aides">
      {!ouvertes.length && <p className="encart">Aucune demande en attente. Les stagiaires se débrouillent ! 🎉</p>}
      {ouvertes.map((a) => <Demande key={a.id} a={a} programme={programme} maj={maj} />)}
      {resolues.length > 0 && (
        <details>
          <summary>Demandes réglées ({resolues.length})</summary>
          {resolues.map((a) => <Demande key={a.id} a={a} programme={programme} maj={maj} />)}
        </details>
      )}
    </div>
  )
}

function Demande({ a, programme, maj }) {
  const [reponse, setReponse] = useState(a.reponse)
  const act = trouverActivite(programme, a.activite)
  const heure = new Date(a.cree_le).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })

  async function envoyer(texte) {
    await api(`/animateur/aides/${a.id}`, { methode: 'PATCH', corps: { reponse: texte } })
    maj()
  }

  async function statut(s) {
    await api(`/animateur/aides/${a.id}`, { methode: 'PATCH', corps: { statut: s } })
    maj()
  }

  return (
    <div className={`demande carte ${a.statut}`}>
      <div className="demande-entete">
        <strong>{a.prenom}</strong>
        <span className="discret petit">{heure} · {act ? act.titre : 'autre'}</span>
        <span className={`statut-aide ${a.statut}`}>{{ ouverte: 'En attente', repondue: 'Répondu', resolue: 'Réglé' }[a.statut]}</span>
      </div>
      <p className="demande-message">{a.message}</p>
      {a.statut !== 'resolue' && (
        <>
          <div className="reponses-rapides">
            {REPONSES_RAPIDES.map((r) => (
              <button key={r} className="puce" onClick={() => setReponse(r)}>{r.length > 40 ? r.slice(0, 38) + '…' : r}</button>
            ))}
          </div>
          <textarea rows={2} value={reponse} onChange={(e) => setReponse(e.target.value)} placeholder="Ta réponse (le stagiaire la verra sur son écran)" />
          <div className="boutons">
            <button className="principal" disabled={!reponse.trim()} onClick={() => envoyer(reponse)}>Répondre</button>
            <button className="secondaire" onClick={() => statut('resolue')}>✓ Réglé (j'y suis allé)</button>
          </div>
        </>
      )}
      {a.statut === 'resolue' && a.reponse && <p className="petit discret">Réponse : {a.reponse}</p>}
    </div>
  )
}
