import { useState } from 'react'
import { api, useApi } from '../api.js'
import Blocs from '../Blocs.jsx'
import { Frise, OngletsJours } from '../Semaine.jsx'

// « il y a 3 min » à partir d'une date envoyée par le serveur
function depuis(dateIso) {
  if (!dateIso) return { enLigne: false, texte: 'jamais connecté' }
  const minutes = Math.max(0, Math.round((Date.now() - new Date(dateIso).getTime()) / 60000))
  if (minutes < 2) return { enLigne: true, texte: 'en ligne' }
  if (minutes < 60) return { enLigne: false, texte: `vu il y a ${minutes} min` }
  if (minutes < 60 * 24) return { enLigne: false, texte: `vu il y a ${Math.round(minutes / 60)} h` }
  return { enLigne: false, texte: `vu le ${new Date(dateIso).toLocaleDateString('fr-FR')}` }
}

export default function Journee({ programme, tableau, recharger, allerA }) {
  const [jour, setJour] = useState(programme.jour_actuel ?? 0)
  const [choix, setChoix] = useState(null)
  const activites = programme.jours[jour].activites
  const choisie = activites.some((a) => a.id === choix)
    ? choix
    : (activites.find((a) => a.id === programme.activite_actuelle) || activites[0]).id
  const stagiaires = tableau.stagiaires

  function badge(a) {
    if (!stagiaires.length) return null
    return (
      <span className="mini-suivi">
        {stagiaires.map((s) => {
          const av = s.avancement[a.id]
          const etat = av.fini ? 'fini' : av.coches ? 'encours' : ''
          return (
            <span key={s.id} className={`initiale ${etat}`} title={`${s.prenom} : ${av.fini ? 'terminé' : av.total ? `${av.coches}/${av.total}` : '—'}`}>
              {s.prenom[0]}
            </span>
          )
        })}
      </span>
    )
  }

  return (
    <div className="journee">
      {programme.jour_actuel === null && (
        <p className="encart petit">
          📅 Le stage n'est pas en cours aujourd'hui. Indique la date de début dans <button className="lien" onClick={() => allerA('reglages')}>Réglages</button> pour
          que l'appli suive la journée toute seule.
        </p>
      )}
      <Bandeau stagiaires={stagiaires} programme={programme} allerA={allerA} />
      <div className="parcours">
        <div className="parcours-gauche">
          <OngletsJours programme={programme} jour={jour} setJour={setJour} />
          <p className="theme">{programme.jours[jour].theme}</p>
          <Frise programme={programme} jour={jour} choisie={choisie} onChoisir={setChoix} badge={badge} />
        </div>
        <div className="parcours-droite">
          <DetailAnimateur key={choisie} id={choisie} programme={programme} stagiaires={stagiaires} recharger={recharger} />
        </div>
      </div>
    </div>
  )
}

function Bandeau({ stagiaires, programme, allerA }) {
  if (!stagiaires.length)
    return (
      <div className="encart">
        👋 Commence par créer les comptes des stagiaires.{' '}
        <button className="principal" onClick={() => allerA('stagiaires')}>Ajouter les stagiaires</button>
      </div>
    )
  return (
    <div className="bandeau">
      {stagiaires.map((s) => {
        const jeu = s.jeu ? programme.jeux[s.jeu] : null
        const finies = Object.values(s.avancement).filter((a) => a.fini).length
        const presence = depuis(s.vu_le)
        // Le bilan le plus récent (bilan-0 = lundi … bilan-4 = vendredi)
        const dernierBilan = Object.keys(s.bilans).sort().pop()
        return (
          <div key={s.id} className="bandeau-stagiaire carte">
            <div className="bandeau-nom">
              <strong>
                <span className={`point-presence ${presence.enLigne ? 'en-ligne' : ''}`} title={presence.texte} />
                {s.prenom}
              </strong>
              {s.aides_ouvertes > 0 && <button className="badge rouge" onClick={() => allerA('aides')}>🆘 {s.aides_ouvertes}</button>}
            </div>
            <div className="discret petit">
              {jeu ? `${jeu.icone} ${jeu.nom}` : 'pas de jeu choisi'}
              {s.dossier && s.dossier !== s.jeu && <> · <code>{s.dossier}</code></>}
            </div>
            <div className="petit">
              {finies} activité{finies > 1 ? 's' : ''} terminée{finies > 1 ? 's' : ''} · <span className="discret">{presence.texte}</span>
            </div>
            {dernierBilan && (
              <p className="bandeau-bilan" title={s.bilans[dernierBilan]}>
                <span className="discret">📮 Bilan de {programme.jours[Number(dernierBilan.split('-')[1])]?.nom.toLowerCase()} : </span>
                {s.bilans[dernierBilan]}
              </p>
            )}
          </div>
        )
      })}
    </div>
  )
}

function DetailAnimateur({ id, programme, stagiaires, recharger }) {
  const jeuxChoisis = [...new Set(stagiaires.map((s) => s.jeu).filter(Boolean))]
  const tousLesJeux = Object.keys(programme.jeux)
  const [jeu, setJeu] = useState(jeuxChoisis[0] || tousLesJeux[0])
  const activite = programme.jours.flatMap((j) => j.activites).find((a) => a.id === id)
  const perso = activite.mode === 'perso'
  const { donnees, erreur } = useApi(perso ? `/activite/${id}?jeu=${jeu}` : `/activite/${id}`)
  const [vue, setVue] = useState('fiche') // 'fiche' (la mienne) ou 'eleves' (le pas-à-pas qu'ils lisent)
  const aUnGuide = donnees?.guide?.length > 0

  async function surprise(active, stagiaireId = null) {
    await api('/animateur/surprises', { methode: 'POST', corps: { activite: id, active, stagiaire_id: stagiaireId } })
    recharger()
  }

  return (
    <article className="activite carte">
      <p className="activite-heure">
        {activite.debut} – {activite.fin} ·{' '}
        <span className={`mode mode-${activite.mode}`}>{perso ? 'Chacun sur son jeu' : 'Tous ensemble'}</span>
      </p>
      <h2>{activite.titre}</h2>
      <p className="vu-par-eleves">
        <span className="discret petit">Le résumé affiché aux stagiaires :</span> {activite.description}
      </p>

      {activite.surprise && (
        <div className="encart surprise">
          <h3>🎭 Déclencher la surprise</h3>
          <p className="petit">Quand tu as joué la scène du client, rends la demande visible sur l'écran des stagiaires.</p>
          <div className="boutons">
            <button className="principal" onClick={() => surprise(true)}>Déclencher pour tous</button>
            {stagiaires.map((s) => {
              const ok = s.surprises.includes(id)
              return (
                <button key={s.id} className={ok ? 'choisi-bouton' : 'secondaire'} onClick={() => surprise(!ok, s.id)}>
                  {ok ? `✓ ${s.prenom} (annuler)` : s.prenom}
                </button>
              )
            })}
          </div>
        </div>
      )}

      {perso && stagiaires.length > 0 && (
        <div className="suivi-activite">
          {stagiaires.map((s) => {
            const av = s.avancement[id]
            return (
              <span key={s.id} className={`suivi ${av.fini ? 'fini' : ''}`}>
                {s.prenom} : {av.fini ? '✓ terminé' : av.total ? `${av.coches}/${av.total} vérifications` : 'en cours'}
              </span>
            )
          })}
        </div>
      )}

      {perso && (
        <div className="choix-jeu">
          {tousLesJeux.map((j) => (
            <button key={j} className={`${jeu === j ? 'actif' : ''} ${jeuxChoisis.includes(j) ? 'choisi' : 'pas-choisi'}`} onClick={() => setJeu(j)}>
              {programme.jeux[j].icone} {programme.jeux[j].nom}
            </button>
          ))}
        </div>
      )}

      {aUnGuide && (
        <div className="vue-fiche">
          <div className="segments" role="group" aria-label="Quelle fiche afficher">
            <button className={vue === 'fiche' ? 'actif' : ''} onClick={() => setVue('fiche')}>Ma fiche d'animateur</button>
            <button className={vue === 'eleves' ? 'actif violet' : ''} onClick={() => setVue('eleves')}>Écran des élèves</button>
          </div>
        </div>
      )}

      {erreur && <p className="erreur">{erreur}</p>}
      {!donnees ? (
        !erreur && <p className="chargement">Chargement…</p>
      ) : aUnGuide && vue === 'eleves' ? (
        <Blocs blocs={donnees.guide} />
      ) : donnees.blocs.length ? (
        <>
          {donnees.phrase_depart && (
            <div className="astuce">💡 Phrase de départ pour Claude : <strong>{donnees.phrase_depart}</strong></div>
          )}
          <Blocs blocs={donnees.blocs} />
        </>
      ) : (
        <p className="discret">Pas de fiche pour ce moment : c'est à toi de jouer (visite, présentation, démo…).</p>
      )}
    </article>
  )
}
