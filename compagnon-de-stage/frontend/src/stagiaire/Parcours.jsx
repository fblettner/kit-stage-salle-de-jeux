import { useEffect, useState } from 'react'
import { useApi } from '../api.js'
import Blocs from '../Blocs.jsx'
import { Frise, OngletsJours, trouverActivite } from '../Semaine.jsx'
import ZoneTexte from '../ZoneTexte.jsx'

const LIENS = {
  projet: ['🎮', 'Choisir mon projet', 'projet'],
  carnet: ['📓', 'Remplir mon carnet de bord', 'carnet'],
  bugs: ['🐞', 'Noter les bugs trouvés', 'bugs'],
}

export default function Parcours({ programme, moi, onCocher, onRepondre, allerA, activite, setActivite }) {
  const [jour, setJour] = useState(programme.jour_actuel ?? 0)
  const toutes = programme.jours.flatMap((j) => j.activites)
  const choisie = activite && programme.jours[jour].activites.some((a) => a.id === activite)
    ? activite
    : (programme.jours[jour].activites.find((a) => a.id === programme.activite_actuelle) || programme.jours[jour].activites[0]).id

  useEffect(() => {
    if (choisie !== activite) setActivite(choisie)
  }, [choisie, activite, setActivite])

  // Quand on change d'activité, on remonte en haut de la page
  useEffect(() => {
    document.querySelector('.page-contenu')?.scrollTo({ top: 0 })
  }, [choisie])

  // Ouvrir une activité, même si elle est un autre jour
  function ouvrir(id) {
    const a = trouverActivite(programme, id)
    if (!a) return
    setJour(a.jour)
    setActivite(id)
  }

  // « Reprendre où j'en étais » : la première activité pas terminée, jusqu'à aujourd'hui
  const dernierJour = programme.jour_actuel ?? 4
  const aReprendre = toutes.find((a) => a.jour <= dernierJour && !moi.avancement[a.id]?.fini)
  const suivante = toutes[toutes.findIndex((a) => a.id === choisie) + 1]

  function badge(a) {
    const av = moi.avancement[a.id]
    if (av?.fini) return <span className="fait">✓</span>
    if (av?.total) return <span className="compte">{av.coches}/{av.total}</span>
    return null
  }

  return (
    <div className="parcours">
      <div className="parcours-gauche">
        {aReprendre && aReprendre.id !== choisie && (
          <button className="reprendre" onClick={() => ouvrir(aReprendre.id)}>
            ▶ Reprendre où j'en étais : {aReprendre.titre}
          </button>
        )}
        <OngletsJours programme={programme} jour={jour} setJour={setJour} />
        <p className="theme">{programme.jours[jour].theme}</p>
        {programme.jour_actuel === null && jour === 0 && (
          <p className="discret petit">Le stage n'a pas encore commencé : tu peux déjà regarder le programme.</p>
        )}
        <Frise programme={programme} jour={jour} choisie={choisie} onChoisir={setActivite} badge={badge} />
      </div>
      <div className="parcours-droite">
        <DetailActivite id={choisie} moi={moi} onCocher={onCocher} onRepondre={onRepondre}
          allerA={allerA} suivante={suivante} ouvrir={ouvrir} />
      </div>
    </div>
  )
}

function DetailActivite({ id, moi, onCocher, onRepondre, allerA, suivante, ouvrir }) {
  // On recharge le contenu si le jeu choisi change ou si une surprise est déclenchée
  const version = encodeURIComponent(`${moi.jeu || ''}-${moi.dossier || ''}-${moi.surprises.join('.')}`)
  const { donnees, erreur } = useApi(`/activite/${id}?v=${version}`)
  if (erreur) return <p className="erreur">{erreur}</p>
  if (!donnees || donnees.activite.id !== id) return <p className="chargement">Chargement…</p>
  const a = donnees.activite
  const fini = !!moi.coches[`fini:${id}`]
  const cleBilan = `bilan-${a.jour}`

  return (
    <article className="activite carte">
      <p className="activite-heure">
        {a.debut} – {a.fin} · <span className={`mode mode-${a.mode}`}>{a.mode === 'perso' ? 'Sur mon jeu' : 'Tous ensemble'}</span>
      </p>
      <h2>{a.titre}</h2>
      <p className="activite-description">{a.description}</p>

      {donnees.phrase_depart && (
        <div className="astuce">
          💡 Commence toujours ta séance Claude par : <strong>{donnees.phrase_depart}</strong>
        </div>
      )}
      {moi.jeu && moi.dossier && moi.dossier !== moi.jeu && a.mode === 'perso' && (
        <div className="astuce">
          🏢 Vous êtes deux « agences concurrentes » sur le même jeu : ta version est dans le dossier{' '}
          <code>{moi.dossier}</code>. C'est déjà remplacé dans les prompts ci-dessous.
        </div>
      )}

      {donnees.manque_jeu && (
        <div className="encart">
          Pour cette activité, il faut d'abord choisir ton jeu.{' '}
          <button className="principal" onClick={() => allerA('projet')}>Choisir mon jeu</button>
        </div>
      )}
      {donnees.verrouille && (
        <div className="encart surprise">
          <div className="grand-emoji">🎭</div>
          <p>Le client prépare quelque chose… Cette partie s'affichera ici quand ton maître de stage la déclenchera.</p>
          <p className="discret">En attendant, continue tes finitions !</p>
        </div>
      )}

      {a.idees && (
        <div className="idees">
          <h3>📝 Ma liste d'améliorations</h3>
          <p className="discret petit">Une idée par ligne, la plus importante en premier. Raye (ou efface) celles qui sont faites.</p>
          <ZoneTexte cle="idees-finitions" valeur={moi.reponses['idees-finitions'] || ''} onRepondre={onRepondre} lignes={5}
            placeholder={'1. …\n2. …\n3. …'} />
        </div>
      )}

      <Blocs blocs={donnees.blocs} coches={moi.coches} onCocher={onCocher} />

      {a.lien && LIENS[a.lien] && (
        <button className="lien-onglet" onClick={() => allerA(LIENS[a.lien][2])}>
          {LIENS[a.lien][0]} {LIENS[a.lien][1]} →
        </button>
      )}

      {a.bilan && (
        <div className="bilan">
          <h3>📮 Mon bilan du jour, pour mon maître de stage</h3>
          <p className="discret petit">
            En 3 lignes : ce que j'ai réussi aujourd'hui, ce qui m'a bloqué, et ma question pour demain.
          </p>
          <ZoneTexte cle={cleBilan} valeur={moi.reponses[cleBilan] || ''} onRepondre={onRepondre} lignes={4}
            placeholder={"Aujourd'hui j'ai réussi à…\nJ'ai été bloqué par…\nMa question : …"} />
        </div>
      )}

      <label className={`termine ${fini ? 'oui' : ''}`}>
        <input type="checkbox" checked={fini} onChange={(e) => onCocher(`fini:${id}`, e.target.checked)} />
        {fini ? '✓ Activité terminée, bravo !' : "J'ai terminé cette activité"}
      </label>
      {fini && suivante && (
        <div className="suite">
          <button className="principal" onClick={() => ouvrir(suivante.id)}>
            Activité suivante : {suivante.titre} →
          </button>
        </div>
      )}
    </article>
  )
}
