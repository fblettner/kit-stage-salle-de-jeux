import { useState } from 'react'
import { api, useApi } from '../api.js'
import Carnet from '../stagiaire/Carnet.jsx'

export default function Stagiaires({ programme, tableau, recharger }) {
  const [prenom, setPrenom] = useState('')
  const [erreur, setErreur] = useState('')
  const [detail, setDetail] = useState(null)
  const [fiches, setFiches] = useState(false)

  async function ajouter(e) {
    e.preventDefault()
    setErreur('')
    try {
      await api('/animateur/stagiaires', { methode: 'POST', corps: { prenom } })
      setPrenom('')
      recharger()
    } catch (err) {
      setErreur(err.message)
    }
  }

  async function modifier(id, corps) {
    try {
      await api(`/animateur/stagiaires/${id}`, { methode: 'PATCH', corps })
      recharger()
    } catch (err) {
      setErreur(err.message)
    }
  }

  async function nouveauCode(s) {
    if (!window.confirm(`Créer un nouveau code pour ${s.prenom} ? L'ancien ne marchera plus.`)) return
    await api(`/animateur/stagiaires/${s.id}/nouveau-code`, { methode: 'POST' })
    recharger()
  }

  async function supprimer(s) {
    if (!window.confirm(`Supprimer ${s.prenom} et tout ce qu'il ou elle a écrit ?`)) return
    await api(`/animateur/stagiaires/${s.id}`, { methode: 'DELETE' })
    if (detail === s.id) setDetail(null)
    recharger()
  }

  if (detail) {
    return <DetailStagiaire id={detail} programme={programme} onRetour={() => setDetail(null)} />
  }

  if (fiches) {
    return (
      <div className="fiches-acces">
        <div className="pas-imprime boutons">
          <button className="secondaire" onClick={() => setFiches(false)}>← Retour</button>
          <button className="principal" onClick={() => window.print()}>🖨️ Imprimer</button>
        </div>
        {tableau.stagiaires.map((s) => (
          <div key={s.id} className="fiche-acces carte">
            <h2>Bienvenue {s.prenom} !</h2>
            <p>Pendant ton stage, ton compagnon te guide jour après jour.</p>
            <p>Va sur <strong>{window.location.origin}</strong></p>
            <p>et entre ton code :</p>
            <p className="code-grand">{s.code}</p>
            <p className="discret petit">Garde ce code pour toi : il ouvre ton carnet de bord.</p>
          </div>
        ))}
      </div>
    )
  }

  return (
    <div className="stagiaires">
      <form className="ligne-formulaire" onSubmit={ajouter}>
        <input value={prenom} onChange={(e) => setPrenom(e.target.value)} placeholder="Prénom du stagiaire" maxLength={40} />
        <button className="principal" disabled={!prenom.trim()}>Ajouter</button>
      </form>
      <p className="discret petit">
        🔒 Seul le prénom est enregistré. Chaque stagiaire reçoit un code à 6 caractères pour se connecter.
        En fin de stage, pense à tout effacer (Réglages).
      </p>
      {erreur && <p className="erreur">{erreur}</p>}

      {tableau.stagiaires.length > 0 && (
        <>
          <div className="table-defilante">
            <table className="table-stagiaires">
              <thead>
                <tr>
                  <th>Prénom</th>
                  <th>Code</th>
                  <th>Jeu</th>
                  <th>Dossier</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {tableau.stagiaires.map((s) => (
                  <tr key={s.id}>
                    <td><strong>{s.prenom}</strong></td>
                    <td><code className="code">{s.code}</code></td>
                    <td>
                      <select value={s.jeu || ''} onChange={(e) => modifier(s.id, { jeu: e.target.value })}>
                        <option value="">— pas choisi —</option>
                        {Object.entries(programme.jeux).map(([cle, j]) => (
                          <option key={cle} value={cle}>{j.icone} {j.nom}</option>
                        ))}
                      </select>
                    </td>
                    <td>
                      <ChampDossier s={s} onValider={(dossier) => modifier(s.id, { dossier })} />
                    </td>
                    <td className="actions">
                      <button className="secondaire petit-bouton" onClick={() => setDetail(s.id)}>Voir son carnet</button>
                      <button className="discret-bouton" onClick={() => nouveauCode(s)}>Nouveau code</button>
                      <button className="discret-bouton danger" onClick={() => supprimer(s)}>Supprimer</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="boutons">
            <button className="secondaire" onClick={() => setFiches(true)}>🖨️ Fiches d'accès à imprimer</button>
          </div>
          <p className="discret petit">
            Le dossier est choisi automatiquement : le nom du jeu, ou <code>jeu_prénom</code> si deux stagiaires ont pris le même jeu
            (formule « deux agences concurrentes »). Pour la formule « une équipe, deux métiers », mets le même dossier aux deux
            (ex. <code>coach</code>).
          </p>
        </>
      )}
    </div>
  )
}

function ChampDossier({ s, onValider }) {
  const [valeur, setValeur] = useState(s.dossier_auto ? '' : s.dossier || '')
  return (
    <input
      className="champ-dossier"
      value={valeur}
      placeholder={s.dossier_auto ? `${s.dossier || '—'} (auto)` : ''}
      onChange={(e) => setValeur(e.target.value.toLowerCase().replace(/[^a-z0-9_]/g, ''))}
      onBlur={() => valeur !== (s.dossier_auto ? '' : s.dossier) && onValider(valeur)}
      title="Laisse vide pour le choix automatique"
    />
  )
}

function DetailStagiaire({ id, programme, onRetour }) {
  const { donnees } = useApi(`/animateur/stagiaires/${id}`, { toutesLes: 20 })
  if (!donnees) return <p className="chargement">Chargement…</p>
  const s = donnees
  const jeu = s.jeu ? programme.jeux[s.jeu] : null

  return (
    <div className="detail-stagiaire">
      <div className="boutons pas-imprime">
        <button className="secondaire" onClick={onRetour}>← Tous les stagiaires</button>
        <button className="secondaire" onClick={() => window.print()}>🖨️ Imprimer le carnet</button>
      </div>
      <section className="carte pas-imprime">
        <h3>Avancement</h3>
        <div className="avancement-jours">
          {programme.jours.map((j) => (
            <div key={j.index}>
              <strong>{j.nom}</strong>
              <ul>
                {j.activites.map((a) => {
                  const av = s.avancement[a.id]
                  return (
                    <li key={a.id} className={av.fini ? 'fini' : ''}>
                      {av.fini ? '✓' : '·'} {a.titre}
                      {av.total > 0 && <span className="discret"> ({av.coches}/{av.total})</span>}
                    </li>
                  )
                })}
              </ul>
            </div>
          ))}
        </div>
        {programme.jours.some((j) => s.reponses[`bilan-${j.index}`]) && (
          <>
            <h4>Ses bilans du jour</h4>
            {programme.jours.filter((j) => s.reponses[`bilan-${j.index}`]).map((j) => (
              <p key={j.index} className="reponse-lue"><strong>{j.nom} :</strong> {s.reponses[`bilan-${j.index}`]}</p>
            ))}
          </>
        )}
        {s.reponses['idees-finitions'] && (
          <>
            <h4>Sa liste d'améliorations</h4>
            <p className="reponse-lue">{s.reponses['idees-finitions']}</p>
          </>
        )}
      </section>
      {(s.bugs.trouves.length > 0 || s.bugs.recus.length > 0) && (
        <section className="carte pas-imprime">
          <h3>Bugs</h3>
          <p className="petit">
            Trouvés chez les autres : {s.bugs.trouves.length} · Reçus dans son jeu : {s.bugs.recus.length} (
            {s.bugs.recus.filter((b) => b.corrige).length} corrigés)
          </p>
        </section>
      )}
      <Carnet moi={s} prenom={s.prenom} jeu={jeu} lectureSeule />
    </div>
  )
}
