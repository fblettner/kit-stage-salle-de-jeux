// Le jeu Coach : recrute ton équipe, choisis ta tactique, et affronte l'entraîneur IA.
// Les étapes : mercato → vestiaire → match (1re mi-temps) → mi-temps → match (2e mi-temps) → fin
import { useEffect, useState } from 'react'
import CarteJoueur from './CarteJoueur.jsx'
import ChoixTactique from './ChoixTactique.jsx'
import Match from './Match.jsx'
import Mercato from './Mercato.jsx'
import RapportIA from './RapportIA.jsx'
import './coach.css'

const DUREE_MINUTE = 200 // millisecondes pour une minute de match à l'écran
const DUREE_MINUTE_RAPIDE = 30

// Petite fonction pour envoyer une demande au serveur Python
async function envoyer(adresse, contenu) {
  const reponse = await fetch(adresse, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(contenu),
  })
  const donnees = await reponse.json()
  if (!reponse.ok) throw new Error(donnees.detail ?? `Erreur ${reponse.status}`)
  return donnees
}

function additionnerStats(a, b) {
  const somme = (x, y) => [x[0] + y[0], x[1] + y[1]]
  return { possession: somme(a.possession, b.possession), tirs: somme(a.tirs, b.tirs), cadres: somme(a.cadres, b.cadres) }
}

function Statistiques({ stats }) {
  if (!stats) return null
  const total = stats.possession[0] + stats.possession[1]
  const lignes = [
    ['Possession', `${Math.round((100 * stats.possession[0]) / total)} %`, `${Math.round((100 * stats.possession[1]) / total)} %`],
    ['Tirs', stats.tirs[0], stats.tirs[1]],
    ['Tirs cadrés', stats.cadres[0], stats.cadres[1]],
  ]
  return (
    <table className="coach-stats">
      <tbody>
        {lignes.map(([nom, a, b]) => (
          <tr key={nom}><td>{a}</td><th>{nom}</th><td>{b}</td></tr>
        ))}
      </tbody>
    </table>
  )
}

export default function Coach() {
  // Les données envoyées par le serveur au démarrage
  const [catalogue, setCatalogue] = useState(null)
  const [tactiques, setTactiques] = useState([])
  const [adversaires, setAdversaires] = useState({})
  const [erreur, setErreur] = useState('')

  // Les choix du joueur
  const [phase, setPhase] = useState('mercato')
  const [equipe, setEquipe] = useState([])
  const [nomClub, setNomClub] = useState('FC Stagiaires')
  const [niveau, setNiveau] = useState(2)
  const [tactique, setTactique] = useState('equilibree')
  const [historique, setHistorique] = useState([]) // les tactiques jouées : l'entraîneur IA s'en souvient !

  // Le match en cours
  const [decision, setDecision] = useState(null) // ce qu'a décidé l'entraîneur adverse
  const [evenements, setEvenements] = useState([])
  const [possession, setPossession] = useState([])
  const [stats, setStats] = useState(null)
  const [score, setScore] = useState([0, 0])
  const [minute, setMinute] = useState(0) // la minute affichée à l'écran
  const [minuteFin, setMinuteFin] = useState(0) // jusqu'où le match a été simulé
  const [rapide, setRapide] = useState(false)
  const [attente, setAttente] = useState(false)

  // Au démarrage : on charge les joueurs, les tactiques et les adversaires
  useEffect(() => {
    Promise.all(['/api/coach/joueurs', '/api/coach/tactiques', '/api/coach/adversaires'].map((u) => fetch(u).then((r) => r.json())))
      .then(([c, t, a]) => {
        setCatalogue(c)
        setTactiques(t)
        setAdversaires(a)
      })
      .catch(() => setErreur('Le serveur ne répond pas. Est-il bien lancé ?'))
  }, [])

  // Le « direct » : la minute affichée avance toute seule jusqu'à la fin de la partie simulée
  useEffect(() => {
    if (phase !== 'match') return
    const minuteur = setTimeout(() => {
      if (minute < minuteFin) setMinute(minute + 1)
      else setPhase(minuteFin >= 90 ? 'fin' : 'mi-temps')
    }, rapide ? DUREE_MINUTE_RAPIDE : DUREE_MINUTE)
    return () => clearTimeout(minuteur)
  }, [phase, minute, minuteFin, rapide])

  // Joue une mi-temps : l'entraîneur IA choisit sa tactique, PUIS le serveur simule
  async function jouerMiTemps(debut, fin, scoreDepart) {
    setAttente(true)
    setErreur('')
    try {
      const ids = equipe.map((j) => j.id)
      // 1. L'entraîneur adverse décide… sans connaître la tactique qu'on vient de choisir
      const choixIA = await envoyer('/api/coach/entraineur', {
        equipe: ids, historique_tactiques: historique, niveau, minute_debut: debut, score: scoreDepart,
      })
      // 2. Le serveur simule la mi-temps
      const resultat = await envoyer('/api/coach/match', {
        equipe: ids, tactique, niveau, tactique_ia: choixIA.tactique, minute_debut: debut, minute_fin: fin, score: scoreDepart,
      })
      const premiere = debut === 1
      setDecision(choixIA)
      setHistorique([...historique, tactique]) // l'entraîneur IA a vu notre tactique : il s'en souviendra
      setEvenements(premiere ? resultat.evenements : [...evenements, ...resultat.evenements])
      setPossession(premiere ? resultat.possession : [...possession, ...resultat.possession])
      setStats(premiere ? resultat.stats : additionnerStats(stats, resultat.stats))
      setScore(resultat.score)
      setMinute(debut - 1)
      setMinuteFin(fin)
      setRapide(false)
      setPhase('match')
    } catch (e) {
      setErreur(e.message === 'Failed to fetch' ? 'Le serveur ne répond pas. Est-il bien lancé ?' : e.message)
    } finally {
      setAttente(false)
    }
  }

  if (!catalogue) {
    return (
      <section className="coach">
        <h2>⚽ Coach</h2>
        <p className={erreur ? 'erreur' : ''}>{erreur || 'Chargement…'}</p>
      </section>
    )
  }

  const adversaire = adversaires[niveau]
  const nomTactique = (id) => tactiques.find((t) => t.id === id)

  // --- 1. Le mercato ---
  if (phase === 'mercato') {
    return (
      <section className="coach">
        <h2>⚽ Coach · le mercato</h2>
        <Mercato catalogue={catalogue} equipe={equipe} setEquipe={setEquipe}
          nomClub={nomClub} setNomClub={setNomClub} onValider={() => setPhase('vestiaire')} />
      </section>
    )
  }

  // --- 2. Le vestiaire : choix de l'adversaire et de la tactique ---
  if (phase === 'vestiaire') {
    return (
      <section className="coach">
        <h2>⚽ Coach · le vestiaire</h2>
        <div className="coach-jeu">
          <div>
            <div className="coach-affiche">
              <div>
                <h3>{nomClub}</h3>
                <div className="coach-equipe-mini">{equipe.map((j) => <CarteJoueur key={j.id} joueur={j} petite />)}</div>
              </div>
              <span className="coach-vs">VS</span>
              <div>
                <h3>{adversaire.nom}</h3>
                <div className="coach-equipe-mini">{adversaire.joueurs.map((j) => <CarteJoueur key={j.id} joueur={j} petite />)}</div>
              </div>
            </div>
            <h3>Ta tactique</h3>
            <ChoixTactique tactiques={tactiques} valeur={tactique} onChange={setTactique} />
          </div>
          <aside className="coach-panneau">
            <div className="carte">
              <h3>Adversaire</h3>
              <label>
                Niveau
                <select value={niveau} onChange={(e) => setNiveau(Number(e.target.value))}>
                  {Object.values(adversaires).map((a) => (
                    <option key={a.niveau} value={a.niveau}>{a.niveau_nom} : {a.nom}</option>
                  ))}
                </select>
              </label>
              <p className="discret">
                {historique.length === 0
                  ? "L'entraîneur adverse ne te connaît pas encore."
                  : `L'entraîneur adverse a déjà vu tes tactiques : ${historique.map((t) => nomTactique(t)?.emoji).join(' ')}`}
              </p>
              <div className="boutons">
                <button className="coach-bouton-principal" disabled={attente} onClick={() => jouerMiTemps(1, 45, [0, 0])}>
                  {attente ? "L'entraîneur adverse réfléchit…" : "⚽ Coup d'envoi !"}
                </button>
                <button className="secondaire" onClick={() => setPhase('mercato')}>← Changer d'équipe</button>
              </div>
              {erreur && <p className="erreur">{erreur}</p>}
            </div>
          </aside>
        </div>
      </section>
    )
  }

  // --- 3. Le match (en direct, à la mi-temps ou terminé) ---
  const [butsJoueur, butsIA] = score
  let resultatFinal = null
  if (phase === 'fin') {
    if (butsJoueur > butsIA) resultatFinal = '🏆 Victoire ! Bravo coach !'
    else if (butsJoueur === butsIA) resultatFinal = '🤝 Match nul.'
    else resultatFinal = "😞 Défaite… L'entraîneur IA a été plus malin cette fois."
  }

  return (
    <section className="coach">
      <h2>⚽ Coach · {phase === 'mi-temps' ? 'la mi-temps' : phase === 'fin' ? 'fin du match' : 'le match'}</h2>
      <div className="coach-jeu">
        <div>
          {resultatFinal && <p className="coach-consigne fin">{resultatFinal}</p>}
          <Match nomClub={nomClub} nomIA={adversaire.nom} evenements={evenements} possession={possession} minute={minute} />
          {phase === 'match' && (
            <button className="secondaire" onClick={() => setRapide(!rapide)}>{rapide ? '▶ Vitesse normale' : '⏩ Accélérer'}</button>
          )}
        </div>

        <aside className="coach-panneau">
          {phase === 'mi-temps' && (
            <div className="carte">
              <h3>Mi-temps : change ta tactique ?</h3>
              <ChoixTactique tactiques={tactiques} valeur={tactique} onChange={setTactique} />
              <button className="coach-bouton-principal" disabled={attente} onClick={() => jouerMiTemps(46, 90, score)}>
                {attente ? "L'entraîneur adverse réfléchit…" : 'Reprendre le match →'}
              </button>
              {erreur && <p className="erreur">{erreur}</p>}
            </div>
          )}
          {phase === 'fin' && (
            <div className="carte">
              <h3>Et maintenant ?</h3>
              <div className="boutons">
                <button onClick={() => setPhase('vestiaire')}>Revanche</button>
                <button className="secondaire" onClick={() => setPhase('mercato')}>Changer d'équipe</button>
              </div>
            </div>
          )}
          {phase !== 'match' && (
            <div className="carte">
              <h3>Statistiques</h3>
              <Statistiques stats={stats} />
            </div>
          )}
          <div className="carte">
            <h3>Dans la tête de l'entraîneur adverse</h3>
            <p className="discret">Ta tactique : {nomTactique(tactique)?.emoji} {nomTactique(tactique)?.nom}</p>
            <RapportIA decision={decision} tactiques={tactiques} />
          </div>
        </aside>
      </div>
    </section>
  )
}
