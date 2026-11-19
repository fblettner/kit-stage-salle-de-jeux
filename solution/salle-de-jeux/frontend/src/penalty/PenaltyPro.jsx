// Penalty Pro : vise, choisis ta puissance… et déjoue le gardien qui apprend tes habitudes.
// Puis change de rôle : à toi d'arrêter les tirs de l'ordinateur !
import { useEffect, useRef, useState } from 'react'
import Cage from './Cage.jsx'
import PenseeIA from './PenseeIA.jsx'
import { compterButs, vainqueur } from './regles.js'
import './penalty.css'

const DUREE_ANIMATION = 1600 // en millisecondes
const PERIODE_JAUGE = 1300 // temps pour que la jauge fasse un aller-retour
const COULEUR_IA = '#2563eb'
const COULEUR_JOUEUR = '#ea580c'

const ANNONCES_TIREUR = {
  but: { texte: 'BUUUT ! ⚽', bon: true },
  arret: { texte: 'Arrêté par le gardien 🧤', bon: false },
  poteau: { texte: '💥 Sur le poteau !', bon: false },
  dehors: { texte: 'À côté ! 😬', bon: false },
}
const ANNONCES_GARDIEN = {
  but: { texte: "L'ordinateur marque… 😩", bon: false },
  arret: { texte: 'ARRÊT ! Quel plongeon 🧤', bon: true },
  poteau: { texte: '💥 Poteau ! Ouf…', bon: true },
  dehors: { texte: "L'ordinateur tire à côté ! 😅", bon: true },
}

async function envoyer(adresse, contenu) {
  const reponse = await fetch(adresse, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(contenu),
  })
  if (!reponse.ok) throw new Error(`Erreur ${reponse.status}`)
  return reponse.json()
}

// Une ligne du tableau des scores : ⚽ = but, ❌ = raté, ○ = pas encore tiré
function LigneScore({ nom, tirs, nombreDeCases }) {
  const cases = []
  for (let i = 0; i < nombreDeCases; i++) {
    const tir = tirs[i]
    cases.push(<span key={i} className="penalty-case">{!tir ? '○' : tir.resultat === 'but' ? '⚽' : '❌'}</span>)
  }
  return (
    <div className="penalty-ligne-score">
      <span className="penalty-nom">{nom}</span>
      <span className="penalty-cases">{cases}</span>
      <strong>{compterButs(tirs)}</strong>
    </div>
  )
}

// La jauge de puissance : verte (précis), puis orange, puis rouge (puissant mais imprécis)
function JaugePuissance({ valeur }) {
  return (
    <div className="penalty-jauge">
      <span className="penalty-jauge-curseur" style={{ left: `${valeur * 100}%` }} />
    </div>
  )
}

export default function PenaltyPro() {
  const [niveau, setNiveau] = useState(2)
  const [role, setRole] = useState('tireur') // le rôle du joueur : 'tireur' ou 'gardien'
  const [phase, setPhase] = useState('viser') // viser → puissance → animation (tireur) ; plonger → animation (gardien)
  const [viseur, setViseur] = useState(null) // où pointe la souris
  const [cible, setCible] = useState(null) // la cible choisie
  const [jauge, setJauge] = useState(0)
  const refJauge = useRef(0) // la valeur exacte de la jauge au moment du clic
  const [animation, setAnimation] = useState(null) // { balle, gardien, couleur }
  const [tirsJoueur, setTirsJoueur] = useState([]) // { cible, resultat }
  const [tirsOrdi, setTirsOrdi] = useState([]) // { plongeon, resultat }
  const [annonce, setAnnonce] = useState(null)
  const [pensee, setPensee] = useState(null)
  const [voirPensee, setVoirPensee] = useState(true)
  const [gagnant, setGagnant] = useState(null)
  const [erreur, setErreur] = useState('')

  // La jauge de puissance fait des allers-retours tant qu'on n'a pas cliqué
  useEffect(() => {
    if (phase !== 'puissance') return
    const debut = performance.now()
    let image
    function animer() {
      const t = ((performance.now() - debut) % PERIODE_JAUGE) / PERIODE_JAUGE
      const valeur = Math.min(1, Math.max(0, t < 0.5 ? t * 2 : 2 - t * 2)) // monte de 0 à 1, puis redescend
      refJauge.current = valeur
      setJauge(valeur)
      image = requestAnimationFrame(animer)
    }
    image = requestAnimationFrame(animer)
    return () => cancelAnimationFrame(image)
  }, [phase])

  // Après l'animation : on change de rôle, ou la séance est finie
  function terminerAction(nouveauxTirsJoueur, nouveauxTirsOrdi, prochainRole) {
    setTimeout(() => {
      setAnimation(null)
      setCible(null)
      const fin = vainqueur(nouveauxTirsJoueur, nouveauxTirsOrdi)
      if (fin) {
        setGagnant(fin)
        setPhase('fin')
      } else {
        setRole(prochainRole)
        setPhase(prochainRole === 'tireur' ? 'viser' : 'plonger')
      }
    }, DUREE_ANIMATION)
  }

  // 1er clic : on choisit où viser. 2e clic : on arrête la jauge et on tire.
  async function cliquerDansLeBut(point) {
    if (phase === 'viser') {
      setCible(point)
      setPhase('puissance')
    } else if (phase === 'puissance') {
      await tirer(refJauge.current)
    } else if (phase === 'plonger') {
      await plonger(point)
    }
  }

  async function tirer(puissance) {
    setPhase('animation')
    setErreur('')
    try {
      // Le serveur est l'arbitre. Le gardien IA ne reçoit que nos tirs PRÉCÉDENTS.
      const reponse = await envoyer('/api/penalty/tir', {
        cible, puissance, niveau, historique: tirsJoueur.map((t) => t.cible),
      })
      const nouveaux = [...tirsJoueur, { cible, resultat: reponse.resultat }]
      setTirsJoueur(nouveaux)
      setAnimation({ balle: reponse.impact, gardien: reponse.plongeon, couleur: COULEUR_IA })
      const auDessus = reponse.resultat === 'dehors' && reponse.impact.y < 0
      setAnnonce(auDessus ? { texte: 'Au-dessus de la barre ! 😬', bon: false } : ANNONCES_TIREUR[reponse.resultat])
      setPensee({ titre: 'Où le gardien pensait que tu allais tirer :', ...reponse })
      terminerAction(nouveaux, tirsOrdi, 'gardien')
    } catch {
      setErreur('Le serveur ne répond pas. Est-il bien lancé ?')
      setPhase('viser')
    }
  }

  async function plonger(plongeon) {
    setPhase('animation')
    setErreur('')
    try {
      // Le tireur IA ne reçoit que nos plongeons PRÉCÉDENTS.
      const reponse = await envoyer('/api/penalty/arret', {
        plongeon, niveau, historique: tirsOrdi.map((t) => t.plongeon),
      })
      const nouveaux = [...tirsOrdi, { plongeon, resultat: reponse.resultat }]
      setTirsOrdi(nouveaux)
      setAnimation({ balle: reponse.impact, gardien: plongeon, couleur: COULEUR_JOUEUR })
      setAnnonce(ANNONCES_GARDIEN[reponse.resultat])
      setPensee({ titre: 'Où le tireur pensait que tu allais plonger :', ...reponse })
      terminerAction(tirsJoueur, nouveaux, 'tireur')
    } catch {
      setErreur('Le serveur ne répond pas. Est-il bien lancé ?')
      setPhase('plonger')
    }
  }

  function nouvelleSeance() {
    setTirsJoueur([])
    setTirsOrdi([])
    setRole('tireur')
    setPhase('viser')
    setCible(null)
    setAnimation(null)
    setAnnonce(null)
    setPensee(null)
    setGagnant(null)
    setErreur('')
  }

  let consigne
  if (gagnant === 'joueur') consigne = '🏆 Tu as gagné la séance de tirs au but !'
  else if (gagnant === 'ordi') consigne = "🤖 L'ordinateur gagne la séance… Revanche ?"
  else if (phase === 'viser') consigne = '1. Vise : clique dans le but.'
  else if (phase === 'puissance') consigne = '2. Puissance : clique pour arrêter la jauge !'
  else if (phase === 'plonger') consigne = "À toi d'arrêter ! Clique où tu veux plonger."
  else consigne = role === 'tireur' ? 'Le ballon part…' : "L'ordinateur tire…"

  const interactif = ['viser', 'puissance', 'plonger'].includes(phase)
  const mortSubite = !gagnant && tirsJoueur.length >= 5 && tirsOrdi.length >= 5
  const nombreDeCases = Math.max(5, tirsJoueur.length, tirsOrdi.length)
  const couleurGardien = animation ? animation.couleur : role === 'tireur' ? COULEUR_IA : COULEUR_JOUEUR

  return (
    <section className="penalty">
      <h2>⚽ Penalty Pro</h2>
      <div className="penalty-jeu">
        <div>
          <p className={`penalty-consigne ${gagnant ? 'fin' : ''}`}>
            {consigne} {mortSubite && <span className="penalty-badge">Mort subite !</span>}
          </p>
          <Cage
            viseur={phase === 'puissance' ? cible : phase === 'viser' || phase === 'plonger' ? viseur : null}
            balle={animation?.balle}
            gardien={animation?.gardien}
            couleurGardien={couleurGardien}
            interactif={interactif}
            onSurvol={setViseur}
            onClic={cliquerDansLeBut}
          />
          {phase === 'puissance' && (
            <div className="penalty-zone-jauge" onClick={() => tirer(refJauge.current)}>
              <span>Puissance</span>
              <JaugePuissance valeur={jauge} />
              <span className="discret">vert = précis · rouge = puissant mais risqué</span>
            </div>
          )}
          <p className={`penalty-annonce ${annonce ? (annonce.bon ? 'bon' : 'mauvais') : ''}`}>{annonce?.texte}</p>
          {erreur && <p className="erreur">{erreur}</p>}
        </div>

        <aside className="penalty-panneau">
          <div className="carte">
            <h3>Score</h3>
            <LigneScore nom="Toi" tirs={tirsJoueur} nombreDeCases={nombreDeCases} />
            <LigneScore nom="IA" tirs={tirsOrdi} nombreDeCases={nombreDeCases} />
          </div>
          <div className="carte">
            <h3>Réglages</h3>
            <label>
              Niveau de l'ordinateur
              <select value={niveau} onChange={(e) => setNiveau(Number(e.target.value))}>
                <option value={1}>Facile</option>
                <option value={2}>Moyen</option>
                <option value={3}>Difficile</option>
              </select>
            </label>
            <button onClick={nouvelleSeance} disabled={phase === 'animation'}>Nouvelle séance</button>
          </div>
          <div className="carte">
            <h3>Dans la tête de l'IA</h3>
            <label className="case-a-cocher">
              <input type="checkbox" checked={voirPensee} onChange={(e) => setVoirPensee(e.target.checked)} />
              Montrer ce que pense l'IA
            </label>
            {voirPensee && <PenseeIA pensee={pensee} />}
          </div>
        </aside>
      </div>
    </section>
  )
}
