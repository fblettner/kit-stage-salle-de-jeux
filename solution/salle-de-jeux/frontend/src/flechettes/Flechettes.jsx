// Les fléchettes : une partie de 301 contre l'ordinateur.
// Ta main tremble un peu : lance au bon moment ! L'IA, elle, calcule où viser selon sa précision.
import { useEffect, useRef, useState } from 'react'
import Cible from './Cible.jsx'
import './flechettes.css'

const AMPLITUDE_TREMBLEMENT = 14 // en mm : de combien la main tremble
const COULEUR_JOUEUR = '#f59e0b'
const COULEUR_IA = '#3b82f6'
const PAUSE_IA = 900 // millisecondes entre deux fléchettes de l'IA

async function envoyer(adresse, contenu) {
  const reponse = await fetch(adresse, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(contenu),
  })
  if (!reponse.ok) throw new Error(`Erreur ${reponse.status}`)
  return reponse.json()
}

const attendre = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

export default function Flechettes() {
  // Les réglages
  const [depart, setDepart] = useState(301)
  const [doubleSortie, setDoubleSortie] = useState(false)
  const [niveau, setNiveau] = useState(2)
  // La partie
  const [restant, setRestant] = useState({ joueur: 301, ia: 301 })
  const [tour, setTour] = useState('joueur') // 'joueur', 'ia' ou 'fin'
  const [volee, setVolee] = useState([]) // les fléchettes de la volée en cours
  const [debutVolee, setDebutVolee] = useState(301) // le score au début de la volée (pour annuler en cas de « bust »)
  const [gagnant, setGagnant] = useState(null)
  const [message, setMessage] = useState('')
  const [attente, setAttente] = useState(false)
  const [erreur, setErreur] = useState('')
  // Le viseur qui tremble
  const [souris, setSouris] = useState(null) // où pointe la souris (là où le joueur VEUT viser)
  const [tremblement, setTremblement] = useState({ x: 0, y: 0 })
  const refTremblement = useRef({ x: 0, y: 0 })
  // L'IA et le conseiller
  const [lancers, setLancers] = useState([]) // tous nos lancers : où on visait, où c'est tombé
  const [viseeIA, setViseeIA] = useState(null)
  const [penseeIA, setPenseeIA] = useState(null) // { explication, carte }
  const [conseil, setConseil] = useState(null) // { visee, explication, carte }
  const [voirCarte, setVoirCarte] = useState(false)

  // La main tremble : le viseur décrit une petite courbe autour de la souris
  const sourisSurLaCible = souris !== null
  useEffect(() => {
    if (tour !== 'joueur' || !sourisSurLaCible) return
    const debut = performance.now()
    let image
    function animer() {
      const t = (performance.now() - debut) / 1000
      const decalage = {
        x: AMPLITUDE_TREMBLEMENT * Math.sin(2.1 * t) * Math.cos(0.7 * t),
        y: AMPLITUDE_TREMBLEMENT * Math.sin(2.9 * t + 0.7),
      }
      refTremblement.current = decalage
      setTremblement(decalage)
      image = requestAnimationFrame(animer)
    }
    image = requestAnimationFrame(animer)
    return () => cancelAnimationFrame(image)
  }, [tour, sourisSurLaCible])

  function nouvellePartie(points = depart) {
    setDepart(points)
    setRestant({ joueur: points, ia: points })
    setDebutVolee(points)
    setTour('joueur')
    setVolee([])
    setGagnant(null)
    setMessage('')
    setViseeIA(null)
    setPenseeIA(null)
    setConseil(null)
    setErreur('')
  }

  // Le joueur lance une fléchette
  async function lancer(visee) {
    if (tour !== 'joueur' || attente || volee.length >= 3) return
    const decalage = refTremblement.current
    const impact = { x: visee.x + decalage.x, y: visee.y + decalage.y }
    setAttente(true)
    setErreur('')
    try {
      // Le serveur est l'arbitre : il compte les points et applique les règles
      const coup = await envoyer('/api/flechettes/lancer', { impact, restant: restant.joueur, double_sortie: doubleSortie })
      const nouvelleVolee = [...volee, { impact, couleur: COULEUR_JOUEUR, ...coup }]
      setVolee(nouvelleVolee)
      setLancers([...lancers, { visee, impact }])
      setConseil(null)
      if (coup.resultat === 'gagne') {
        setRestant({ ...restant, joueur: 0 })
        setGagnant('joueur')
        setTour('fin')
        setMessage(`${coup.libelle} ! 🏆 Tu as gagné !`)
      } else if (coup.resultat === 'bust') {
        setRestant({ ...restant, joueur: debutVolee })
        setMessage(`${coup.libelle} : trop ! 💥 « Bust » : ta volée ne compte pas.`)
        finirVolee({ ...restant, joueur: debutVolee })
      } else {
        setRestant({ ...restant, joueur: coup.restant })
        setMessage(`${coup.libelle} : ${coup.points} point${coup.points > 1 ? 's' : ''}`)
        if (nouvelleVolee.length === 3) finirVolee({ ...restant, joueur: coup.restant })
      }
    } catch {
      setErreur('Le serveur ne répond pas. Est-il bien lancé ?')
    } finally {
      setAttente(false)
    }
  }

  // Fin de notre volée : c'est au tour de l'IA
  async function finirVolee(scores) {
    setTour('ia')
    await attendre(1000)
    setVolee([])
    try {
      const reponse = await envoyer('/api/flechettes/ia/volee', { restant: scores.ia, double_sortie: doubleSortie, niveau })
      setPenseeIA({ explication: reponse.explication, carte: reponse.carte })
      // On montre les fléchettes de l'IA une par une : d'abord où elle vise, puis où ça tombe
      const affichees = []
      for (const f of reponse.flechettes) {
        setViseeIA(f.visee)
        await attendre(PAUSE_IA / 2)
        affichees.push({ impact: f.impact, couleur: COULEUR_IA, ...f })
        setVolee([...affichees])
        setMessage(`L'IA : ${f.libelle}${f.resultat === 'bust' ? ' 💥 Bust !' : ''}`)
        await attendre(PAUSE_IA / 2)
      }
      setViseeIA(null)
      setRestant({ ...scores, ia: reponse.restant })
      if (reponse.restant === 0) {
        setGagnant('ia')
        setTour('fin')
        setMessage("🤖 L'ordinateur a gagné ! Revanche ?")
        return
      }
      await attendre(800)
      setVolee([])
      setDebutVolee(scores.joueur)
      setMessage('')
      setTour('joueur')
    } catch {
      setErreur('Le serveur ne répond pas. Est-il bien lancé ?')
      setTour('joueur')
    }
  }

  // Le conseiller : il mesure notre précision et nous dit où viser
  async function demanderConseil() {
    try {
      const reponse = await envoyer('/api/flechettes/conseil', { restant: restant.joueur, double_sortie: doubleSortie, lancers })
      setConseil(reponse)
      setVoirCarte(true)
    } catch {
      setErreur('Le serveur ne répond pas. Est-il bien lancé ?')
    }
  }

  const viseur = tour === 'joueur' && souris ? { x: souris.x + tremblement.x, y: souris.y + tremblement.y } : null
  const carte = voirCarte ? (conseil?.carte ?? penseeIA?.carte) : null
  const totalVolee = volee.reduce((s, f) => s + (f.resultat === 'bust' ? 0 : f.points), 0)

  return (
    <section className="flechettes">
      <h2>🎯 Fléchettes</h2>
      <div className="flechettes-jeu">
        <div>
          <div className="flechettes-scores">
            <div className={`flechettes-score ${tour === 'joueur' ? 'actif' : ''}`}>
              <span>Toi</span><b>{restant.joueur}</b>
            </div>
            <div className={`flechettes-score ia ${tour === 'ia' ? 'actif' : ''}`}>
              <span>IA</span><b>{restant.ia}</b>
            </div>
          </div>
          <p className="flechettes-consigne">
            {gagnant ? message : tour === 'joueur'
              ? `À toi ! Fléchette ${Math.min(volee.length + 1, 3)}/3 — ta main tremble : lance au bon moment.`
              : "L'ordinateur joue…"}
          </p>
          <Cible
            flechettes={volee}
            viseur={viseur}
            viseeIA={viseeIA}
            conseil={conseil?.visee}
            carte={carte}
            interactif={tour === 'joueur' && !attente}
            onSurvol={setSouris}
            onSortie={() => setSouris(null)}
            onClic={lancer}
          />
          {!gagnant && <p className="flechettes-message">{message}</p>}
          {erreur && <p className="erreur">{erreur}</p>}
        </div>

        <aside className="flechettes-panneau">
          <div className="carte">
            <h3>Volée en cours</h3>
            <div className="flechettes-volee">
              {[0, 1, 2].map((i) => (
                <span key={i} className={volee[i] ? 'jouee' : ''}>{volee[i] ? volee[i].libelle : '🎯'}</span>
              ))}
            </div>
            <p className="discret">Total de la volée : {totalVolee}</p>
            {tour === 'joueur' && (
              <button className="secondaire" onClick={demanderConseil}>💡 Où dois-je viser ?</button>
            )}
            {conseil && <p className="discret">🧠 {conseil.explication}</p>}
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
            <label className="case-a-cocher">
              <input type="checkbox" checked={doubleSortie} onChange={(e) => setDoubleSortie(e.target.checked)} />
              Finir sur un double (comme les pros)
            </label>
            <div className="boutons">
              {[101, 301, 501].map((points) => (
                <button key={points} className={points === depart ? '' : 'secondaire'} disabled={tour === 'ia'}
                  onClick={() => nouvellePartie(points)}>{points}</button>
              ))}
            </div>
            <p className="discret">Choisis un départ pour lancer une nouvelle partie.</p>
          </div>

          <div className="carte">
            <h3>Dans la tête de l'IA</h3>
            <label className="case-a-cocher">
              <input type="checkbox" checked={voirCarte} onChange={(e) => setVoirCarte(e.target.checked)} />
              Afficher la carte de chaleur (rouge = là où l'on marque le plus en moyenne)
            </label>
            {penseeIA ? <p className="discret">🧠 « {penseeIA.explication} »</p> : <p className="discret">L'IA n'a pas encore joué.</p>}
          </div>
        </aside>
      </div>
    </section>
  )
}
