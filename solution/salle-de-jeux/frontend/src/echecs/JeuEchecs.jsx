import { useRef, useState } from 'react'
import { Chessboard } from 'react-chessboard'
import { Chess, DEFAULT_POSITION } from 'chess.js'
import './echecs.css'

const NOMS_NIVEAUX = { 1: 'Facile', 2: 'Moyen', 3: 'Difficile' }

// Couleurs utilisées pour colorier les cases de l'échiquier
const STYLE_DERNIER_COUP = { background: 'rgba(255, 213, 79, 0.55)' }
const STYLE_SELECTION = { background: 'rgba(122, 78, 45, 0.45)' }
const STYLE_ECHEC = { background: 'radial-gradient(circle, rgba(220, 38, 38, 0.85) 30%, transparent 75%)' }
const STYLE_COUP_POSSIBLE = { background: 'radial-gradient(circle, rgba(0, 0, 0, 0.22) 22%, transparent 24%)' }
const STYLE_PRISE_POSSIBLE = { background: 'radial-gradient(circle, transparent 58%, rgba(0, 0, 0, 0.22) 60%)' }

// Explique pourquoi la partie est finie, en français
function messageFinDePartie(partie, couleurJoueur) {
  if (partie.isCheckmate()) {
    const perdant = partie.turn() // celui qui devait jouer est mat
    return perdant === couleurJoueur ? "Échec et mat… l'ordinateur a gagné 🤖" : 'Échec et mat ! Vous avez gagné 🎉'
  }
  if (partie.isStalemate()) return 'Pat : match nul 🤝'
  if (partie.isThreefoldRepetition()) return 'Même position 3 fois : match nul 🤝'
  if (partie.isInsufficientMaterial()) return 'Plus assez de pièces pour mater : match nul 🤝'
  return 'Match nul 🤝'
}

// Trouve la case du roi qui est en échec (pour la colorier en rouge)
function caseDuRoiEnEchec(partie) {
  if (!partie.inCheck()) return null
  for (const ligne of partie.board()) {
    for (const piece of ligne) {
      if (piece && piece.type === 'k' && piece.color === partie.turn()) return piece.square
    }
  }
  return null
}

export default function JeuEchecs() {
  // "partie" connaît toutes les règles des échecs (grâce à la librairie chess.js)
  const partie = useRef(new Chess())

  // Tout ce qui s'affiche à l'écran est rangé dans des "états"
  const [position, setPosition] = useState(DEFAULT_POSITION)
  const [historique, setHistorique] = useState([])
  const [dernierCoup, setDernierCoup] = useState(null)
  const [caseChoisie, setCaseChoisie] = useState(null)
  const [ordiReflechit, setOrdiReflechit] = useState(false)
  const [niveau, setNiveau] = useState(2)
  const [couleurJoueur, setCouleurJoueur] = useState('w')
  const [modeDebutant, setModeDebutant] = useState(true)
  const [infoOrdi, setInfoOrdi] = useState('')
  const [erreur, setErreur] = useState('')
  const [finDePartie, setFinDePartie] = useState('')

  // Met à jour l'affichage après chaque coup
  function rafraichir(coup) {
    const p = partie.current
    setPosition(p.fen())
    setHistorique(p.history())
    setDernierCoup(coup ? { from: coup.from, to: coup.to } : null)
    setCaseChoisie(null)
    setFinDePartie(p.isGameOver() ? messageFinDePartie(p, couleurJoueur) : '')
  }

  // Demande au serveur Python de choisir le coup de l'ordinateur
  async function faireJouerOrdi(niveauChoisi = niveau) {
    setOrdiReflechit(true)
    setErreur('')
    try {
      const reponse = await fetch('/api/echecs/coup-ia', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fen: partie.current.fen(), niveau: niveauChoisi }),
      })
      if (!reponse.ok) throw new Error(`Erreur ${reponse.status}`)
      const donnees = await reponse.json()
      // Le coup arrive au format "e7e5" (case de départ + case d'arrivée)
      const coup = partie.current.move(donnees.coup)
      rafraichir(coup)
      setInfoOrdi(`L'ordinateur a examiné ${donnees.positions_examinees.toLocaleString('fr-FR')} positions.`)
    } catch {
      setErreur("Le serveur ne répond pas. Est-il bien lancé ?")
    } finally {
      setOrdiReflechit(false)
    }
  }

  // Essaie de jouer le coup du joueur ; renvoie true si c'est autorisé
  function jouerCoupJoueur(depart, arrivee) {
    const p = partie.current
    if (ordiReflechit || p.isGameOver() || p.turn() !== couleurJoueur) return false
    let coup
    try {
      // promotion: 'q' → un pion qui arrive au bout devient une dame
      coup = p.move({ from: depart, to: arrivee, promotion: 'q' })
    } catch {
      return false // coup interdit : la pièce revient à sa place
    }
    rafraichir(coup)
    if (!p.isGameOver()) faireJouerOrdi()
    return true
  }

  // Jouer en faisant glisser une pièce
  function quandOnLachePiece({ sourceSquare, targetSquare }) {
    if (!targetSquare) return false
    return jouerCoupJoueur(sourceSquare, targetSquare)
  }

  // Jouer en cliquant : 1er clic sur la pièce, 2e clic sur la case d'arrivée
  function quandOnCliqueCase({ square }) {
    const piece = partie.current.get(square)
    if (caseChoisie && jouerCoupJoueur(caseChoisie, square)) return
    setCaseChoisie(piece && piece.color === couleurJoueur ? square : null)
  }

  function nouvellePartie(couleur = couleurJoueur) {
    partie.current = new Chess()
    setCouleurJoueur(couleur)
    setInfoOrdi('')
    setErreur('')
    setFinDePartie('')
    setHistorique([])
    setDernierCoup(null)
    setCaseChoisie(null)
    setPosition(DEFAULT_POSITION)
    // Si le joueur prend les noirs, c'est l'ordinateur qui commence
    if (couleur === 'b') faireJouerOrdi()
  }

  // Colorie les cases : dernier coup, roi en échec, coups possibles (mode débutant)
  const stylesCases = {}
  if (dernierCoup) {
    stylesCases[dernierCoup.from] = STYLE_DERNIER_COUP
    stylesCases[dernierCoup.to] = STYLE_DERNIER_COUP
  }
  const affichage = new Chess(position)
  const roiEnEchec = caseDuRoiEnEchec(affichage)
  if (roiEnEchec) stylesCases[roiEnEchec] = STYLE_ECHEC
  if (caseChoisie) {
    stylesCases[caseChoisie] = STYLE_SELECTION
    if (modeDebutant) {
      for (const coup of affichage.moves({ square: caseChoisie, verbose: true })) {
        stylesCases[coup.to] = coup.captured ? STYLE_PRISE_POSSIBLE : STYLE_COUP_POSSIBLE
      }
    }
  }

  let statut
  if (finDePartie) statut = finDePartie
  else if (ordiReflechit) statut = "L'ordinateur réfléchit…"
  else statut = affichage.inCheck() ? 'Échec ! À vous de jouer.' : 'À vous de jouer.'

  // On regroupe l'historique par paires : "1. e4 e5", "2. Cf3 Cc6"…
  const tours = []
  for (let i = 0; i < historique.length; i += 2) tours.push([historique[i], historique[i + 1]])

  return (
    <section>
      <h2>♞ Échecs contre l'IA</h2>

      <div className="echecs-jeu">
        <section className="echecs-plateau">
          <p className={`echecs-statut ${finDePartie ? 'fin' : ''}`}>{statut}</p>
          <Chessboard
            options={{
              position,
              boardOrientation: couleurJoueur === 'w' ? 'white' : 'black',
              onPieceDrop: quandOnLachePiece,
              onSquareClick: quandOnCliqueCase,
              squareStyles: stylesCases,
              allowDragging: !ordiReflechit && !finDePartie,
            }}
          />
          {erreur && <p className="erreur">{erreur}</p>}
        </section>

        <aside className="echecs-panneau">
          <div className="carte">
            <h3>Réglages</h3>
            <label>
              Niveau de l'ordinateur
              <select value={niveau} onChange={(e) => setNiveau(Number(e.target.value))}>
                {Object.entries(NOMS_NIVEAUX).map(([n, nom]) => (
                  <option key={n} value={n}>{nom}</option>
                ))}
              </select>
            </label>
            <label className="case-a-cocher">
              <input type="checkbox" checked={modeDebutant} onChange={(e) => setModeDebutant(e.target.checked)} />
              Mode débutant (montrer les coups possibles)
            </label>
            <div className="boutons">
              <button onClick={() => nouvellePartie('w')} disabled={ordiReflechit}>Jouer les Blancs</button>
              <button className="secondaire" onClick={() => nouvellePartie('b')} disabled={ordiReflechit}>Jouer les Noirs</button>
            </div>
          </div>

          <div className="carte">
            <h3>Coups joués</h3>
            {tours.length === 0 ? (
              <p className="discret">Aucun coup pour l'instant.</p>
            ) : (
              <ol className="echecs-historique">
                {tours.map(([blanc, noir], i) => (
                  <li key={i}><span>{blanc}</span><span>{noir ?? ''}</span></li>
                ))}
              </ol>
            )}
            {infoOrdi && <p className="discret">{infoOrdi}</p>}
          </div>
        </aside>
      </div>
    </section>
  )
}
