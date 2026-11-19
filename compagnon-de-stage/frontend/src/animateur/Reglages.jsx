import { useEffect, useState } from 'react'
import { api } from '../api.js'

export default function Reglages({ programme, tableau, recharger }) {
  const r = tableau.reglages
  const [confirmation, setConfirmation] = useState('')
  const [message, setMessage] = useState('')
  const [erreur, setErreur] = useState('')

  async function changer(corps) {
    setErreur('')
    try {
      await api('/animateur/reglages', { methode: 'PUT', corps })
      recharger()
    } catch {
      setErreur("Ce réglage n'a pas été enregistré : vérifie ce que tu as écrit (une adresse doit commencer par https://, une adresse Git ne contient pas d'espace).")
    }
  }

  async function effacer() {
    try {
      await api('/animateur/effacer-tout', { methode: 'POST', corps: { confirmation } })
      setConfirmation('')
      setMessage('✓ Tout est effacé.')
      recharger()
    } catch (e) {
      setMessage(e.message)
    }
  }

  return (
    <div className="reglages">
      {erreur && <p className="erreur">{erreur}</p>}
      <section className="carte">
        <div className="titre-carte">Ce que voient les stagiaires</div>
        <p className="petit">
          Chaque activité affiche aux stagiaires un <strong>pas-à-pas écrit pour eux</strong> (bouton « Écran des élèves » dans
          Le programme), et la page « Je suis bloqué » les aide à se dépanner seuls. Ces réglages complètent leurs écrans.
          Détails : <code>guides/autonomie-des-eleves.md</code> (onglet Documents).
        </p>
        <Champ nom="Le mot du jour, affiché en haut de leur journée" valeur={r.message} onValider={(v) => changer({ message: v })} lignes={3}
          placeholder="Ex. : Bravo pour hier ! Ce matin, pensez à faire un commit après chaque prompt qui marche." />
        <Champ nom="L'adresse du dépôt Git du projet (pour mardi midi et la fusion)" valeur={r.url_depot} onValider={(v) => changer({ url_depot: v })}
          placeholder="git@github.com:toi/salle-de-jeux.git" aide="Un dépôt privé et vide, créé avant le stage. Elle est recopiée dans leurs commandes." />
      </section>
      <section className="carte">
        <div className="titre-carte">Le calendrier</div>
        <label>
          Date du lundi (premier jour du stage)
          <input type="date" value={r.date_debut} onChange={(e) => changer({ date_debut: e.target.value })} />
        </label>
        <label>
          Jour affiché
          <select value={r.jour_force} onChange={(e) => changer({ jour_force: e.target.value })}>
            <option value="">Automatique (selon la date)</option>
            {programme.jours.map((j) => <option key={j.index} value={String(j.index)}>Forcer : {j.nom}</option>)}
          </select>
        </label>
        <p className="discret petit">
          Aujourd'hui pour l'appli : {programme.jour_actuel === null ? 'hors stage' : programme.jours[programme.jour_actuel].nom}.
          Forcer un jour sert pour la répétition générale, ou si le programme a pris du retard.
        </p>
      </section>
      <section className="carte">
        <div className="titre-carte">Le choix des jeux</div>
        <label className="case">
          <input type="checkbox" checked={r.choix_verrouille} onChange={(e) => changer({ choix_verrouille: e.target.checked })} />
          Valider les choix : les stagiaires ne peuvent plus changer de jeu (toi, tu peux toujours, dans « Stagiaires »)
        </label>
      </section>
      <section className="carte danger-zone">
        <div className="titre-carte">Fin du stage : tout effacer</div>
        <p className="petit">
          Efface les stagiaires, leurs codes, leurs carnets, leurs demandes d'aide et leurs bugs. Pense à imprimer les carnets avant !
        </p>
        <div className="ligne-formulaire">
          <input value={confirmation} onChange={(e) => setConfirmation(e.target.value)} placeholder="Écris EFFACER" />
          <button className="danger" disabled={confirmation !== 'EFFACER'} onClick={effacer}>Tout effacer</button>
        </div>
        {message && <p className="petit">{message}</p>}
      </section>
    </div>
  )
}

// Un champ de texte qui s'enregistre quand on en sort (pas à chaque lettre)
function Champ({ nom, valeur, onValider, placeholder, aide, lignes = 0 }) {
  const [texte, setTexte] = useState(valeur)
  useEffect(() => setTexte(valeur), [valeur])
  const proprietes = {
    value: texte,
    placeholder,
    onChange: (e) => setTexte(e.target.value),
    onBlur: () => texte.trim() !== valeur && onValider(texte.trim()),
  }
  return (
    <label>
      {nom}
      {lignes ? <textarea rows={lignes} maxLength={1000} {...proprietes} /> : <input maxLength={300} {...proprietes} />}
      {aide && <span className="aide-champ">{aide}</span>}
    </label>
  )
}
