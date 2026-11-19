// Les règles de la séance de tirs au but : qui a gagné ?
// (Le résultat de chaque tir, lui, est décidé par le serveur : c'est l'arbitre.)

export function compterButs(tirs) {
  return tirs.filter((tir) => tir.resultat === 'but').length
}

// Qui a gagné ? Renvoie 'joueur', 'ordi', ou null si la séance continue.
// Le joueur tire toujours en premier : il a donc autant ou un tir de plus que l'ordinateur.
export function vainqueur(tirsJoueur, tirsOrdi) {
  const butsJoueur = compterButs(tirsJoueur)
  const butsOrdi = compterButs(tirsOrdi)

  // Pendant les 5 premiers tirs : on s'arrête dès que l'écart ne peut plus être rattrapé
  if (tirsJoueur.length <= 5 && tirsOrdi.length <= 5) {
    const tirsRestantsJoueur = 5 - tirsJoueur.length
    const tirsRestantsOrdi = 5 - tirsOrdi.length
    if (butsJoueur > butsOrdi + tirsRestantsOrdi) return 'joueur'
    if (butsOrdi > butsJoueur + tirsRestantsJoueur) return 'ordi'
    if (tirsJoueur.length < 5 || tirsOrdi.length < 5) return null
  }

  // Après 5 tirs chacun, c'est la mort subite : on compare quand les deux ont tiré autant de fois
  if (tirsJoueur.length === tirsOrdi.length && butsJoueur !== butsOrdi) {
    return butsJoueur > butsOrdi ? 'joueur' : 'ordi'
  }
  return null
}
