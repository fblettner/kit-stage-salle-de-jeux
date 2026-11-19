// Petits calculs sur l'équipe (les mêmes règles que le serveur, pour guider le joueur pendant le mercato)

// Résume une équipe en 5 notes, comme le moteur de match (backend/app/coach/simulateur.py)
export function forcesEquipe(joueurs) {
  const champ = joueurs.filter((j) => j.poste !== 'G')
  const gardien = joueurs.find((j) => j.poste === 'G')
  const moyenne = (carac) => (champ.length ? Math.round(champ.reduce((s, j) => s + j[carac], 0) / champ.length) : 0)
  return {
    attaque: moyenne('attaque'),
    defense: moyenne('defense'),
    technique: moyenne('technique'),
    vitesse: moyenne('vitesse'),
    gardien: gardien ? gardien.defense : 0,
  }
}

export function coutEquipe(joueurs) {
  return joueurs.reduce((total, j) => total + j.prix, 0)
}

// Pourquoi ne peut-on pas ajouter ce joueur ? (null si c'est possible)
export function raisonRefus(joueur, equipe, regles) {
  if (equipe.some((j) => j.id === joueur.id)) return null // déjà choisi : on peut le retirer
  if (equipe.length >= regles.taille_equipe) return `Équipe complète (${regles.taille_equipe} joueurs)`
  const aUnGardien = equipe.some((j) => j.poste === 'G')
  if (joueur.poste === 'G' && aUnGardien) return 'Tu as déjà un gardien'
  const placesRestantes = regles.taille_equipe - equipe.length
  if (joueur.poste !== 'G' && !aUnGardien && placesRestantes === 1) return 'Il te faut encore un gardien'
  if (coutEquipe(equipe) + joueur.prix > regles.budget) return 'Trop cher pour ton budget'
  return null
}

export function equipeValide(equipe, regles) {
  return (
    equipe.length === regles.taille_equipe &&
    equipe.filter((j) => j.poste === 'G').length === 1 &&
    coutEquipe(equipe) <= regles.budget
  )
}
