// Ce fichier est COMMUN à tous les jeux : c'est le menu d'accueil de la salle de jeux.
// Chaque jeu vit dans son propre dossier : src/echecs/, src/coach/, src/penalty/, src/flechettes/
import { useEffect, useState } from 'react'
import JeuEchecs from './echecs/JeuEchecs.jsx'
import Coach from './coach/Coach.jsx'
import Flechettes from './flechettes/Flechettes.jsx'
import PenaltyPro from './penalty/PenaltyPro.jsx'
import './App.css'

// La liste des jeux de la salle. Pour ajouter un jeu, il suffit d'ajouter une ligne ici.
const JEUX = [
  {
    id: 'echecs',
    icone: '♞',
    titre: "Échecs contre l'IA",
    description: "L'ordinateur imagine plusieurs coups à l'avance pour choisir le meilleur.",
    composant: JeuEchecs,
  },
  {
    id: 'coach',
    icone: '⚽',
    titre: 'Coach',
    description: "Recrute ton équipe, choisis ta tactique… l'entraîneur adverse simule des centaines de matchs pour te battre.",
    composant: Coach,
  },
  {
    id: 'penalty',
    icone: '🥅',
    titre: 'Penalty Pro',
    description: 'Vise, dose ta puissance… le gardien apprend tes habitudes. Puis à toi d\'arrêter ses tirs !',
    composant: PenaltyPro,
  },
  {
    id: 'flechettes',
    icone: '🎯',
    titre: 'Fléchettes',
    description: "Une partie de 301 : ta main tremble, l'IA calcule où viser selon sa précision.",
    composant: Flechettes,
  },
]

export default function App() {
  const [jeuChoisi, setJeuChoisi] = useState(null)
  const [messageServeur, setMessageServeur] = useState('Connexion au serveur…')

  // Au démarrage, on demande au serveur s'il est bien là
  useEffect(() => {
    fetch('/api/sante')
      .then((reponse) => reponse.json())
      .then((donnees) => setMessageServeur(donnees.message))
      .catch(() => setMessageServeur('Le serveur ne répond pas 😕'))
  }, [])

  const jeu = JEUX.find((j) => j.id === jeuChoisi)

  // Un jeu est choisi : on l'affiche, avec un bouton pour revenir au menu
  if (jeu) {
    const Jeu = jeu.composant
    return (
      <main className="page">
        <button className="secondaire retour" onClick={() => setJeuChoisi(null)}>← Menu</button>
        <Jeu />
      </main>
    )
  }

  // Sinon : le menu
  return (
    <main className="page">
      <header>
        <h1>🎮 La salle de jeux</h1>
        <p className="sous-titre">Projet réalisé pendant le stage de 3e · {messageServeur}</p>
      </header>
      <div className="menu">
        {JEUX.map((j) => (
          <button key={j.id} className="tuile" onClick={() => setJeuChoisi(j.id)}>
            <span className="icone">{j.icone}</span>
            <span className="titre">{j.titre}</span>
            <span className="description">{j.description}</span>
          </button>
        ))}
      </div>
    </main>
  )
}
