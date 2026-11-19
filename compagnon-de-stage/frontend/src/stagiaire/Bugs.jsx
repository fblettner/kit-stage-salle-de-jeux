import { useState } from 'react'
import { api } from '../api.js'

export default function Bugs({ moi, recharger, jeux }) {
  const autres = moi.autres
  const [cible, setCible] = useState(autres[0]?.id ?? '')
  const [champs, setChamps] = useState({ action: '', resultat: '', attendu: '' })
  const [erreur, setErreur] = useState('')

  async function envoyer(e) {
    e.preventDefault()
    setErreur('')
    try {
      await api('/moi/bugs', { methode: 'POST', corps: { cible_id: Number(cible), ...champs } })
      setChamps({ action: '', resultat: '', attendu: '' })
      recharger()
    } catch (err) {
      setErreur(err.message)
    }
  }

  async function corrige(id, valeur) {
    await api(`/moi/bugs/${id}`, { methode: 'PUT', corps: { corrige: valeur } })
    recharger()
  }

  async function supprimer(id) {
    await api(`/moi/bugs/${id}`, { methode: 'DELETE' })
    recharger()
  }

  const nomJeu = (s) => (s?.jeu ? `${jeux[s.jeu].icone} ${jeux[s.jeu].nom}` : 'jeu pas choisi')

  return (
    <div className="bugs">
      <p className="discret">
        Un testeur décrit un bug pour que le développeur puisse le <strong>reproduire</strong> : qu'est-ce que j'ai fait,
        qu'est-ce qui s'est passé, qu'est-ce qui aurait dû se passer.
      </p>
      {autres.length === 0 ? (
        <p className="encart">Il n'y a pas encore d'autre stagiaire inscrit.</p>
      ) : (
        <form className="carte formulaire-bug" onSubmit={envoyer}>
          <label>
            Le jeu que je teste
            <select value={cible} onChange={(e) => setCible(e.target.value)}>
              {autres.map((a) => (
                <option key={a.id} value={a.id}>{a.prenom} · {nomJeu(a)}</option>
              ))}
            </select>
          </label>
          <label>
            Ce que j'ai fait
            <textarea rows={2} value={champs.action} onChange={(e) => setChamps({ ...champs, action: e.target.value })}
              placeholder="Ex. : j'ai cliqué très vite deux fois sur « Tirer »" />
          </label>
          <label>
            Ce qui s'est passé
            <textarea rows={2} value={champs.resultat} onChange={(e) => setChamps({ ...champs, resultat: e.target.value })}
              placeholder="Ex. : le ballon est parti deux fois et le score a compté 2 buts" />
          </label>
          <label>
            Ce qui aurait dû se passer
            <textarea rows={2} value={champs.attendu} onChange={(e) => setChamps({ ...champs, attendu: e.target.value })}
              placeholder="Ex. : un seul tir, le deuxième clic ne fait rien" />
          </label>
          {erreur && <p className="erreur">{erreur}</p>}
          <button className="principal" disabled={!champs.action || !champs.resultat || !champs.attendu}>Signaler ce bug</button>
        </form>
      )}

      <h3>Les bugs trouvés dans MON jeu ({moi.bugs.recus.filter((b) => !b.corrige).length} à corriger)</h3>
      {moi.bugs.recus.length === 0 && <p className="discret">Aucun pour l'instant… 😎</p>}
      {moi.bugs.recus.map((b) => (
        <FicheBug key={b.id} b={b} entete={`Trouvé par ${b.auteur}`}>
          <CaseCorrige b={b} onChange={(v) => corrige(b.id, v)} />
        </FicheBug>
      ))}
      {moi.bugs.recus.some((b) => !b.corrige) && (
        <p className="astuce">
          💡 Pour corriger un bug avec Claude, copie-lui les trois lignes du bug et demande-lui d'abord
          d'<strong>expliquer la cause</strong>, puis d'ajouter un test qui vérifie que le bug ne revient pas.
        </p>
      )}

      <h3>Les bugs que j'ai trouvés ({moi.bugs.trouves.length})</h3>
      {moi.bugs.trouves.map((b) => (
        <FicheBug key={b.id} b={b} entete={`Dans le jeu de ${b.cible}`}>
          {!b.corrige && <button className="discret-bouton" onClick={() => supprimer(b.id)}>Retirer</button>}
        </FicheBug>
      ))}
    </div>
  )
}

function CaseCorrige({ b, onChange }) {
  // On coche tout de suite à l'écran, sans attendre la réponse du serveur
  const [coche, setCoche] = useState(b.corrige)
  return (
    <label className="petit">
      <input type="checkbox" checked={coche} onChange={(e) => { setCoche(e.target.checked); onChange(e.target.checked) }} /> Corrigé
    </label>
  )
}

function FicheBug({ b, entete, children }) {
  return (
    <div className={`fiche-bug carte ${b.corrige ? 'corrige' : ''}`}>
      <div className="fiche-bug-entete">
        <span>{b.corrige ? '✅' : '🐞'} {entete}</span>
        {children}
      </div>
      <dl>
        <dt>J'ai fait</dt><dd>{b.action}</dd>
        <dt>Il s'est passé</dt><dd>{b.resultat}</dd>
        <dt>Il aurait fallu</dt><dd>{b.attendu}</dd>
      </dl>
    </div>
  )
}
