import { useEffect, useRef, useState } from 'react'
import { api, lienSalle, useApi } from '../api.js'
import Salle from '../Salle.jsx'
import Coquille from '../Coquille.jsx'
import Icone from '../Icone.jsx'
import Aide from './Aide.jsx'
import Bugs from './Bugs.jsx'
import Carnet from './Carnet.jsx'
import Depannage from './Depannage.jsx'
import Lexique from './Lexique.jsx'
import Parcours from './Parcours.jsx'
import Projet from './Projet.jsx'

const SECTIONS = [
  {
    titre: 'Ma semaine',
    liens: [
      { cle: 'parcours', nom: 'Ma journée', icone: 'calendrier', description: 'Le programme, étape par étape' },
      { cle: 'projet', nom: 'Mon projet', icone: 'manette', description: "Joue aux jeux d'exemple, lis les fiches, puis choisis ton jeu" },
      { cle: 'carnet', nom: 'Carnet de bord', icone: 'carnet', description: "À remplir chaque soir (10 minutes). Tout s'enregistre automatiquement." },
    ],
  },
  {
    titre: 'Mes outils',
    liens: [
      { cle: 'bugs', nom: 'Bugs', icone: 'bug', titre: 'La chasse aux bugs', description: "Ce que j'ai fait, ce qui s'est passé, ce qui aurait dû se passer" },
      { cle: 'lexique', nom: 'Lexique', icone: 'lexique', titre: 'Petit lexique du développeur', description: 'Les mots du métier, expliqués simplement' },
      { cle: 'depannage', nom: 'Je suis bloqué', icone: 'bouee', description: "L'échelle du dépannage : quoi faire, dans quel ordre" },
    ],
  },
]

export default function Stagiaire({ prenom, onDeconnexion }) {
  const [onglet, setOnglet] = useState('parcours')
  const [aideOuverte, setAideOuverte] = useState(false)
  const [annonce, setAnnonce] = useState('')
  const programme = useApi('/programme', { toutesLes: 20 })
  const moi = useApi('/moi', { toutesLes: 15 })
  const [activite, setActivite] = useState(null)

  // Prévenir quand l'animateur répond ou quand la demande du client arrive
  const avant = useRef(null)
  useEffect(() => {
    const m = moi.donnees
    if (!m) return
    const etat = {
      reponses: m.aides.filter((a) => a.reponse).map((a) => a.id + a.reponse).join('|'),
      surprises: m.surprises.join(','),
    }
    if (avant.current) {
      if (etat.surprises !== avant.current.surprises && m.surprises.length) setAnnonce('🎭 Le client a une nouvelle demande ! Regarde « Le client change d\'avis ».')
      else if (etat.reponses !== avant.current.reponses) setAnnonce('💬 Ton maître de stage t\'a répondu ! (bouton SOS)')
    }
    avant.current = etat
  }, [moi.donnees])

  async function cocher(cle, fait) {
    moi.setDonnees((m) => ({ ...m, coches: { ...m.coches, [cle]: fait } }))
    try {
      await api('/moi/coche', { methode: 'PUT', corps: { cle, fait } })
    } catch (e) {
      setAnnonce('⚠️ ' + e.message)
    }
    moi.recharger()
  }

  async function repondre(cle, texte) {
    await api('/moi/reponse', { methode: 'PUT', corps: { cle, texte } })
    moi.setDonnees((m) => ({ ...m, reponses: { ...m.reponses, [cle]: texte } }))
  }

  if (!programme.donnees || !moi.donnees)
    return <p className="chargement">{programme.erreur || moi.erreur || 'Chargement…'}</p>

  const p = programme.donnees
  const m = moi.donnees
  const jeu = m.jeu ? p.jeux[m.jeu] : null
  const reponsesNonLues = m.aides.filter((a) => a.statut === 'repondue').length
  const activites = Object.values(m.avancement)
  const finies = activites.filter((a) => a.fini).length
  const bugsACorriger = m.bugs.recus.filter((b) => !b.corrige).length
  const salle = lienSalle(p)
  const sections = SECTIONS.map((s) => ({
    ...s,
    liens: s.liens.map((l) => (l.cle === 'bugs' ? { ...l, badge: bugsACorriger } : l)),
  }))
  // La salle de jeux d'exemple : pour jouer aux 4 jeux avant de choisir, et pour s'en inspirer ensuite
  if (salle) sections[0].liens.splice(2, 0, salle)

  function allerA(cle) {
    setOnglet(cle)
    moi.recharger()
  }

  return (
    <Coquille
      sections={sections}
      page={onglet}
      allerA={allerA}
      onDeconnexion={onDeconnexion}
      qui={
        <>
          <strong>{prenom}</strong>
          <span>{jeu ? `${jeu.icone} ${jeu.nom}` : 'jeu pas encore choisi'}</span>
        </>
      }
      pied={
        <div className="nav-avancement">
          {finies} activité{finies > 1 ? 's' : ''} terminée{finies > 1 ? 's' : ''} sur {activites.length}
          <div className="jauge"><span style={{ width: `${(100 * finies) / activites.length}%` }} /></div>
        </div>
      }
      actions={
        <>
          <button className="bouton-aide" onClick={() => setAideOuverte(true)}>
            SOS
            {reponsesNonLues > 0 && <span className="badge">{reponsesNonLues}</span>}
          </button>
        </>
      }
    >
      {annonce && (
        <div className="annonce" role="status">
          <span>{annonce}</span>
          <button onClick={() => setAnnonce('')}>OK</button>
        </div>
      )}
      {onglet === 'parcours' && p.message && (
        <div className="encart violet mot-du-jour">
          <Icone nom="punaise" taille={20} />
          <div>
            <strong>Le mot de ton maître de stage</strong>
            <p>{p.message}</p>
          </div>
        </div>
      )}
      {onglet === 'parcours' && (
        <Parcours
          programme={p}
          moi={m}
          onCocher={cocher}
          onRepondre={repondre}
          allerA={allerA}
          activite={activite}
          setActivite={setActivite}
        />
      )}
      {onglet === 'projet' && <Projet moi={m} recharger={moi.recharger} onRepondre={repondre} salle={salle} allerA={allerA} />}
      {onglet === 'salle' && <Salle />}
      {onglet === 'carnet' && <Carnet moi={m} prenom={prenom} jeu={jeu} onRepondre={repondre} />}
      {onglet === 'bugs' && <Bugs moi={m} recharger={moi.recharger} jeux={p.jeux} />}
      {onglet === 'lexique' && <Lexique />}
      {onglet === 'depannage' && <Depannage ouvrirAide={() => setAideOuverte(true)} />}
      {aideOuverte && (
        <Aide
          moi={m}
          programme={p}
          activite={activite || p.activite_actuelle}
          recharger={moi.recharger}
          onFermer={() => setAideOuverte(false)}
          allerA={(cle) => { setAideOuverte(false); allerA(cle) }}
        />
      )}
    </Coquille>
  )
}
