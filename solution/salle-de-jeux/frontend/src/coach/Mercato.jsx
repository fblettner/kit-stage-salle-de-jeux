// Le mercato : on recrute 5 joueurs sans dépasser le budget
import { useState } from 'react'
import CarteJoueur from './CarteJoueur.jsx'
import Jauge from './Jauge.jsx'
import { coutEquipe, equipeValide, forcesEquipe, raisonRefus } from './equipe.js'

const FILTRES = [
  ['tous', 'Tous'],
  ['G', 'Gardiens'],
  ['DEF', 'Défenseurs'],
  ['MIL', 'Milieux'],
  ['ATT', 'Attaquants'],
]

export default function Mercato({ catalogue, equipe, setEquipe, nomClub, setNomClub, onValider }) {
  const [filtre, setFiltre] = useState('tous')
  const regles = { budget: catalogue.budget, taille_equipe: catalogue.taille_equipe }
  const depense = coutEquipe(equipe)
  const forces = forcesEquipe(equipe)

  function basculer(joueur) {
    if (equipe.some((j) => j.id === joueur.id)) setEquipe(equipe.filter((j) => j.id !== joueur.id))
    else if (!raisonRefus(joueur, equipe, regles)) setEquipe([...equipe, joueur])
  }

  const visibles = catalogue.joueurs.filter((j) => filtre === 'tous' || j.poste === filtre)

  return (
    <div className="coach-jeu">
      <div>
        <p className="coach-consigne">Recrute 5 joueurs : 1 gardien et 4 joueurs de champ, sans dépasser {catalogue.budget} M€.</p>
        <div className="coach-filtres">
          {FILTRES.map(([id, nom]) => (
            <button key={id} className={filtre === id ? '' : 'secondaire'} onClick={() => setFiltre(id)}>{nom}</button>
          ))}
        </div>
        <div className="coach-grille-cartes">
          {visibles.map((j) => (
            <CarteJoueur
              key={j.id}
              joueur={j}
              choisi={equipe.some((e) => e.id === j.id)}
              refus={raisonRefus(j, equipe, regles)}
              onClick={() => basculer(j)}
            />
          ))}
        </div>
      </div>

      <aside className="coach-panneau">
        <div className="carte">
          <h3>Ton club</h3>
          <label>
            Nom du club
            <input className="coach-champ" value={nomClub} maxLength={24} onChange={(e) => setNomClub(e.target.value)} />
          </label>
          <div className="coach-budget">
            <span>Budget : <b>{depense}</b> / {catalogue.budget} M€</span>
            <span className="coach-jauge-fond"><span style={{ width: `${Math.min(100, (100 * depense) / catalogue.budget)}%` }} /></span>
          </div>
          <div className="coach-equipe-mini">
            {equipe.length === 0 && <p className="discret">Clique sur des cartes pour recruter.</p>}
            {equipe.map((j) => (
              <CarteJoueur key={j.id} joueur={j} choisi petite onClick={() => basculer(j)} />
            ))}
          </div>
        </div>

        <div className="carte">
          <h3>Forces de l'équipe</h3>
          <Jauge nom="Attaque" valeur={forces.attaque} />
          <Jauge nom="Défense" valeur={forces.defense} />
          <Jauge nom="Technique" valeur={forces.technique} />
          <Jauge nom="Vitesse" valeur={forces.vitesse} />
          <Jauge nom="Gardien" valeur={forces.gardien} />
          <button className="coach-bouton-principal" disabled={!equipeValide(equipe, regles)} onClick={onValider}>
            Aller au vestiaire →
          </button>
        </div>
      </aside>
    </div>
  )
}
